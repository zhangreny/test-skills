#!/usr/bin/env python3
"""
Download a single Google Drive file ID with `gog drive download`.

This script keeps the "one ID per invocation" contract so callers can retry
individual failures. When markdown export succeeds, it also strips embedded
base64 image reference blocks from the changed markdown files.
"""

import argparse
import os
import select
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

from strip_markdown_base64_images import clean_markdown_paths

try:
    import pty
except ModuleNotFoundError:
    pty = None


def _run_gog_without_pty(
    cmd: List[str], timeout: int, send_enters: bytes = b"\n\n"
) -> Tuple[int, str, str]:
    """Fallback for platforms without pty support, such as Windows."""
    try:
        proc = subprocess.run(
            cmd,
            input=send_enters,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return (-1, "", "timeout")

    stdout = proc.stdout.decode("utf-8", errors="replace")
    stderr = proc.stderr.decode("utf-8", errors="replace")
    combined = "\n".join(part for part in (stdout.strip(), stderr.strip()) if part)
    return (proc.returncode, stdout, combined)


def _run_gog_with_pty(
    cmd: List[str], timeout: int, send_enters: bytes = b"\n\n"
) -> Tuple[int, str, str]:
    """Run the command in a pty when supported so gog keyring prompts can pass."""
    if pty is None:
        return _run_gog_without_pty(cmd, timeout=timeout, send_enters=send_enters)

    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            close_fds=True,
        )
        os.close(slave)
        slave = None

        time.sleep(0.1)
        os.write(master, send_enters)

        out_chunks: List[bytes] = []
        deadline = time.monotonic() + timeout
        while True:
            remaining = max(0.01, deadline - time.monotonic())
            ready, _, _ = select.select([master], [], [], remaining)
            if not ready:
                proc.kill()
                proc.wait()
                return (proc.returncode or -1, "", "timeout")
            try:
                buf = os.read(master, 4096)
            except OSError:
                break
            if not buf:
                break
            out_chunks.append(buf)
            if proc.poll() is not None:
                try:
                    while True:
                        buf = os.read(master, 4096)
                        if not buf:
                            break
                        out_chunks.append(buf)
                except (OSError, BlockingIOError):
                    pass
                break

        proc.wait()
        out = b"".join(out_chunks).decode("utf-8", errors="replace")
        return (proc.returncode or 0, out, out)
    finally:
        if slave is not None:
            try:
                os.close(slave)
            except OSError:
                pass
        try:
            os.close(master)
        except OSError:
            pass


def _snapshot_markdown_files(output_dir: str) -> Dict[str, Tuple[int, int]]:
    snapshot: Dict[str, Tuple[int, int]] = {}
    for path in Path(output_dir).rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".markdown"}:
            stat = path.stat()
            snapshot[str(path.resolve())] = (stat.st_mtime_ns, stat.st_size)
    return snapshot


def _find_changed_markdown_files(
    before: Dict[str, Tuple[int, int]], output_dir: str
) -> List[str]:
    after = _snapshot_markdown_files(output_dir)
    changed = sorted(
        path for path, meta in after.items() if before.get(path) != meta
    )
    if changed:
        return changed
    return sorted(after)


def _cleanup_downloaded_markdown(
    output_dir: str, before: Dict[str, Tuple[int, int]]
) -> Tuple[bool, str]:
    candidates = _find_changed_markdown_files(before, output_dir)
    if not candidates:
        return True, ""

    cleaned_files, removed_blocks, errors = clean_markdown_paths(candidates)
    if errors:
        details = "; ".join(f"{path}: {message}" for path, message in errors)
        return False, details

    if cleaned_files or removed_blocks:
        print(
            f"post-processed {len(cleaned_files)} markdown file(s), "
            f"removed {removed_blocks} embedded image block(s)",
            file=sys.stderr,
        )
    return True, ""


def download_one(
    file_id: str, output_dir: str, export_format: str = "md", timeout: int = 120
) -> Tuple[bool, str]:
    """Run `gog drive download <id> --output <dir>`."""
    if not file_id or not output_dir:
        return False, "file_id or output_dir is empty"

    cmd = [
        "gog",
        "drive",
        "download",
        file_id.strip(),
        "--output",
        output_dir,
        "--format",
        export_format,
    ]

    before = _snapshot_markdown_files(output_dir)

    try:
        code, out, _ = _run_gog_with_pty(cmd, timeout=timeout)
        if code != 0:
            return False, out.strip() or f"exit code {code}"

        if export_format.lower() == "md":
            cleaned, cleanup_error = _cleanup_downloaded_markdown(output_dir, before)
            if not cleaned:
                return False, f"download succeeded but cleanup failed: {cleanup_error}"

        return True, ""
    except FileNotFoundError:
        return False, "gog command not found; install gog CLI first"
    except Exception as exc:
        return False, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download one Google Drive file ID into the target directory."
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        metavar="DIR",
        help="Target directory for the downloaded file.",
    )
    parser.add_argument(
        "--id",
        required=True,
        metavar="ID",
        help="Google Drive file ID to download.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        metavar="SEC",
        help="Download timeout in seconds. Default: 120.",
    )
    parser.add_argument(
        "--format",
        default="md",
        metavar="FMT",
        help="Google Docs export format. Default: md.",
    )
    args = parser.parse_args()

    output_dir = os.path.expanduser(args.output)
    if not os.path.isdir(output_dir):
        print(
            f"Error: output directory does not exist or is not a directory: {output_dir}",
            file=sys.stderr,
        )
        sys.exit(2)

    file_id = (args.id or "").strip()
    if not file_id:
        print("Error: missing file ID.", file=sys.stderr)
        sys.exit(2)

    export_format = (args.format or "md").strip() or "md"
    ok, err = download_one(file_id, output_dir, export_format=export_format, timeout=args.timeout)
    if ok:
        print(f"{file_id} downloaded successfully", file=sys.stderr)
        sys.exit(0)

    print(f"{file_id} failed: {err}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

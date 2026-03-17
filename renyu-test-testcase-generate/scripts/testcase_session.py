#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

DOC_EXTENSIONS = {
    ".doc",
    ".docx",
    ".md",
    ".pdf",
    ".ppt",
    ".pptx",
    ".rtf",
    ".txt",
    ".xls",
    ".xlsx",
}

POSITIVE_KEYWORDS = [
    "requirement",
    "requirements",
    "design",
    "spec",
    "prd",
    "api",
    "story",
    "userstory",
    "workflow",
    "architecture",
    "plan",
    "需求",
    "设计",
    "方案",
    "说明",
    "规格",
    "原型",
    "流程",
    "架构",
]

NEGATIVE_KEYWORDS = [
    "cache",
    "debug",
    "dist",
    "build",
    "tmp",
    "temp",
    "log",
]

GOOGLE_DOC_PATTERN = re.compile(r"/d/([^/]+)")


def print_json(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def get_default_downloads_dir() -> Path:
    home = Path.home()
    candidates: list[Path] = []

    env_candidates = [
        os.environ.get("CODEX_DOWNLOADS"),
        os.environ.get("DOWNLOADS"),
    ]
    for value in env_candidates:
        if value:
            candidates.append(Path(value).expanduser())

    if os.name == "nt":
        win_homes = [
            os.environ.get("USERPROFILE"),
            os.environ.get("HOMEDRIVE", "") + os.environ.get("HOMEPATH", ""),
            os.environ.get("OneDrive"),
        ]
        for value in win_homes:
            if value:
                base = Path(value).expanduser()
                candidates.append(base / "Downloads")
                candidates.append(base / "下载")
    else:
        candidates.append(home / "Downloads")
        candidates.append(home / "downloads")

    candidates.append(home / "Downloads")

    for candidate in candidates:
        if candidate and candidate.exists() and candidate.is_dir():
            return candidate.resolve()

    fallback = home / "Downloads"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback.resolve()


def resolve_existing_session(session_dir: str) -> tuple[Path, Path]:
    session_path = Path(session_dir).expanduser()
    temp_dir = session_path / "temp_inputs"
    if not session_path.exists() or not session_path.is_dir():
        raise FileNotFoundError(f"Session directory does not exist: {session_path}")
    if not temp_dir.exists() or not temp_dir.is_dir():
        raise FileNotFoundError(f"temp_inputs directory does not exist: {temp_dir}")
    return session_path.resolve(), temp_dir.resolve()


def unique_target(directory: Path, filename: str) -> Path:
    candidate = directory / filename
    if not candidate.exists():
        return candidate

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        candidate = directory / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size_bytes)
    unit = units[0]
    for unit in units:
        if value < 1024 or unit == units[-1]:
            break
        value /= 1024
    if unit == "B":
        return f"{int(value)} {unit}"
    return f"{value:.1f} {unit}"


def build_file_record(path: Path, relative_to: Path | None = None) -> dict[str, object]:
    stat = path.stat()
    relative_path = str(path.relative_to(relative_to)) if relative_to else path.name
    return {
        "name": path.name,
        "path": str(path.resolve()),
        "relative_path": relative_path,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "size_human": format_size(stat.st_size),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
    }


def score_file(path: Path) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    name = path.name.lower()
    extension = path.suffix.lower()

    if extension in DOC_EXTENSIONS:
        score += 3
        reasons.append(f"document extension {extension}")

    matched_positive = [keyword for keyword in POSITIVE_KEYWORDS if keyword in name]
    if matched_positive:
        score += 2 * len(matched_positive)
        reasons.append(f"name matches {', '.join(matched_positive[:4])}")

    matched_negative = [keyword for keyword in NEGATIVE_KEYWORDS if keyword in name]
    if matched_negative:
        score -= len(matched_negative)
        reasons.append(f"name suggests non-source file: {', '.join(matched_negative[:4])}")

    if extension in {".png", ".jpg", ".jpeg", ".gif", ".zip", ".exe", ".dll"}:
        score -= 2
        reasons.append(f"extension {extension} is usually not a primary testcase source")

    return score, reasons


def command_prepare_session(args: argparse.Namespace) -> int:
    downloads_dir = Path(args.downloads_dir).expanduser().resolve() if args.downloads_dir else get_default_downloads_dir()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    session_dir = downloads_dir / f"{args.prefix}-{timestamp}"
    temp_dir = session_dir / "temp_inputs"

    temp_dir.mkdir(parents=True, exist_ok=False)

    print_json(
        {
            "downloads_dir": str(downloads_dir),
            "session_dir": str(session_dir.resolve()),
            "temp_dir": str(temp_dir.resolve()),
        }
    )
    return 0


def command_stage_files(args: argparse.Namespace) -> int:
    try:
        session_dir, temp_dir = resolve_existing_session(args.session_dir)
    except FileNotFoundError as exc:
        return fail(str(exc))

    if not args.source:
        return fail("At least one --source file is required.")

    copied_files: list[dict[str, object]] = []
    for raw_source in args.source:
        source = Path(raw_source).expanduser()
        if not source.exists():
            return fail(f"Source file does not exist: {source}")
        if not source.is_file():
            return fail(f"Source path is not a file: {source}")

        target = unique_target(temp_dir, source.name)
        shutil.copy2(source, target)
        copied_files.append(
            {
                "source": str(source.resolve()),
                "copied_to": str(target.resolve()),
            }
        )

    print_json(
        {
            "session_dir": str(session_dir),
            "temp_dir": str(temp_dir),
            "copied_files": copied_files,
        }
    )
    return 0


def command_scan_dir(args: argparse.Namespace) -> int:
    source_dir = Path(args.source_dir).expanduser()
    if not source_dir.exists():
        return fail(f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        return fail(f"Source path is not a directory: {source_dir}")
    source_dir = source_dir.resolve()

    walker = source_dir.rglob("*") if args.recursive else source_dir.glob("*")
    files = sorted(path for path in walker if path.is_file())
    if not files:
        print_json(
            {
                "source_dir": str(source_dir.resolve()),
                "files": [],
                "recommendations": [],
            }
        )
        return 0

    file_records = [build_file_record(path, source_dir.resolve()) for path in files]
    ranked = []
    for path in files:
        score, reasons = score_file(path)
        ranked.append(
            {
                "path": str(path.resolve()),
                "relative_path": str(path.relative_to(source_dir)),
                "score": score,
                "reasons": reasons,
            }
        )
    ranked.sort(key=lambda item: (-int(item["score"]), str(item["relative_path"]).lower()))

    print_json(
        {
            "source_dir": str(source_dir.resolve()),
            "files": file_records,
            "recommendations": ranked[: args.limit],
        }
    )
    return 0


def command_parse_gdocs(args: argparse.Namespace) -> int:
    parsed_ids: list[dict[str, str]] = []
    invalid_urls: list[str] = []

    for url in args.url:
        match = GOOGLE_DOC_PATTERN.search(url)
        if not match:
            invalid_urls.append(url)
            continue
        parsed_ids.append({"url": url, "id": match.group(1)})

    print_json(
        {
            "parsed": parsed_ids,
            "invalid_urls": invalid_urls,
        }
    )
    return 0 if not invalid_urls else 1


def command_import_downloaded(args: argparse.Namespace) -> int:
    try:
        session_dir, temp_dir = resolve_existing_session(args.session_dir)
    except FileNotFoundError as exc:
        return fail(str(exc))

    source_dir = Path(args.source_dir).expanduser()
    if not source_dir.exists():
        return fail(f"Import source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        return fail(f"Import source is not a directory: {source_dir}")
    source_dir = source_dir.resolve()

    files = sorted(path for path in source_dir.rglob("*") if path.is_file())
    if not files:
        return fail(f"No files found to import from: {source_dir}")

    imported: list[dict[str, str]] = []
    for path in files:
        target = unique_target(temp_dir, path.name)
        shutil.copy2(path, target)
        imported.append(
            {
                "source": str(path.resolve()),
                "copied_to": str(target.resolve()),
            }
        )

    print_json(
        {
            "session_dir": str(session_dir),
            "temp_dir": str(temp_dir),
            "imported_files": imported,
        }
    )
    return 0


def command_summarize_session(args: argparse.Namespace) -> int:
    try:
        session_dir, temp_dir = resolve_existing_session(args.session_dir)
    except FileNotFoundError as exc:
        return fail(str(exc))

    files = sorted(path for path in temp_dir.rglob("*") if path.is_file())
    summary = [build_file_record(path, temp_dir) for path in files]
    total_bytes = sum(int(item["size_bytes"]) for item in summary)

    print_json(
        {
            "session_dir": str(session_dir),
            "temp_dir": str(temp_dir),
            "file_count": len(summary),
            "total_size_bytes": total_bytes,
            "total_size_human": format_size(total_bytes),
            "files": summary,
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare and summarize testcase input sessions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare-session", help="Create a timestamped testcase session directory.")
    prepare_parser.add_argument("--prefix", default="testcase-generate", help="Session directory prefix.")
    prepare_parser.add_argument("--downloads-dir", help="Override the detected Downloads directory.")
    prepare_parser.set_defaults(func=command_prepare_session)

    stage_parser = subparsers.add_parser("stage-files", help="Copy source files into temp_inputs.")
    stage_parser.add_argument("--session-dir", required=True, help="Existing testcase session directory.")
    stage_parser.add_argument("--source", action="append", required=True, help="Source file path. Repeat for multiple files.")
    stage_parser.set_defaults(func=command_stage_files)

    scan_parser = subparsers.add_parser("scan-dir", help="List files in a source directory and rank likely source documents.")
    scan_parser.add_argument("--source-dir", required=True, help="Directory to scan.")
    scan_parser.add_argument("--recursive", action="store_true", default=True, help="Scan subdirectories recursively.")
    scan_parser.add_argument("--limit", type=int, default=10, help="Maximum number of ranked recommendations to return.")
    scan_parser.set_defaults(func=command_scan_dir)

    parse_parser = subparsers.add_parser("parse-gdocs", help="Extract Google Doc IDs from URLs.")
    parse_parser.add_argument("--url", action="append", required=True, help="Google Doc URL. Repeat for multiple URLs.")
    parse_parser.set_defaults(func=command_parse_gdocs)

    import_parser = subparsers.add_parser("import-downloaded", help="Copy downloaded files into temp_inputs.")
    import_parser.add_argument("--session-dir", required=True, help="Existing testcase session directory.")
    import_parser.add_argument("--source-dir", required=True, help="Directory containing files to import.")
    import_parser.set_defaults(func=command_import_downloaded)

    summarize_parser = subparsers.add_parser("summarize-session", help="Summarize files currently staged in temp_inputs.")
    summarize_parser.add_argument("--session-dir", required=True, help="Existing testcase session directory.")
    summarize_parser.set_defaults(func=command_summarize_session)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

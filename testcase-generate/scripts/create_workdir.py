#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

INPUT_MANIFEST_TEMPLATE = {
    "google doc url": [],
    "uploaded files by agent": [],
    "user file directory": [],
}


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
        config = home / ".config" / "user-dirs.dirs"
        if config.exists():
            for line in config.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line.startswith("XDG_DOWNLOAD_DIR="):
                    raw_value = line.split("=", 1)[1].strip().strip('"')
                    candidates.append(Path(raw_value.replace("$HOME", str(home))).expanduser())
        candidates.append(home / "Downloads")
        candidates.append(home / "downloads")

    candidates.append(home / "Downloads")

    for candidate in candidates:
        if candidate and candidate.exists() and candidate.is_dir():
            return candidate.resolve()

    fallback = home / "Downloads"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a testcase-generate intake work directory.",
    )
    parser.add_argument("--downloads-dir", help="Override the detected Downloads directory.")
    parser.add_argument("--prefix", default="testcase-generate", help="Working directory prefix.")
    args = parser.parse_args()

    downloads_dir = (
        Path(args.downloads_dir).expanduser().resolve()
        if args.downloads_dir
        else get_default_downloads_dir()
    )
    downloads_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    workdir = (downloads_dir / f"{args.prefix}-{timestamp}").resolve()
    workdir.mkdir(parents=True, exist_ok=False)

    input_manifest = workdir / "input-manifest.json"
    input_manifest.write_text(
        json.dumps(INPUT_MANIFEST_TEMPLATE, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "downloads_dir": str(downloads_dir),
                "workdir": str(workdir),
                "input_manifest": str(input_manifest),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

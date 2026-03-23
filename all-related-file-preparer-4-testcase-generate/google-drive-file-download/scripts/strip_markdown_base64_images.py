#!/usr/bin/env python3
"""
Strip embedded base64 image reference blocks from markdown files.

This targets gog markdown exports such as:
    [image1]: <data:image/png;base64,...>
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

EMBEDDED_IMAGE_PATTERN = re.compile(
    r"(?ms)^[ \t]*\[image\d+\]:[ \t]*<data:image/[^>]*?;base64,[^>]*?>[ \t]*(?:\r?\n)?"
)


def strip_embedded_images(text: str) -> Tuple[str, int]:
    removed = len(EMBEDDED_IMAGE_PATTERN.findall(text))
    if removed == 0:
        return text, 0
    return EMBEDDED_IMAGE_PATTERN.sub("", text), removed


def _iter_markdown_files(paths: Sequence[str]) -> Iterable[Path]:
    seen = set()
    for raw_path in paths:
        path = Path(raw_path).expanduser().resolve()
        if path.is_dir():
            candidates = sorted(
                child
                for child in path.rglob("*")
                if child.is_file() and child.suffix.lower() in {".md", ".markdown"}
            )
        else:
            candidates = [path]

        for candidate in candidates:
            if candidate.suffix.lower() not in {".md", ".markdown"}:
                continue
            key = str(candidate)
            if key in seen:
                continue
            seen.add(key)
            yield candidate


def clean_markdown_paths(paths: Sequence[str]) -> Tuple[List[str], int, List[Tuple[str, str]]]:
    cleaned_files: List[str] = []
    removed_blocks = 0
    errors: List[Tuple[str, str]] = []

    for path in _iter_markdown_files(paths):
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
            stripped, removed = strip_embedded_images(original)
            if removed == 0:
                continue
            path.write_text(stripped, encoding="utf-8", newline="")
            cleaned_files.append(str(path))
            removed_blocks += removed
        except Exception as exc:
            errors.append((str(path), str(exc)))

    return cleaned_files, removed_blocks, errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove embedded base64 image references from markdown files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Markdown file or directory path(s). Directories are scanned recursively.",
    )
    args = parser.parse_args()

    cleaned_files, removed_blocks, errors = clean_markdown_paths(args.paths)

    for path in cleaned_files:
        print(f"cleaned: {path}")

    if removed_blocks:
        print(
            f"removed {removed_blocks} embedded image block(s) from "
            f"{len(cleaned_files)} file(s)",
            file=sys.stderr,
        )

    if errors:
        for path, message in errors:
            print(f"error: {path}: {message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

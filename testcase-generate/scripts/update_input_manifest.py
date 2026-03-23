#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

MANIFEST_KEYS = [
    "google doc url",
    "uploaded files by agent",
    "user file directory",
]

MARKDOWN_SUFFIXES = {".md", ".markdown"}


def load_manifest(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise FileNotFoundError(f"input manifest not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("input manifest must be a JSON object")
    for key in MANIFEST_KEYS:
        value = data.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"input manifest field must be a list: {key}")
        data[key] = value
    return data


def normalize_uploaded_markdown(path_str: str) -> str:
    path = Path(path_str).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"uploaded markdown file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"uploaded markdown path is not a file: {path}")
    if path.suffix.lower() not in MARKDOWN_SUFFIXES:
        raise ValueError(f"uploaded markdown must end with .md or .markdown: {path}")
    return str(path.resolve())


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update testcase-generate input-manifest.json after Google Docs fallback handling.",
    )
    parser.add_argument("--manifest", required=True, help="Path to input-manifest.json")
    parser.add_argument(
        "--remove-google-doc-url",
        action="append",
        default=[],
        help="A failed Google Docs URL to remove from the manifest. Repeat for multiple URLs.",
    )
    parser.add_argument(
        "--add-uploaded-file",
        action="append",
        default=[],
        help="A manually uploaded Markdown file path to add into uploaded files by agent. Repeat for multiple files.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    data = load_manifest(manifest_path)

    removed_urls: list[str] = []
    missing_urls: list[str] = []
    google_doc_urls = [str(item) for item in data["google doc url"]]
    for url in args.remove_google_doc_url:
        if url in google_doc_urls:
            google_doc_urls = [item for item in google_doc_urls if item != url]
            removed_urls.append(url)
        else:
            missing_urls.append(url)
    data["google doc url"] = google_doc_urls

    added_uploaded_files = [
        normalize_uploaded_markdown(path_str)
        for path_str in args.add_uploaded_file
    ]
    existing_uploaded_files = [str(item) for item in data["uploaded files by agent"]]
    data["uploaded files by agent"] = dedupe_keep_order(
        existing_uploaded_files + added_uploaded_files
    )

    manifest_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "removed_google_doc_urls": removed_urls,
                "google_doc_urls_not_found": missing_urls,
                "added_uploaded_files": added_uploaded_files,
                "google_doc_url_count": len(data["google doc url"]),
                "uploaded_files_count": len(data["uploaded files by agent"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

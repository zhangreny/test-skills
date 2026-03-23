#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

MANIFEST_HEADER = """# Full Read Manifest

| step | round | source_type | path | scope | why_read |
| --- | --- | --- | --- | --- | --- |
"""


def escape_cell(value: object) -> str:
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    return text.replace("|", "\\|")


def ensure_manifest(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(MANIFEST_HEADER, encoding="utf-8")


def load_entries(args: argparse.Namespace) -> list[dict[str, object]]:
    if args.entry:
        return [json.loads(raw) for raw in args.entry]
    return [
        {
            "step": args.step,
            "round": args.round,
            "source_type": args.source_type,
            "path": args.path,
            "scope": args.scope,
            "why_read": args.why_read,
        }
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Append rows to full_read_manifest.md.")
    parser.add_argument("--manifest", required=True, help="Path to full_read_manifest.md.")
    parser.add_argument(
        "--entry",
        action="append",
        help="JSON entry with step, round, source_type, path, scope, why_read. Repeat for multiple rows.",
    )
    parser.add_argument("--step", help="Step number for single-row mode.")
    parser.add_argument("--round", help="Round name for single-row mode.")
    parser.add_argument("--source-type", dest="source_type", help="Source type for single-row mode.")
    parser.add_argument("--path", help="Source path for single-row mode.")
    parser.add_argument("--scope", help="Read scope for single-row mode.")
    parser.add_argument("--why-read", dest="why_read", help="Reason for reading for single-row mode.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    ensure_manifest(manifest_path)
    entries = load_entries(args)

    required_keys = ["step", "round", "source_type", "path", "scope", "why_read"]
    rows: list[str] = []
    for entry in entries:
        missing = [key for key in required_keys if not entry.get(key)]
        if missing:
            raise SystemExit(f"Missing manifest fields: {', '.join(missing)}")
        cells = [escape_cell(entry[key]) for key in required_keys]
        rows.append(f"| {' | '.join(cells)} |")

    with manifest_path.open("a", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(row + "\n")

    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "appended_rows": len(rows),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def default_parser_path() -> Path:
    skills_dir = Path(__file__).resolve().parents[2]
    parser_path = skills_dir / "testrail-testcase-extract-upload" / "scripts" / "parse_testrail_template.py"
    if not parser_path.is_file():
        raise FileNotFoundError(f"Parser script not found: {parser_path}")
    return parser_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one or more TestRail-style testcase markdown files.")
    parser.add_argument("--source", action="append", required=True, help="Absolute path to a testcase markdown file.")
    parser.add_argument("--parser", dest="parser_path", help="Override parse_testrail_template.py path.")
    parser.add_argument("--pretty", action="store_true", help="Pass --pretty through to the parser.")
    args = parser.parse_args()

    parser_path = Path(args.parser_path).expanduser().resolve() if args.parser_path else default_parser_path()

    results: list[dict[str, object]] = []
    exit_code = 0
    for raw_source in args.source:
        source = Path(raw_source).expanduser().resolve()
        command = [sys.executable, str(parser_path), "--source", str(source)]
        if args.pretty:
            command.append("--pretty")
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        results.append(
            {
                "source": str(source),
                "ok": completed.returncode == 0,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
        if completed.returncode != 0:
            exit_code = 1

    print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

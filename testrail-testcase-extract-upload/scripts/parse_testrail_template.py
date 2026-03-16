#!/usr/bin/env python3
"""Parse TestRail-style markdown testcase documents into a nested JSON tree."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def testrail_default_template_to_json(text: str) -> list[dict]:
    """Convert markdown testcase text to a nested JSON structure."""
    lines = text.replace("\r\n", "\n").split("\n")
    root = {"number": "", "title": "root", "description": "", "children": []}
    stack = [root]
    i = 0

    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue

        if stripped.startswith("## ") and not stripped.startswith("### "):
            num, title = _parse_number_title(stripped[3:])
            node = {"number": num or "", "title": title, "description": "", "children": []}
            root["children"].append(node)
            stack = [root, node]
            i = _consume_description(lines, i + 1, node)
            continue

        if stripped.startswith("### ") and not stripped.startswith("#### "):
            num, title = _parse_number_title(stripped[4:])
            node = {"number": num or "", "title": title, "description": "", "children": []}
            parent = stack[1] if len(stack) >= 2 else root
            parent["children"].append(node)
            stack = [root, stack[1], node] if len(stack) >= 2 else [root, node]
            i = _consume_description(lines, i + 1, node)
            continue

        if stripped.startswith("#### "):
            num, title = _parse_number_title(stripped[5:])
            node = {"number": num or "", "title": title, "description": "", "steps": []}
            parent = stack[2] if len(stack) >= 3 else (stack[1] if len(stack) >= 2 else root)
            if "children" not in parent:
                parent["children"] = []
            parent["children"].append(node)
            i = _consume_description(lines, i + 1, node)
            while i < len(lines):
                step_line = lines[i].strip()
                if step_line.startswith("#"):
                    break
                step_match = re.match(r"^【Step\s*(\d+)】\s*(.*)$", step_line)
                if step_match:
                    node["steps"].append(step_match.group(2).strip())
                i += 1
            continue

        i += 1

    return _serialize_children(root.get("children") or [])


def _consume_description(lines: list[str], start: int, node: dict) -> int:
    i = start
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and re.match(r"^描述[：:]\s*", lines[i].strip()):
        node["description"] = re.sub(r"^描述[：:]\s*", "", lines[i].strip())
        i += 1
    return i


def _parse_number_title(line: str) -> tuple[str | None, str]:
    match = re.match(r"^(\d+(?:\.\d+)*)\s+(.+)$", line.strip())
    return (match.group(1), match.group(2).strip()) if match else (None, line.strip())


def _serialize_children(children: list[dict]) -> list[dict]:
    return [
        {
            "number": node.get("number", ""),
            "title": node.get("title", ""),
            "description": node.get("description", ""),
            **({"steps": node["steps"]} if node.get("steps") is not None else {}),
            **({"children": _serialize_children(node["children"])} if node.get("children") else {}),
        }
        for node in children
    ]


def _absolute_markdown_path(source: str) -> Path:
    path = Path(source)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("`--source` must be an absolute path to a markdown testcase file.")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"Source file does not exist: {path}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse TestRail-style markdown testcase documents.")
    parser.add_argument(
        "--source",
        type=_absolute_markdown_path,
        required=True,
        help="Absolute path to the markdown testcase file.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    result = testrail_default_template_to_json(text)
    indent = 2 if args.pretty else None
    print(json.dumps(result, ensure_ascii=False, indent=indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

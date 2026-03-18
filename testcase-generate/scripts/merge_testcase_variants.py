#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Origin:
    source_file: str
    source_path: str
    action: str
    deduplicated_with_uid: str | None = None
    split_further_reason: str = ""


@dataclass
class Node:
    uid: str
    title: str
    description: str = ""
    steps: list[str] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)
    origins: list[Origin] = field(default_factory=list)
    merged_path: str = ""

    @property
    def is_leaf(self) -> bool:
        return bool(self.steps)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def parse_numbered_title(raw: str) -> str:
    match = re.match(r"^\d+(?:\.\d+)*\s+(.+)$", raw.strip())
    return match.group(1).strip() if match else raw.strip()


def parse_markdown(path: Path, source_label: str) -> list[Node]:
    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    root = Node(uid=f"{source_label}::root", title="root")
    stack: list[tuple[int, Node]] = [(1, root)]
    node_counter = 0
    i = 0

    while i < len(lines):
        stripped = lines[i].lstrip("\ufeff").strip()
        if not stripped:
            i += 1
            continue

        heading_match = re.match(r"^(#{2,6})\s+(.+)$", stripped)
        if not heading_match:
            i += 1
            continue

        level = len(heading_match.group(1))
        title = parse_numbered_title(heading_match.group(2))
        node_counter += 1
        node = Node(uid=f"{source_label}::{node_counter}", title=title)

        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and re.match(r"^描述[：:]\s*", lines[j].strip()):
            node.description = re.sub(r"^描述[：:]\s*", "", lines[j].strip())
            j += 1

        steps: list[str] = []
        while j < len(lines):
            candidate = lines[j].strip()
            if re.match(r"^#{2,6}\s+", candidate):
                break
            step_match = re.match(r"^【Step\s*(\d+)】\s*(.*)$", candidate)
            if step_match:
                steps.append(step_match.group(2).strip())
            j += 1
        node.steps = steps

        while stack and stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1][1] if stack else root
        parent.children.append(node)
        if not node.is_leaf:
            stack.append((level, node))

        i = j

    annotate_origins(root.children, source_label)
    return root.children


def annotate_origins(nodes: list[Node], source_file: str, path: list[str] | None = None) -> None:
    current_path = path or []
    for node in nodes:
        source_path = " / ".join([*current_path, node.title])
        node.origins = [Origin(source_file=source_file, source_path=source_path, action="kept")]
        if node.children:
            annotate_origins(node.children, source_file, [*current_path, node.title])


def leaf_signature(node: Node) -> tuple[str, str, tuple[str, ...]]:
    return (
        normalize_text(node.title),
        normalize_text(node.description),
        tuple(normalize_text(step) for step in node.steps),
    )


def find_matching_branch(nodes: list[Node], incoming: Node) -> Node | None:
    for node in nodes:
        if not node.is_leaf and normalize_text(node.title) == normalize_text(incoming.title):
            return node
    return None


def find_duplicate_leaf(nodes: list[Node], incoming: Node) -> Node | None:
    signature = leaf_signature(incoming)
    for node in nodes:
        if node.is_leaf and leaf_signature(node) == signature:
            return node
    return None


def sibling_has_same_leaf_title(nodes: list[Node], incoming: Node) -> bool:
    incoming_title = normalize_text(incoming.title)
    return any(node.is_leaf and normalize_text(node.title) == incoming_title for node in nodes)


def merge_children(target_nodes: list[Node], incoming_nodes: list[Node]) -> None:
    for incoming in incoming_nodes:
        if incoming.is_leaf:
            duplicate = find_duplicate_leaf(target_nodes, incoming)
            if duplicate:
                for origin in incoming.origins:
                    duplicate.origins.append(
                        Origin(
                            source_file=origin.source_file,
                            source_path=origin.source_path,
                            action="deduped",
                            deduplicated_with_uid=duplicate.uid,
                        )
                    )
                continue

            copied = deepcopy(incoming)
            if sibling_has_same_leaf_title(target_nodes, incoming):
                for origin in copied.origins:
                    origin.action = "kept-distinct"
                    origin.split_further_reason = "same title but different description or steps"
            target_nodes.append(copied)
            continue

        branch = find_matching_branch(target_nodes, incoming)
        if branch:
            for origin in incoming.origins:
                branch.origins.append(
                    Origin(
                        source_file=origin.source_file,
                        source_path=origin.source_path,
                        action="merged-branch",
                    )
                )
            if not branch.description and incoming.description:
                branch.description = incoming.description
            merge_children(branch.children, incoming.children)
            continue

        target_nodes.append(deepcopy(incoming))


def number_nodes(nodes: list[Node], prefix: list[int] | None = None) -> None:
    base_prefix = prefix or []
    for index, node in enumerate(nodes, start=1):
        current_prefix = [*base_prefix, index]
        number = ".".join(str(item) for item in current_prefix)
        node.merged_path = f"{number} {node.title}".strip()
        if node.children:
            number_nodes(node.children, current_prefix)


def render_nodes(nodes: list[Node], depth: int = 0) -> str:
    rendered: list[str] = []
    for index, node in enumerate(nodes, start=1):
        number = ".".join(node.merged_path.split(" ", 1)[0].split("."))
        title = node.merged_path.split(" ", 1)[1] if " " in node.merged_path else node.title
        heading_level = min(2 + depth, 6)
        rendered.append(f"{'#' * heading_level} {number} {title}".rstrip())
        rendered.append("")
        rendered.append(f"描述：{node.description}")
        rendered.append("")
        if node.is_leaf:
            for step_index, step in enumerate(node.steps, start=1):
                rendered.append(f"【Step{step_index}】{step}")
            rendered.append("")
            continue
        rendered.append(render_nodes(node.children, depth + 1).rstrip())
        rendered.append("")
    return "\n".join(line for line in rendered if line is not None)


def collect_uid_map(nodes: list[Node], uid_map: dict[str, str] | None = None) -> dict[str, str]:
    mapping = uid_map or {}
    for node in nodes:
        mapping[node.uid] = node.merged_path
        if node.children:
            collect_uid_map(node.children, mapping)
    return mapping


def collect_merge_map(nodes: list[Node], uid_map: dict[str, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for node in nodes:
        for origin in node.origins:
            rows.append(
                {
                    "source_file": origin.source_file,
                    "source_path": origin.source_path,
                    "merged_section": node.merged_path,
                    "kept_as_is": "yes" if origin.action in {"kept", "kept-distinct"} else "no",
                    "deduplicated_with": uid_map.get(origin.deduplicated_with_uid or "", ""),
                    "split_further_reason": origin.split_further_reason,
                    "action": origin.action,
                }
            )
        if node.children:
            rows.extend(collect_merge_map(node.children, uid_map))
    return rows


def write_merge_map(path: Path, rows: list[dict[str, str]]) -> None:
    header = (
        "# Final Merge Map\n\n"
        "| source_file | source_path | merged_section | kept_as_is | deduplicated_with | split_further_reason | action |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
    )
    lines = [header]
    for row in rows:
        cells = [
            row["source_file"],
            row["source_path"],
            row["merged_section"],
            row["kept_as_is"],
            row["deduplicated_with"],
            row["split_further_reason"],
            row["action"],
        ]
        escaped = [cell.replace("|", "\\|") for cell in cells]
        lines.append(f"| {' | '.join(escaped)} |\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge testcase baseline and delta markdown files.")
    parser.add_argument("--base", required=True, help="Absolute path to the baseline testcase markdown file.")
    parser.add_argument("--delta", action="append", default=[], help="Absolute path to a delta testcase markdown file.")
    parser.add_argument("--output", required=True, help="Absolute path for merged markdown output.")
    parser.add_argument("--map-output", required=True, help="Absolute path for merge map markdown output.")
    args = parser.parse_args()

    base_path = Path(args.base).expanduser().resolve()
    delta_paths = [Path(item).expanduser().resolve() for item in args.delta]
    output_path = Path(args.output).expanduser().resolve()
    map_output_path = Path(args.map_output).expanduser().resolve()

    merged_nodes = parse_markdown(base_path, base_path.name)
    for delta_path in delta_paths:
        merge_children(merged_nodes, parse_markdown(delta_path, delta_path.name))

    number_nodes(merged_nodes)
    uid_map = collect_uid_map(merged_nodes)
    merge_map = collect_merge_map(merged_nodes, uid_map)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_nodes(merged_nodes).rstrip() + "\n", encoding="utf-8")
    write_merge_map(map_output_path, merge_map)

    print(
        json.dumps(
            {
                "base": str(base_path),
                "delta_count": len(delta_paths),
                "output": str(output_path),
                "map_output": str(map_output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Parse a TestRail-style markdown testcase document and upload it under a suite or section."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from parse_testrail_template import testrail_default_template_to_json
from testrail_client import (
    DEFAULT_TESTRAIL_API_KEY,
    DEFAULT_TESTRAIL_USER,
    TestrailClient,
)


def _absolute_markdown_path(source: str) -> Path:
    path = Path(source)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("`--source` must be an absolute path to a markdown testcase file.")
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"Source file does not exist: {path}")
    return path


def _project_suite_ids(client: TestrailClient, project_id: int) -> set[int]:
    return {int(suite["id"]) for suite in client.get_suites(project_id)}


def resolve_upload_target(
    client: TestrailClient,
    project_id: int,
    target_id: int,
    suite_id: int | None = None,
) -> tuple[int, int, str]:
    """Resolve target metadata as (suite_id, parent_id, target_kind)."""
    project_suite_ids = _project_suite_ids(client, project_id)

    if suite_id is not None:
        if suite_id not in project_suite_ids:
            raise SystemExit(f"Provided suite {suite_id} does not belong to project {project_id}.")
        if target_id == suite_id:
            return suite_id, 0, "suite"

        section = client.get_section(target_id)
        target_suite_id = int(section["suite_id"])
        if target_suite_id != suite_id:
            raise SystemExit(
                f"Target section {target_id} belongs to suite {target_suite_id}, not the provided suite {suite_id}."
            )
        return suite_id, target_id, "section"

    try:
        section = client.get_section(target_id)
    except RuntimeError as section_error:
        if target_id in project_suite_ids:
            return target_id, 0, "suite"
        raise SystemExit(
            f"Could not resolve target {target_id} as a section or suite in project {project_id}: {section_error}"
        ) from section_error

    resolved_suite_id = int(section["suite_id"])
    if resolved_suite_id not in project_suite_ids:
        raise SystemExit(
            f"Target section {target_id} belongs to suite {resolved_suite_id}, which is not in project {project_id}."
        )
    return resolved_suite_id, target_id, "section"


def create_from_json_tree(
    client: TestrailClient,
    project_id: int,
    suite_id: int,
    parent_id: int,
    nodes: list[dict],
) -> dict:
    stats = {"sections": 0, "cases": 0}
    for node in nodes:
        name = f"{(node.get('number') or '').strip()} {(node.get('title') or '').strip()}".strip()
        if not name:
            name = node.get("title") or "Untitled"
        description = (node.get("description") or "").strip()
        if node.get("children"):
            new_section = client.add_section(
                project_id=project_id,
                suite_id=suite_id,
                name=name,
                parent_id=parent_id,
                description=description,
            )
            stats["sections"] += 1
            child_stats = create_from_json_tree(
                client,
                project_id=project_id,
                suite_id=suite_id,
                parent_id=int(new_section["id"]),
                nodes=node["children"],
            )
            stats["sections"] += child_stats["sections"]
            stats["cases"] += child_stats["cases"]
        elif node.get("steps") is not None:
            client.add_case(
                section_id=parent_id,
                title=name,
                steps=node.get("steps") or [],
                description=description,
            )
            stats["cases"] += 1
        else:
            client.add_section(
                project_id=project_id,
                suite_id=suite_id,
                name=name,
                parent_id=parent_id,
                description=description,
            )
            stats["sections"] += 1
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload a TestRail-style testcase markdown file to TestRail.")
    parser.add_argument(
        "--source",
        type=_absolute_markdown_path,
        required=True,
        help="Absolute path to the markdown testcase file.",
    )
    parser.add_argument("--url", required=True, help="TestRail base URL, e.g. http://testrail.smartx.com")
    parser.add_argument(
        "--user",
        default=DEFAULT_TESTRAIL_USER,
        help=f"TestRail username or email. Defaults to {DEFAULT_TESTRAIL_USER}.",
    )
    parser.add_argument(
        "--api-key",
        default=DEFAULT_TESTRAIL_API_KEY,
        help="TestRail API key or password. Defaults to the built-in SmartX credential.",
    )
    parser.add_argument("--project-id", type=int, required=True, help="Target TestRail project id.")
    parser.add_argument(
        "--suite-id",
        type=int,
        help="Optional owning suite id for the upload target. If omitted, the script resolves it from `--target-id`.",
    )
    parser.add_argument(
        "--target-id",
        type=int,
        required=True,
        help="Target section id, or the suite id itself when uploading to the suite root.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Parse only and print the upload plan.")
    args = parser.parse_args()

    content = args.source.read_text(encoding="utf-8")
    tree = testrail_default_template_to_json(content)
    if not tree:
        raise SystemExit("No valid testcase structure was parsed from the source document.")

    client = TestrailClient(base_url=args.url, user=args.user, api_key=args.api_key)
    resolved_suite_id, parent_id, target_kind = resolve_upload_target(
        client=client,
        project_id=args.project_id,
        target_id=args.target_id,
        suite_id=args.suite_id,
    )

    if args.dry_run:
        preview = {
            "project_id": args.project_id,
            "suite_id": resolved_suite_id,
            "target_id": args.target_id,
            "target_kind": target_kind,
            "resolved_parent_id": parent_id,
            "parsed_tree": tree,
        }
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return 0

    stats = create_from_json_tree(
        client=client,
        project_id=args.project_id,
        suite_id=resolved_suite_id,
        parent_id=parent_id,
        nodes=tree,
    )
    print(
        json.dumps(
            {
                "status": "ok",
                "project_id": args.project_id,
                "suite_id": resolved_suite_id,
                "target_id": args.target_id,
                "target_kind": target_kind,
                "resolved_parent_id": parent_id,
                "created_sections": stats["sections"],
                "created_cases": stats["cases"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

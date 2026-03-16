#!/usr/bin/env python3
"""List TestRail suites and section tree for a project."""

from __future__ import annotations

import argparse
import json

from testrail_client import (
    DEFAULT_TESTRAIL_API_KEY,
    DEFAULT_TESTRAIL_USER,
    TestrailClient,
    build_section_tree,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="List the TestRail suite/section tree for a project.")
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
    args = parser.parse_args()

    client = TestrailClient(base_url=args.url, user=args.user, api_key=args.api_key)
    suites = client.get_suites(args.project_id)
    result = []
    for suite in suites:
        suite_id = int(suite["id"])
        sections = client.get_sections(args.project_id, suite_id)
        result.append(
            {
                "id": suite_id,
                "name": suite.get("name") or "",
                "parent_id": None,
                "children": build_section_tree(sections),
            }
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

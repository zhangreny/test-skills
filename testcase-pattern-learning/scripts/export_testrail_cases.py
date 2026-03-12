#!/usr/bin/env python3
"""
导出 TestRail 所有项目近一年的 subsection + testcase，输出为 4 空格缩进的 md 文件。

输出格式：
<项目名>
    <suite/baseline 名>
        <section 名>
            <subsection 名>
                <用例标题>

用法：
    python scripts/export_testrail_cases.py
    python scripts/export_testrail_cases.py --output my_cases.md
    python scripts/export_testrail_cases.py --days 180          # 只看近 180 天新建的用例
    python scripts/export_testrail_cases.py --project-ids 23 45 # 只看指定项目

环境变量：
    TESTRAIL_URL
    TESTRAIL_USER
    TESTRAIL_KEY
"""

import argparse
import os
from pathlib import Path
import re
import time
from datetime import datetime, timezone

from requests.auth import HTTPBasicAuth
import requests


TESTRAIL_URL = os.environ.get("TESTRAIL_URL", "").strip()
TESTRAIL_USER = os.environ.get("TESTRAIL_USER", "").strip()
TESTRAIL_KEY = os.environ.get("TESTRAIL_KEY", "").strip()
INDENT = "    "  # 4 空格


def require_config() -> None:
    missing = [
        name
        for name, value in {
            "TESTRAIL_URL": TESTRAIL_URL,
            "TESTRAIL_USER": TESTRAIL_USER,
            "TESTRAIL_KEY": TESTRAIL_KEY,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(
            "缺少 TestRail 配置环境变量: " + ", ".join(missing)
        )


def safe_name(name: str) -> str:
    """将名称转成适合 Windows 路径的安全片段。"""
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", (name or "").strip())
    cleaned = cleaned.rstrip(". ")
    return cleaned or "unnamed"


def _get(path: str, params: dict | None = None) -> object:
    url = f"{TESTRAIL_URL}/index.php?/api/v2/{path}"
    if params:
        url += "&" + "&".join(f"{k}={v}" for k, v in params.items())
    resp = requests.get(
        url,
        auth=HTTPBasicAuth(TESTRAIL_USER, TESTRAIL_KEY),
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"TestRail 请求失败 [{resp.status_code}]: {resp.text[:300]}")
    return resp.json()


def get_projects() -> list[dict]:
    """获取所有可见项目，返回 [{id, name}, ...]。"""
    raw = _get("get_projects")
    items = raw.get("projects", raw) if isinstance(raw, dict) else raw
    return [{"id": p["id"], "name": p.get("name", "")} for p in (items or [])]


def get_suites(project_id: int) -> list[dict]:
    """获取项目下所有 suite（baseline），返回 [{id, name}, ...]。"""
    raw = _get(f"get_suites/{project_id}")
    items = raw if isinstance(raw, list) else []
    return [{"id": s["id"], "name": s.get("name", "")} for s in items]


def get_sections(project_id: int, suite_id: int) -> list[dict]:
    """获取 suite 下所有 section（扁平列表）。"""
    raw = _get(f"get_sections/{project_id}", {"suite_id": suite_id})
    items = raw if isinstance(raw, list) else []
    return [
        {"id": s["id"], "name": s.get("name", ""), "parent_id": s.get("parent_id")}
        for s in items
    ]


def get_cases(project_id: int, suite_id: int, created_after: int) -> list[dict]:
    """
    获取 suite 下近一年（created_after Unix 时间戳）新建的用例，支持分页。
    返回 [{id, title, section_id}, ...]。
    """
    cases, offset, limit = [], 0, 250
    while True:
        params = {
            "suite_id": suite_id,
            "limit": limit,
            "offset": offset,
            "created_after": created_after,
        }
        raw = _get(f"get_cases/{project_id}", params)
        chunk = raw.get("cases", raw) if isinstance(raw, dict) else raw
        if not isinstance(chunk, list) or not chunk:
            break
        for c in chunk:
            cases.append({
                "id": c.get("id"),
                "title": (c.get("title") or "").strip(),
                "section_id": c.get("section_id"),
            })
        if len(chunk) < limit:
            break
        offset += limit
    return cases


def build_section_tree(flat: list[dict]) -> list[dict]:
    """将扁平 section 列表转为树（children 列表），返回根节点列表。"""
    by_id = {s["id"]: {**s, "children": [], "testcases": []} for s in flat}
    roots = []
    for s in flat:
        node = by_id[s["id"]]
        pid = s.get("parent_id")
        if pid is not None and pid in by_id:
            by_id[pid]["children"].append(node)
        else:
            roots.append(node)
    return roots


def prune_tree(nodes: list[dict]) -> list[dict]:
    """
    剪枝：递归删除既没有用例、子节点也为空的 section。
    返回保留节点列表（原地修改 children）。
    """
    kept = []
    for node in nodes:
        node["children"] = prune_tree(node["children"])
        if node["testcases"] or node["children"]:
            kept.append(node)
    return kept


def render_tree(nodes: list[dict], depth: int, lines: list[str]) -> None:
    """递归写入 section 树的缩进文本行。"""
    for node in nodes:
        lines.append(INDENT * depth + node["name"])
        for case in node["testcases"]:
            lines.append(INDENT * (depth + 1) + case["title"])
        render_tree(node["children"], depth + 1, lines)


def write_suite_file(
    output_dir: str,
    project_id: int,
    project_name: str,
    suite_id: int,
    suite_name: str,
    tree: list[dict],
) -> Path:
    """按 项目目录/suite.md 的形式写出单个 suite。"""
    project_dir = Path(output_dir) / f"{project_id}_{safe_name(project_name)}"
    project_dir.mkdir(parents=True, exist_ok=True)

    suite_file = project_dir / f"{suite_id}_{safe_name(suite_name)}.md"
    suite_lines: list[str] = []
    render_tree(tree, depth=0, lines=suite_lines)
    suite_file.write_text("\n".join(suite_lines), encoding="utf-8")
    return suite_file


def export(
    days: int,
    project_ids: list[int] | None,
    output: str | None,
    output_dir: str | None,
) -> None:
    cutoff = int(time.time()) - days * 86400
    cutoff_dt = datetime.fromtimestamp(cutoff, tz=timezone.utc).strftime("%Y-%m-%d")
    print(f"近 {days} 天（{cutoff_dt} 至今）新建的用例，正在导出…\n")

    all_projects = get_projects()
    if project_ids:
        all_projects = [p for p in all_projects if p["id"] in project_ids]

    lines: list[str] = []
    written_files = 0

    for proj in all_projects:
        pid = proj["id"]
        pname = proj["name"]
        print(f"  项目: {pname} (id={pid})")

        try:
            suites = get_suites(pid)
        except Exception as e:
            print(f"    [WARN] 获取 suites 失败: {e}")
            continue

        proj_lines: list[str] = []

        for suite in suites:
            sid = suite["id"]
            sname = suite["name"]

            try:
                flat_sections = get_sections(pid, sid)
                cases = get_cases(pid, sid, cutoff)
            except Exception as e:
                print(f"    [WARN] suite '{sname}' 获取失败: {e}")
                continue

            if not cases:
                continue

            tree = build_section_tree(flat_sections)
            by_section: dict[int, list[dict]] = {}
            for c in cases:
                by_section.setdefault(c["section_id"], []).append(c)

            def attach(nodes: list[dict]) -> None:
                for n in nodes:
                    n["testcases"] = by_section.get(n["id"], [])
                    attach(n["children"])

            attach(tree)
            tree = prune_tree(tree)

            if not tree:
                continue

            suite_lines: list[str] = [INDENT + sname]
            render_tree(tree, depth=2, lines=suite_lines)
            proj_lines.extend(suite_lines)

            if output_dir:
                suite_file = write_suite_file(output_dir, pid, pname, sid, sname, tree)
                written_files += 1
                print(f"      -> 已写入 {suite_file}")

            print(f"    [OK] suite: {sname}  ({len(cases)} 条用例)")

        if proj_lines:
            lines.append(pname)
            lines.extend(proj_lines)
            lines.append("")

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"\n已写入 {output}（共 {len(lines)} 行）")

    if output_dir:
        print(f"已写入目录 {output_dir}（共 {written_files} 个 suite 文件）")


def main() -> None:
    require_config()
    parser = argparse.ArgumentParser(
        description="导出 TestRail 近 N 天新建的 subsection + testcase 到 md"
    )
    parser.add_argument(
        "--days", type=int, default=365,
        help="只导出近多少天新建的用例（默认 365）"
    )
    parser.add_argument(
        "--project-ids", type=int, nargs="+", metavar="ID",
        help="只导出指定项目 ID（默认导出全部）"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="可选：汇总输出文件路径，例如 testrail_export.md"
    )
    parser.add_argument(
        "--output-dir",
        default="testrail_cases_by_group",
        help="按 项目目录/suite.md 的方式拆分导出（默认 testrail_cases_by_group）"
    )
    args = parser.parse_args()
    export(
        days=args.days,
        project_ids=args.project_ids,
        output=args.output,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()

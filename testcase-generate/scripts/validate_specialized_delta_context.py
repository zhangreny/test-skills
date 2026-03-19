#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


STEP_CONFIG = {
    "9": {"slug": "border", "requires_fault_reference": False},
    "10": {"slug": "compatibility", "requires_fault_reference": False},
    "11": {"slug": "stress", "requires_fault_reference": False},
    "12": {"slug": "user_scenario", "requires_fault_reference": False},
    "13": {"slug": "upgrade", "requires_fault_reference": False},
    "14": {"slug": "scale", "requires_fault_reference": False},
    "15": {"slug": "fault", "requires_fault_reference": True},
}

REQUIRED_HEADERS = [
    "## 本轮输入清单",
    "## 历史近邻继承点",
    "## 当前缺口判断",
    "## 新增用例与依据映射",
    "## 收敛记录",
]

METRIC_PATTERNS = {
    "new_top_level_scenarios": re.compile(r"new_top_level_scenarios:\s*(\d+)"),
    "new_leaf_cases": re.compile(r"new_leaf_cases:\s*(\d+)"),
    "deduped_cases": re.compile(r"deduped_cases:\s*(\d+)"),
    "continue_or_stop_reason": re.compile(r"continue_or_stop_reason:\s*(.+)"),
}


def normalize_path(value: str) -> str:
    text = value.strip().strip("`").strip()
    return text.replace("\\", "/").rstrip("/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fault_reference_paths() -> set[str]:
    skill_dir = Path(__file__).resolve().parents[1]
    fault_dir = skill_dir / "references" / "fault"
    return {normalize_path(str(path.resolve())) for path in fault_dir.glob("*.csv")}


def ensure_file(path: Path, errors: list[str], label: str) -> None:
    if not path.is_file():
        errors.append(f"{label} 不存在: {path}")


def parse_markdown_table(section_text: str) -> list[dict[str, str]]:
    lines = [line.rstrip() for line in section_text.splitlines()]
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 3:
        return []

    header = [cell.strip() for cell in table_lines[0].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for raw_line in table_lines[2:]:
        cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def extract_section(text: str, title: str) -> str:
    start = text.find(title)
    if start == -1:
        return ""
    remainder = text[start + len(title) :]
    next_header_match = re.search(r"^##\s+", remainder, flags=re.MULTILINE)
    if next_header_match:
        return remainder[: next_header_match.start()].strip()
    return remainder.strip()


def extract_former_case_paths(text: str) -> set[str]:
    candidates = set()
    for match in re.findall(r"(?:\.\./|[A-Za-z]:/|/)[^\s`|]*former_cases[^\s`|]*", text):
        candidates.add(normalize_path(match))
    return candidates


def path_matches(path_value: str, candidates: set[str]) -> bool:
    normalized = normalize_path(path_value)
    return normalized in candidates


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Step 9-15 specialized delta evidence/context reports.")
    parser.add_argument("--step", required=True, choices=sorted(STEP_CONFIG), help="Specialized step number (9-15).")
    parser.add_argument("--round", required=True, help="Round number, such as 1 or 2.")
    parser.add_argument("--manifest", required=True, help="Path to working_dir/full_read_manifest.md")
    parser.add_argument("--former-case-selection", required=True, help="Path to working_dir/former_case_selection.md")
    parser.add_argument("--base-testcase", required=True, help="Path to working_dir/merged/testcase_basic_final.md")
    parser.add_argument("--report", required=True, help="Path to the specialized evidence report for this round.")
    parser.add_argument("--delta", required=True, help="Path to the delta testcase file for this round.")
    parser.add_argument("--previous-delta", help="Path to previous-round delta when round > 1.")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = Path(args.manifest).expanduser().resolve()
    former_case_selection_path = Path(args.former_case_selection).expanduser().resolve()
    base_testcase_path = Path(args.base_testcase).expanduser().resolve()
    report_path = Path(args.report).expanduser().resolve()
    delta_path = Path(args.delta).expanduser().resolve()
    previous_delta_path = Path(args.previous_delta).expanduser().resolve() if args.previous_delta else None

    ensure_file(manifest_path, errors, "full_read_manifest")
    ensure_file(former_case_selection_path, errors, "former_case_selection")
    ensure_file(base_testcase_path, errors, "base_testcase")
    ensure_file(report_path, errors, "evidence report")
    ensure_file(delta_path, errors, "delta")
    if previous_delta_path:
        ensure_file(previous_delta_path, errors, "previous delta")

    if errors:
        print(json.dumps({"ok": False, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 1

    report_text = read_text(report_path)
    delta_text = read_text(delta_path)
    manifest_entries = parse_markdown_table(read_text(manifest_path))
    former_case_paths = extract_former_case_paths(read_text(former_case_selection_path))

    expected_title = f"# Step {args.step} Round {args.round} Evidence"
    if expected_title not in report_text:
        errors.append(f"evidence report 缺少标题: {expected_title}")

    for header in REQUIRED_HEADERS:
        if header not in report_text:
            errors.append(f"evidence report 缺少必需章节: {header}")

    input_rows = parse_markdown_table(extract_section(report_text, "## 本轮输入清单"))
    mapping_rows = parse_markdown_table(extract_section(report_text, "## 新增用例与依据映射"))

    input_paths: set[str] = set()
    for row in input_rows:
        for key, value in row.items():
            if key.lower().strip() == "path" and value.strip():
                input_paths.add(normalize_path(value))

    if normalize_path(str(base_testcase_path)) not in input_paths:
        errors.append("本轮输入清单未列出 testcase_basic_final.md")

    if previous_delta_path and normalize_path(str(previous_delta_path)) not in input_paths:
        errors.append("本轮输入清单未列出上一轮 delta")

    manifest_paths_by_type: dict[str, set[str]] = {}
    manifest_fault_paths_this_round: set[str] = set()
    for entry in manifest_entries:
        source_type = entry.get("source_type", "").strip()
        path_value = entry.get("path", "").strip()
        if not source_type or not path_value:
            continue
        normalized_path = normalize_path(path_value)
        manifest_paths_by_type.setdefault(source_type, set()).add(normalized_path)
        if (
            source_type == "fault_reference"
            and entry.get("step", "").strip() == args.step
            and entry.get("round", "").strip() == args.round
        ):
            manifest_fault_paths_this_round.add(normalized_path)

    document_source_paths = set()
    for source_type in ("user_upload", "drive_doc", "product_doc"):
        document_source_paths.update(manifest_paths_by_type.get(source_type, set()))

    if document_source_paths and not any(path_matches(path_value, document_source_paths) for path_value in input_paths):
        errors.append("本轮输入清单没有引用任何 manifest 中已读过的用户/Drive/产品文档")

    if former_case_paths:
        if not any(path_matches(path_value, former_case_paths) for path_value in input_paths):
            errors.append("本轮输入清单没有列出 former_case_selection.md 中命中的实际历史样本路径")
    elif "former_case_selection.md" not in report_text:
        warnings.append("未从 former_case_selection.md 中解析到具体路径；请至少在报告正文中显式提到 former_case_selection.md")

    if STEP_CONFIG[args.step]["requires_fault_reference"]:
        normalized_report = report_text.replace("\\", "/")
        if "references/fault/" not in normalized_report and "| fault_reference |" not in report_text:
            errors.append("Step 15 evidence report 未列出任何 fault reference 文件")
        expected_fault_paths = fault_reference_paths()
        missing_fault_inputs = sorted(expected_fault_paths - input_paths)
        if missing_fault_inputs:
            errors.append(
                "Step 15 本轮输入清单未覆盖全部 fault csv: "
                + "；".join(missing_fault_inputs)
            )
        missing_fault_manifest = sorted(expected_fault_paths - manifest_fault_paths_this_round)
        if missing_fault_manifest:
            errors.append(
                "Step 15 当前 round 的 manifest 未记录全部 fault csv 读取: "
                + "；".join(missing_fault_manifest)
            )

    metrics: dict[str, object] = {}
    for key, pattern in METRIC_PATTERNS.items():
        match = pattern.search(report_text)
        if not match:
            errors.append(f"收敛记录缺少字段: {key}")
            continue
        metrics[key] = int(match.group(1)) if key != "continue_or_stop_reason" else match.group(1).strip()

    if not delta_text.strip():
        errors.append("delta 文件为空")

    new_leaf_cases = int(metrics.get("new_leaf_cases", 0)) if isinstance(metrics.get("new_leaf_cases"), int) else 0
    min_mapping_rows = min(3, new_leaf_cases) if new_leaf_cases > 0 else 0
    if len(mapping_rows) < min_mapping_rows:
        errors.append(f"新增用例与依据映射行数不足，期望至少 {min_mapping_rows} 行，实际 {len(mapping_rows)} 行")

    recognized_sources = set(input_paths) | former_case_paths | document_source_paths
    if STEP_CONFIG[args.step]["requires_fault_reference"]:
        recognized_sources |= fault_reference_paths()

    for row in mapping_rows:
        lowered = {key.lower().strip(): value for key, value in row.items()}
        scenario = lowered.get("scenario", "").strip()
        evidence_path = lowered.get("evidence_path", "").strip()
        evidence_kind = lowered.get("evidence_kind", "").strip()
        why_new = lowered.get("why_new", "").strip()
        if not all([scenario, evidence_path, evidence_kind, why_new]):
            errors.append("新增用例与依据映射存在空列，必须至少填写 scenario/evidence_path/evidence_kind/why_new")
            continue
        if recognized_sources and normalize_path(evidence_path) not in recognized_sources:
            errors.append(f"依据映射里的 evidence_path 未在本轮输入或已知来源中出现: {evidence_path}")

    print(
        json.dumps(
            {
                "ok": not errors,
                "step": args.step,
                "round": args.round,
                "report": str(report_path),
                "delta": str(delta_path),
                "input_rows": len(input_rows),
                "mapping_rows": len(mapping_rows),
                "metrics": metrics,
                "errors": errors,
                "warnings": warnings,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

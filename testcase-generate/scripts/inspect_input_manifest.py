#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SUPPORTED_SOURCE_SUFFIXES = {
    ".doc",
    ".docx",
    ".markdown",
    ".md",
    ".pdf",
    ".ppt",
    ".pptx",
    ".rtf",
    ".txt",
    ".xls",
    ".xlsx",
}

POSITIVE_KEYWORDS = [
    "requirement",
    "requirements",
    "design",
    "spec",
    "prd",
    "api",
    "story",
    "userstory",
    "workflow",
    "architecture",
    "plan",
    "需求",
    "设计",
    "方案",
    "说明",
    "规格",
    "原型",
    "流程",
    "架构",
]

NEGATIVE_KEYWORDS = [
    "cache",
    "debug",
    "dist",
    "build",
    "tmp",
    "temp",
    "log",
]

GOOGLE_DOC_PATTERN = re.compile(r"/d/([^/]+)")


def as_list(data: dict[str, object], key: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def build_file_record(path: Path, root: Path | None = None) -> dict[str, str]:
    resolved = path.resolve() if path.exists() else path.expanduser()
    record = {
        "path": str(resolved),
        "name": path.name,
        "suffix": path.suffix.lower(),
    }
    if root is not None and path.exists():
        record["relative_path"] = str(path.resolve().relative_to(root.resolve()))
    return record


def score_file(path: Path) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    name = path.name.lower()
    extension = path.suffix.lower()

    if extension in SUPPORTED_SOURCE_SUFFIXES:
        score += 3
        reasons.append(f"document extension {extension}")

    matched_positive = [keyword for keyword in POSITIVE_KEYWORDS if keyword in name]
    if matched_positive:
        score += 2 * len(matched_positive)
        reasons.append(f"name matches {', '.join(matched_positive[:4])}")

    matched_negative = [keyword for keyword in NEGATIVE_KEYWORDS if keyword in name]
    if matched_negative:
        score -= len(matched_negative)
        reasons.append(f"name suggests non-source file: {', '.join(matched_negative[:4])}")

    return score, reasons


def flatten_candidate_files(
    records: list[dict[str, object]],
    source_type: str,
) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    for record in records:
        origin = str(record.get("input", ""))
        for item in record.get("supported_files", []):
            if not isinstance(item, dict):
                continue
            candidates.append(
                {
                    "source_type": source_type,
                    "from_input": origin,
                    "path": str(item.get("path", "")),
                    "relative_path": str(item.get("relative_path", "")),
                    "name": str(item.get("name", "")),
                }
            )
    return candidates


def inspect_path(raw_path: str) -> dict[str, object]:
    path = Path(raw_path).expanduser()
    if path.exists():
        resolved_path = str(path.resolve())
    else:
        resolved_path = str(path)

    record: dict[str, object] = {
        "input": raw_path,
        "resolved_path": resolved_path,
        "kind": "missing",
        "exists": False,
        "supported_files": [],
        "recommended_files": [],
        "notes": [],
    }

    if path.is_dir():
        files = sorted(item for item in path.rglob("*") if item.is_file())
        supported_files = [
            build_file_record(item, root=path)
            for item in files
            if item.suffix.lower() in SUPPORTED_SOURCE_SUFFIXES
        ]
        ranked = []
        for item in files:
            if item.suffix.lower() not in SUPPORTED_SOURCE_SUFFIXES:
                continue
            score, reasons = score_file(item)
            ranked.append(
                {
                    "path": str(item.resolve()),
                    "relative_path": str(item.resolve().relative_to(path.resolve())),
                    "score": score,
                    "reasons": reasons,
                }
            )
        ranked.sort(key=lambda item: (-int(item["score"]), str(item["relative_path"]).lower()))
        record.update(
            {
                "kind": "directory",
                "exists": True,
                "supported_files": supported_files,
                "recommended_files": ranked[:10],
            }
        )
        if not supported_files:
            record["notes"] = ["Directory exists but no supported requirement-like files were found."]
        return record

    if path.is_file():
        record.update(
            {
                "kind": "file",
                "exists": True,
            }
        )
        if path.suffix.lower() in SUPPORTED_SOURCE_SUFFIXES:
            record["supported_files"] = [build_file_record(path)]
        else:
            record["notes"] = [f"Unsupported file suffix: {path.suffix.lower() or '(none)'}"]
        return record

    return record


def parse_google_docs(urls: list[str]) -> dict[str, object]:
    parsed: list[dict[str, str]] = []
    invalid: list[str] = []
    for url in urls:
        match = GOOGLE_DOC_PATTERN.search(url)
        if not match:
            invalid.append(url)
            continue
        parsed.append({"url": url, "id": match.group(1)})
    return {
        "urls": urls,
        "parsed": parsed,
        "invalid": invalid,
    }


def collect_blocking_issues(
    google_docs: dict[str, object],
    uploaded_records: list[dict[str, object]],
    local_records: list[dict[str, object]],
    candidate_files: list[dict[str, str]],
) -> list[str]:
    issues: list[str] = []

    for url in google_docs.get("invalid", []):
        issues.append(f"Invalid Google Docs URL: {url}")

    for label, records in (
        ("uploaded files by agent", uploaded_records),
        ("user file directory", local_records),
    ):
        for record in records:
            if not bool(record.get("exists")):
                issues.append(f"{label} path does not exist: {record.get('input', '')}")
                continue
            if record.get("kind") == "file" and not record.get("supported_files"):
                issues.append(f"{label} file is not a supported source document: {record.get('resolved_path', '')}")
            if record.get("kind") == "directory" and not record.get("supported_files"):
                issues.append(f"{label} directory has no supported source documents: {record.get('resolved_path', '')}")

    has_google_docs = bool(google_docs.get("parsed"))
    if not has_google_docs and not candidate_files:
        issues.append("No usable requirement inputs were found after manifest inspection.")

    return issues


def build_confirmation(
    blocking_issues: list[str],
    google_docs: dict[str, object],
    candidate_files: list[dict[str, str]],
) -> dict[str, object]:
    if blocking_issues:
        return {
            "status": "blocked",
            "title": "输入里有待修正项",
            "message": "请先修正无效链接、缺失路径或不支持的文件后，再重新执行输入确认。",
        }

    has_google_docs = bool(google_docs.get("parsed"))
    has_local_files = bool(candidate_files)
    if has_google_docs and not has_local_files:
        return {
            "status": "needs_confirmation",
            "title": "请确认 Google Docs 输入范围",
            "message": "已收到可解析的 Google Docs 链接。请确认这些链接都要纳入本次 testcase 生成；确认后再下载并继续分析。",
        }
    if has_local_files and not has_google_docs:
        return {
            "status": "needs_confirmation",
            "title": "请确认本地资料范围",
            "message": "已解析出本地资料。请确认哪些文件属于原始需求文档，哪些是补充资料；确认后再进入需求分析。",
        }
    return {
        "status": "needs_confirmation",
        "title": "请确认本轮纳入的资料",
        "message": "已解析出 Google Docs 与本地资料。请确认都要纳入本次 testcase 生成，并指出要排除或新增的文件。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect testcase-generate input manifest and summarize candidate inputs.",
    )
    parser.add_argument("input_manifest", help="Path to input-manifest.json")
    args = parser.parse_args()

    manifest_path = Path(args.input_manifest).expanduser()
    if not manifest_path.is_file():
        raise SystemExit(f"input manifest not found: {manifest_path}")

    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    google_docs = parse_google_docs(as_list(data, "google doc url"))
    uploaded_records = [inspect_path(item) for item in as_list(data, "uploaded files by agent")]
    local_records = [inspect_path(item) for item in as_list(data, "user file directory")]

    candidate_files = (
        flatten_candidate_files(uploaded_records, "uploaded_file")
        + flatten_candidate_files(local_records, "user_path")
    )
    blocking_issues = collect_blocking_issues(
        google_docs=google_docs,
        uploaded_records=uploaded_records,
        local_records=local_records,
        candidate_files=candidate_files,
    )
    confirmation = build_confirmation(
        blocking_issues=blocking_issues,
        google_docs=google_docs,
        candidate_files=candidate_files,
    )

    payload = {
        "input_manifest": str(manifest_path.resolve()),
        "google doc url": google_docs,
        "uploaded files by agent": uploaded_records,
        "user file directory": local_records,
        "candidate_requirement_files": candidate_files,
        "blocking_issues": blocking_issues,
        "confirmation": confirmation,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

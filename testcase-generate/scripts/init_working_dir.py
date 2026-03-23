#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

MODE_PRESETS = {
    "lite": {
        "required_steps": ["0", "1", "2", "3", "4", "8", "16", "17"],
        "optional_steps": ["5", "6", "7", "9", "10", "11", "12", "13", "14", "15"],
        "round_policy": {
            "step_8": {"default_rounds": 1, "max_rounds": 2},
            "step_9_to_15": {"default_rounds": 1, "max_rounds": 2},
            "step_17": {"default_rounds": 1, "max_rounds": 2},
        },
    },
    "standard": {
        "required_steps": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "16", "17"],
        "optional_steps": ["9", "10", "11", "12", "13", "14", "15"],
        "round_policy": {
            "step_8": {"default_rounds": 2, "max_rounds": 3},
            "step_9_to_15": {"default_rounds": 1, "max_rounds": 2},
            "step_17": {"default_rounds": 2, "max_rounds": 3},
        },
    },
    "deep": {
        "required_steps": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "16", "17"],
        "optional_steps": ["9", "10", "11", "12", "13", "14", "15"],
        "round_policy": {
            "step_8": {"default_rounds": 3, "max_rounds": 5},
            "step_9_to_15": {"default_rounds": 3, "max_rounds": 5},
            "step_17": {"default_rounds": 3, "max_rounds": 5},
        },
    },
}

MANIFEST_HEADER = """# Full Read Manifest

| step | round | source_type | path | scope | why_read |
| --- | --- | --- | --- | --- | --- |
"""


def get_default_downloads_dir() -> Path:
    home = Path.home()
    candidates: list[Path] = []

    env_candidates = [
        os.environ.get("CODEX_DOWNLOADS"),
        os.environ.get("DOWNLOADS"),
    ]
    for value in env_candidates:
        if value:
            candidates.append(Path(value).expanduser())

    if os.name == "nt":
        win_homes = [
            os.environ.get("USERPROFILE"),
            os.environ.get("HOMEDRIVE", "") + os.environ.get("HOMEPATH", ""),
            os.environ.get("OneDrive"),
        ]
        for value in win_homes:
            if value:
                base = Path(value).expanduser()
                candidates.append(base / "Downloads")
                candidates.append(base / "下载")
    else:
        config = home / ".config" / "user-dirs.dirs"
        if config.exists():
            for line in config.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if line.startswith("XDG_DOWNLOAD_DIR="):
                    raw_value = line.split("=", 1)[1].strip().strip('"')
                    candidates.append(Path(raw_value.replace("$HOME", str(home))).expanduser())
        candidates.append(home / "Downloads")
        candidates.append(home / "downloads")

    candidates.append(home / "Downloads")

    for candidate in candidates:
        if candidate and candidate.exists() and candidate.is_dir():
            return candidate.resolve()

    fallback = home / "Downloads"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback.resolve()


def resolve_parent_dir(output_dir: str | None) -> Path:
    if output_dir:
        parent = Path(output_dir).expanduser().resolve()
        parent.mkdir(parents=True, exist_ok=True)
        return parent
    return get_default_downloads_dir()


def resolve_working_dir(existing_workdir: str | None, output_dir: str | None, prefix: str) -> Path:
    if existing_workdir:
        working_dir = Path(existing_workdir).expanduser().resolve()
        if not working_dir.exists() or not working_dir.is_dir():
            raise FileNotFoundError(f"Existing working directory does not exist: {working_dir}")
        return working_dir

    parent_dir = resolve_parent_dir(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return (parent_dir / f"{prefix}-{timestamp}").resolve()


def build_workflow_state(mode: str, working_dir: Path) -> dict[str, object]:
    preset = MODE_PRESETS[mode]
    return {
        "mode": mode,
        "required_steps": preset["required_steps"],
        "optional_steps": preset["optional_steps"],
        "round_policy": preset["round_policy"],
        "convergence_rules": {
            "stop_when": [
                "Two consecutive rounds add zero new一级场景 and zero net-new leaf cases.",
                "The current round adds fewer than 3 net-new leaf cases and no unresolved blocker remains.",
                "The current mode has reached the configured max_rounds for this step.",
            ],
            "continue_when": [
                "A new一级场景 appears in the current round.",
                "The current round adds at least 3 net-new leaf cases.",
                "An unresolved blocker still needs another pass to close.",
            ],
        },
        "directories": {
            "working_dir": str(working_dir),
            "baseline_dir": str((working_dir / "baseline").resolve()),
            "delta_dir": str((working_dir / "delta").resolve()),
            "merged_dir": str((working_dir / "merged").resolve()),
            "reports_dir": str((working_dir / "reports").resolve()),
            "manifest": str((working_dir / "full_read_manifest.md").resolve()),
            "input_manifest": str((working_dir / "input-manifest.json").resolve()),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a testcase-generate working directory.")
    parser.add_argument("--mode", choices=sorted(MODE_PRESETS), default="standard", help="Workflow mode preset.")
    parser.add_argument(
        "--existing-workdir",
        help="Reuse an intake work directory that was already created earlier.",
    )
    parser.add_argument(
        "--output-dir",
        help="Optional parent directory for a newly generated working directory. Defaults to the OS Downloads directory.",
    )
    parser.add_argument("--prefix", default="testcase-generate", help="Working directory prefix.")
    args = parser.parse_args()

    if args.existing_workdir and args.output_dir:
        raise SystemExit("--existing-workdir and --output-dir cannot be used together.")

    working_dir = resolve_working_dir(
        existing_workdir=args.existing_workdir,
        output_dir=args.output_dir,
        prefix=args.prefix,
    )
    if not args.existing_workdir:
        working_dir.mkdir(parents=True, exist_ok=False)

    for relative_dir in ("baseline", "delta", "merged", "reports"):
        (working_dir / relative_dir).mkdir(parents=True, exist_ok=False)

    manifest_path = working_dir / "full_read_manifest.md"
    manifest_path.write_text(MANIFEST_HEADER, encoding="utf-8")

    workflow_state = build_workflow_state(args.mode, working_dir)
    workflow_state_path = working_dir / "workflow_state.json"
    workflow_state_path.write_text(
        json.dumps(workflow_state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "working_dir": str(working_dir),
                "mode": args.mode,
                "workflow_state": str(workflow_state_path),
                "manifest": str(manifest_path),
                "baseline_dir": str((working_dir / "baseline").resolve()),
                "delta_dir": str((working_dir / "delta").resolve()),
                "merged_dir": str((working_dir / "merged").resolve()),
                "reports_dir": str((working_dir / "reports").resolve()),
                "input_manifest": str((working_dir / "input-manifest.json").resolve()),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

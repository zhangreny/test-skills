#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
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


def resolve_parent_dir(output_dir: str | None) -> Path:
    if output_dir:
        parent = Path(output_dir).expanduser().resolve()
        parent.mkdir(parents=True, exist_ok=True)
        return parent
    return Path(tempfile.gettempdir()).resolve()


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
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a testcase-generate working directory.")
    parser.add_argument("--mode", choices=sorted(MODE_PRESETS), default="standard", help="Workflow mode preset.")
    parser.add_argument("--output-dir", help="Optional parent directory for the generated working directory.")
    parser.add_argument("--prefix", default=".codex-testcase-generate", help="Working directory prefix.")
    args = parser.parse_args()

    parent_dir = resolve_parent_dir(args.output_dir)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    working_dir = (parent_dir / f"{args.prefix}-{timestamp}").resolve()

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
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

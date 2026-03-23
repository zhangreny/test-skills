---
name: smartx-docs-download
description: Use when SmartX internal documentation needs to be crawled, refreshed, or searched locally. This skill builds a docs index from internal-docs.smartx.com, exports documents to local Markdown, and helps other skills read the generated corpus from markdown_docs/ on demand.
---

# SmartX Docs Download

## Quick Start

Use this skill when the task is about SmartX internal docs as a local knowledge source instead of a one-off web browse.

Prefer this order:
1. If `markdown_docs/` already contains the needed documents, search and read those files directly.
2. If the local export is missing, stale, or incomplete, rebuild the index and re-export the docs with the bundled scripts.
3. Read only the specific exported Markdown files needed for the current task.

## Use When

Use this skill when the user wants to:
1. Batch export SmartX internal docs to local Markdown.
2. Refresh an existing local docs corpus from `internal-docs.smartx.com`.
3. Find product guides, release notes, whitepapers, CLI references, or terminology docs in `markdown_docs/`.
4. Let another skill consume SmartX supplemental documentation from a local folder instead of browsing live pages.

## Do Not Use When

Do not use this skill when:
1. The task is unrelated to SmartX internal documentation.
2. The user already provided the exact local Markdown files and no refresh is needed.
3. A normal website lookup is enough and no local export or repeatable corpus is required.

## Workflow

1. Confirm whether the task needs existing local docs or a fresh export.
2. If local docs already exist, search `markdown_docs/` first with focused filename or content queries before opening files.
3. If export is needed, follow `references/workflow.md` to:
   - install dependencies
   - run `scripts/crawl_doc_index.py`
   - run `scripts/download_docs.py`
4. After export, report the output location and read only the Markdown files relevant to the current task.
5. If another skill depends on this corpus, pass along concrete file paths or search results rather than summarizing the whole corpus.

## Output

When this skill is used, prefer one of these outputs:
1. A short status summary of whether local docs were reused or refreshed.
2. The specific file paths or filenames that are relevant to the task.
3. If export failed, the blocking dependency or script error and the next recovery step.

## Quality Check

Before finishing, verify:
1. You reused `markdown_docs/` when it was already sufficient instead of rerunning expensive crawling unnecessarily.
2. You read only the files relevant to the active task.
3. You kept script-running instructions out of the main answer unless they were needed.
4. You clearly distinguished between bundled scripts and generated outputs.
5. You treated `markdown_docs/` and `doc_index.json` as local run artifacts, not core skill instructions.

## Additional Resources

- Workflow, commands, outputs, and troubleshooting: [references/workflow.md](references/workflow.md)
- Exported local docs corpus: [markdown_docs](markdown_docs)
- Index builder: [scripts/crawl_doc_index.py](scripts/crawl_doc_index.py)
- Markdown exporter: [scripts/download_docs.py](scripts/download_docs.py)

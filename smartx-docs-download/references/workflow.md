# SmartX Docs Workflow

## When To Read This File

Read this file only when you need to run or debug the export scripts, or when the local `markdown_docs/` corpus is missing, stale, or clearly incomplete.

## Environment

- Python `3.9`
- Google Chrome installed locally
- Network access to `https://internal-docs.smartx.com`

Install dependencies:

```bash
pip install -r scripts/requirements.txt
playwright install chrome
```

## Standard Flow

### 1. Build the doc index

```bash
python scripts/crawl_doc_index.py
```

Expected result:
- A local `doc_index.json` is created in the skill directory.

### 2. Export docs to Markdown

```bash
python scripts/download_docs.py
```

Default behavior:
- Reads links from `doc_index.json`
- Writes exported documents to `markdown_docs/`
- Produces one Markdown file per document

Useful variants:

```bash
python scripts/download_docs.py -i doc_index.json -o markdown_docs
python scripts/download_docs.py --match "配置和管理规格" --limit 1
```

## Search Guidance

When the corpus already exists, search before opening files:

```bash
rg "关键词" markdown_docs
rg --files markdown_docs
```

Prefer narrowing by:
1. Product name
2. Document type such as `发布说明` or `用户指南`
3. Feature keyword

## Output Conventions

- `doc_index.json` is a generated index file.
- `markdown_docs/` is a generated local corpus.
- These are run artifacts and should be treated as refreshable local data.

## Troubleshooting

| Problem | Likely cause | Recovery |
|---|---|---|
| Child navigation items are missed | The nav tree rerendered after expansion | Rerun export and inspect the navigation-expansion logic in `scripts/download_docs.py` |
| Page body does not change after clicking | Page transition is slower than expected | Increase waits or inspect page-ready conditions in `scripts/download_docs.py` |
| Chrome is not found | Chrome is not installed for Playwright to use | Run `playwright install chrome` |
| Missing Python packages | Dependencies were not installed | Run `pip install -r scripts/requirements.txt` |

## Script Roles

- `scripts/crawl_doc_index.py`: Collects product and version entry pages into `doc_index.json`
- `scripts/download_docs.py`: Opens each page, expands navigation, captures the content area, and converts it to Markdown

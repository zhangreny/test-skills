---
name: testrail-testcase-extract-upload
description: Use when the user wants to parse a TestRail-style testcase markdown document into structured JSON, inspect the target suite or section tree, or upload the parsed testcase hierarchy into TestRail under a specific suite or section.
---

# TestRail Testcase Extract Upload

Use this skill when the task is about taking an existing testcase markdown document and turning it into structured TestRail content.

Typical triggers:

1. The user wants to parse a TestRail-style markdown testcase document into JSON.
2. The user wants to upload generated testcase markdown into TestRail.
3. The user has a target suite id or section id and wants the testcase tree created under it.
4. The user needs to inspect the TestRail suite or section tree before choosing an upload target.

Do not use this skill for testcase generation itself. Use it after testcase content already exists.

## Workflow

### 1. Confirm the input

Use this skill for markdown that follows the default TestRail export template used in this repo:

- level-2 through level-6 headings for modules, submodules, subsections, and cases
- testcase leaf nodes may appear at any heading depth that the parser accepts
- one localized description line under each heading
- one or more localized step lines under each case, such as `【Step1】` through `【StepN】`

Require these inputs before continuing:

1. The testcase markdown absolute path, for example `C:/work/testcase_final.md`.
2. The TestRail project id.
3. The TestRail upload target id.
4. The owning suite id only when the user already knows it or wants an explicit cross-check.

If the source does not follow this structure, fix or normalize the testcase content first.
If the testcase markdown or any intermediate JSON contains Chinese, prefer UTF-8 explicitly for reading and writing instead of relying on the OS default encoding.

Do not accept stdin or relative paths for testcase markdown.
Prefer resolving the suite id from the target through the script instead of guessing it manually.

### 2. Parse before upload

Always parse the markdown first to confirm the structure is valid.

Use:

```bash
python scripts/parse_testrail_template.py --source C:/absolute/path/to/testcase_final.md
```

This returns the nested JSON tree that the upload script will consume.
The parser uses UTF-8 and now performs garbled-text checks on the source and parsed result. If it reports suspected mojibake, stop and fix the source file encoding before uploading.

### 3. Inspect the target location if needed

If the user does not already know the target suite id or section id, inspect the TestRail tree first.

Use:

```bash
python scripts/list_testrail_tree.py --url http://testrail.smartx.com --project-id 23
```

Prefer reading the tree first instead of guessing ids.
The scripts default to the built-in SmartX TestRail credential and only need `--user` or `--api-key` when you want to override it.

### 4. Upload the testcase tree

Upload the markdown directly under a suite root or an existing section.

Use the shortest form when only the target id is known:

```bash
python scripts/upload_testrail_cases.py \
  --source C:/absolute/path/to/testcase_final.md \
  --url http://testrail.smartx.com \
  --project-id 23 \
  --target-id 12345
```

If the user already knows the owning suite id and wants explicit validation, pass it too:

```bash
python scripts/upload_testrail_cases.py \
  --source C:/absolute/path/to/testcase_final.md \
  --url http://testrail.smartx.com \
  --project-id 23 \
  --suite-id 678 \
  --target-id 12345
```

Rules:

1. `--source` must be an absolute path.
2. `--target-id` may be either a section id or a suite id.
3. When `--suite-id` is omitted, let the script try `get_section(target-id)` first; if that fails, treat `target-id` as a suite id in the same project.
4. If uploading to the suite root and the caller wants explicit validation, set `target-id` equal to `suite-id`.
5. If uploading to an existing subsection and `--suite-id` is provided, it must match the section's owning suite id.
6. Keep numbering in titles when uploading.
7. Map the localized description line to `custom_preconds`.
8. Map localized step lines to `custom_steps_separated`.
9. The built-in default TestRail credential is `renyu.zhang@smartx.com` / `Zhangry-2001`; use flags only when you need to override it.

## Scripts

### `scripts/parse_testrail_template.py`

Minimal parser extracted from the existing project logic.

Use it when you need:

1. Structured JSON for validation.
2. A pre-upload sanity check.
3. Reusable parsing from another script.

### `scripts/testrail_client.py`

Minimal TestRail API wrapper for:

1. `get_section`
2. `get_suites`
3. `get_sections`
4. `add_section`
5. `add_case`

Keep new API additions minimal unless the task truly needs them.

### `scripts/upload_testrail_cases.py`

Recursive uploader that:

1. Parses testcase markdown.
2. Can auto-resolve the owning `suite-id` from `target-id`.
3. Still accepts `suite-id` when the caller wants explicit validation.
4. Creates sections and cases recursively in TestRail.

### `scripts/list_testrail_tree.py`

Use when the user needs to find a valid upload target in a project before uploading.

## Output Expectations

When this skill is used, prefer one of these outputs:

1. Parsed JSON tree.
2. The created TestRail target summary and upload counts.
3. A concise error telling the user whether the failure was parsing, missing required input, auth, target resolution, or TestRail API rejection.

## Quality Check

Before finishing, verify:

1. The markdown was parsed successfully before upload.
2. The testcase markdown path was absolute.
3. The upload target was resolved as either a section or a suite in the given project.
4. Only the minimal extraction and upload logic was copied into `scripts/`.
5. Chinese-containing testcase markdown and intermediate files were handled as UTF-8, not with the system default encoding.
6. The skill stays focused on extraction and upload, not testcase generation.

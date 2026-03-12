# Workflow

This file answers one question: in what order should historical testcase sources be analyzed?

## Step 1: Confirm the source

Use this priority order:

1. Reuse an existing export script in the repo.
2. Reuse an existing grouped export directory.
3. Only add export logic if neither of the above exists.

If the repo already contains `export_testrail_cases.py`, inspect and reuse it first.

## Step 2: Prefer grouped exports

Default target structure:

```text
testrail_cases_by_group/
  <project>/
    <suite>.md
```

Requirements:

1. One suite per markdown file.
2. Preserve project grouping.
3. Preserve section and subsection hierarchy.
4. Do not default to one giant summary file.

## Step 3: Narrow the scope

Start with the smallest useful analysis unit:

1. One project.
2. One suite.
3. One subdomain.

Do not scan the entire corpus first.

## Step 4: Read structure before titles

Inspect structure first:

1. How sections are grouped.
2. How subsections are grouped.
3. Whether the structure is organized by feature, lifecycle, matrix, fault mode, or UI area.

Then inspect titles:

1. Title sentence patterns.
2. How many checkpoints a single case covers.
3. Whether success and failure paths appear in pairs.
4. Whether preconditions and results are stated explicitly.

## Step 5: Sample, then stop

Default sampling sequence:

1. Read the overall structure of one suite.
2. Read about 20 representative cases.
3. Expand to about 50 cases only if the pattern is still unstable.

Stop increasing sample size when:

1. Title patterns are stable.
2. Coverage dimensions repeat consistently.
3. Granularity rules are obvious.
4. New cases only repeat known patterns.

## Step 6: Write the rule document

The final output should include at least:

1. Organization pattern.
2. Naming pattern.
3. Test point splitting pattern.
4. Granularity pattern.
5. Coverage dimensions.
6. Anti-patterns.

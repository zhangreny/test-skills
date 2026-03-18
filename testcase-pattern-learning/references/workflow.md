# Workflow

This file answers one question: in what order should historical testcase sources be analyzed?

## Step 1: Confirm both source layers

Check whether the current task should use one or both of these source layers:

1. Curated local historical suites in `former_cases/`.
2. Live or recent grouped exports from TestRail.

Use this priority order when locating data:

1. Reuse curated local suite files in `former_cases/`.
2. Reuse an existing grouped export directory.
3. Reuse `export_testrail_cases.py` to pull a fresh grouped export.
4. Only add export logic if none of the above structured sources exists.

If the caller wants stronger testcase coverage rather than a lightweight style summary, do not stop after checking only one source layer unless you can explain why the other layer is unnecessary or unavailable.

## Step 2: Prefer grouped exports for live data

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

If the caller provides `core_keywords` and `expansion_keywords`, narrow in this order:

1. `core_keywords` for feature family anchoring.
2. Object words and action words.
3. Symptom words and result-layer words.
4. Tool / observability words and version / compatibility words.

Do not scan the entire corpus first.

Before reading curated local samples, pick the local root that matches the current group:

1. Network and security: `former_cases/15_SDN`
2. ELF virtualization: `former_cases/1_SmartX` with `121_Master.md` first
3. Backup and replication: `former_cases/6_Backup`
4. SKS and Kubernetes platform: `former_cases/8_SKS`
5. ZBS and block storage: `former_cases/18_ZBS CSI`, plus `former_cases/1_SmartX/300_SMTX ZBS.md` when linkage matters
6. SRE and platform ops:
   - `former_cases/10_可观测平台`
   - `former_cases/16_巡检中心`
   - `former_cases/17_SFS`
   - `former_cases/22_Neutree`

Only fall back to the broader `former_cases/` tree when no group root can be justified.

## Step 4: Read structure before titles

Inspect structure first:

1. How sections are grouped.
2. How subsections are grouped.
3. Whether the structure is organized by feature, lifecycle, matrix, fault mode, tool category, or UI area.

Then inspect titles:

1. Title sentence patterns.
2. How many checkpoints a single case covers.
3. Whether success and failure paths appear in pairs.
4. Whether preconditions and results are stated explicitly.
5. Whether titles or sections reveal tool / observability expectations.

## Step 5: Sample local first, compare with live, then stop

Default sampling sequence:

1. Read the overall structure of the closest curated local suite.
2. Read the overall structure of the closest live grouped suite when available.
3. Read about 20 representative cases across the source layers first.
4. Expand to about 50 cases only if the pattern is still unstable.

Stop increasing sample size when:

1. Title patterns are stable.
2. Coverage dimensions repeat consistently.
3. Granularity rules are obvious.
4. Tool / observability clues are stable enough to guide drafting.
5. New cases only repeat known patterns.

## Step 6: Write the output

The final output should include at least:

1. Historical neighbors and why they matched.
2. Organization pattern.
3. Naming pattern.
4. Test point splitting pattern.
5. Granularity pattern.
6. Coverage dimensions.
7. Tool / observability clues when relevant.
8. Coverage-expansion inputs or anti-patterns, depending on the caller's goal.

---
name: testcase-pattern-learning
description: Extract reusable testcase-writing rules from historical TestRail cases, curated local former_cases, or grouped markdown exports. Use when the user wants to study old testcase style, summarize naming or granularity patterns, review grouped suite exports, or derive reusable guidance for writing new testcases.
metadata:
  short-description: Learn reusable testcase-writing patterns from historical cases
---

# Testcase Pattern Learning

Use this skill to turn historical testcases into reusable testcase-writing guidance.
The goal is to produce generalized rules, not a suite-by-suite recap.

## Use This Skill When

- The user wants to learn how older testcases are named, split, or organized.
- The user wants coverage guidance from historical TestRail exports.
- The user wants reusable testcase design rules for a new feature.
- The user provides grouped markdown exports and asks for patterns, style, or anti-patterns.

## Default Workflow

1. Confirm the source layers.
   First identify whether there is a curated local corpus in `former_cases/`, an existing grouped export directory, and an exporter script for live TestRail data.
2. Prefer structured sources.
   Use curated local suite files and project / suite scoped grouped markdown exports instead of a single giant export whenever possible.
3. Narrow the scope first.
   Start with one project, one suite, or one subdomain before scaling up.
4. Read structure before details.
   Inspect section and subsection organization first, then sample titles, paired paths, tool clues, and case granularity.
5. Stop when patterns stabilize across the source layers you used.
   Do not read the full corpus if new samples only repeat known rules or only restate known coverage dimensions.
6. Output reusable rules or coverage-expansion inputs.
   Summarize naming, testcase splitting, granularity, coverage dimensions, tool / observability clues, and anti-patterns.

When another skill uses this skill to improve testcase detail rather than to write a standalone rule document, also do this:

1. Narrow to the closest historical subdomain first.
2. Start with the closest curated local samples in `former_cases/`.
3. For network, security, port-control, connectivity, or forwarding features, read from `former_cases/15_SDN` first.
4. If the caller wants stronger coverage, the local corpus lacks convincing neighbors, or the missing dimensions still look unstable, additionally pull from live TestRail grouped exports via an existing grouped export directory or `scripts/export_testrail_cases.py`.
5. Reuse `core_keywords` and `expansion_keywords` when the caller provides them; the latter should drive suite / section / object / action / symptom / result / tool / version searches.
6. Extract matrix dimensions, paired success/failure cases, tool and observability clues, and detail gaps that the current feature should inherit.
7. Return reusable detail guidance, `coverage_expansion_plan` inputs, and unsupported dimensions instead of copying old business content.

## Open References On Demand

- [references/workflow.md](references/workflow.md): detailed workflow, sampling, and stop conditions.
- [references/learning-rules.md](references/learning-rules.md): what rules to extract from historical cases.
- [references/output-template.md](references/output-template.md): default output structure for the final write-up.
- [references/examples.md](references/examples.md): good and bad examples of analysis output.
- [references/sdn-sample.md](references/sdn-sample.md): entrypoint for a longer domain-specific sample.
- [references/historical-neighbor-learning.md](references/historical-neighbor-learning.md): how to learn matrix detail from nearby historical suites, especially `former_cases/15_SDN`.
- [scripts/export_testrail_cases.py](scripts/export_testrail_cases.py): reusable exporter for grouped markdown output.

## Export Guidance

If the repository already includes `scripts/export_testrail_cases.py`, reuse it before creating new export code.

When the caller needs recent neighboring suites rather than a generic style study:

1. Prefer an existing grouped export directory if it is already available and still relevant.
2. Otherwise export the smallest relevant project or project set you can justify, then narrow by suite / section / keyword matching.
3. Do not stop at curated local samples alone if the caller explicitly wants better coverage and the current missing dimensions are still unclear.

Recommended command:

```bash
python scripts/export_testrail_cases.py --days 365 --output-dir testrail_cases_by_group
```

Expected directory shape:

```text
testrail_cases_by_group/
  <project>/
    <suite>.md
```

## Output Rules

- Deliver rules, not a chronological recap.
- Keep conclusions reusable across products when possible.
- Explicitly cover granularity, coverage dimensions, failure or recovery scenarios, and tool / observability clues when they affect testcase design.
- Call out anti-patterns that should not be copied into new testcase design.
- When the caller needs testcase 细节补全, prefer returning matrix dimensions, must-cover pairs, tool / observability clues, `coverage_expansion_plan` inputs, and unsupported dimensions over a long suite summary.
- If both curated local samples and live grouped exports were used, distinguish what each source layer contributed.

## Quality Bar

Before finishing, check that:

1. The analysis used structured sources: curated local suite files, grouped exports, or an equally structured source.
2. The write-up inspected structure before reading many case details.
3. The final output is a rule set or coverage-expansion input set, not a suite-by-suite summary.
4. The guidance is reusable for future testcase design.
5. If only one source layer was used, the write-up explains why the other source layer was unnecessary or unavailable.

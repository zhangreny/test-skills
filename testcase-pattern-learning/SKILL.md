---
name: testcase-pattern-learning
description: Extract reusable testcase-writing rules from historical TestRail cases or grouped markdown exports. Use when the user wants to study old testcase style, summarize naming or granularity patterns, review grouped suite exports, or derive reusable guidance for writing new testcases.
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

1. Confirm the source.
   Prefer an existing export script or an existing grouped export directory before writing new export logic.
2. Prefer grouped markdown exports.
   Use project and suite scoped markdown files instead of a single giant export whenever possible.
3. Narrow the scope first.
   Start with one project, one suite, or one subdomain before scaling up.
4. Read structure before details.
   Inspect section and subsection organization first, then sample titles and case granularity.
5. Stop when patterns stabilize.
   Do not read the full corpus if new samples only repeat known rules.
6. Output reusable rules.
   Summarize naming, testcase splitting, granularity, coverage dimensions, and anti-patterns.

## Open References On Demand

- [references/workflow.md](references/workflow.md): detailed workflow, sampling, and stop conditions.
- [references/learning-rules.md](references/learning-rules.md): what rules to extract from historical cases.
- [references/output-template.md](references/output-template.md): default output structure for the final write-up.
- [references/examples.md](references/examples.md): good and bad examples of analysis output.
- [references/sdn-sample.md](references/sdn-sample.md): entrypoint for a longer domain-specific sample.
- [scripts/export_testrail_cases.py](scripts/export_testrail_cases.py): reusable exporter for grouped markdown output.

## Export Guidance

If the repository already includes `scripts/export_testrail_cases.py`, reuse it before creating new export code.

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
- Explicitly cover granularity, coverage dimensions, and failure or recovery scenarios.
- Call out anti-patterns that should not be copied into new testcase design.

## Quality Bar

Before finishing, check that:

1. The analysis used grouped exports or an equally structured source.
2. The write-up inspected structure before reading many case details.
3. The final output is a rule set, not a suite-by-suite summary.
4. The guidance is reusable for future testcase design.

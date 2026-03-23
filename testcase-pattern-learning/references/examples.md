# Examples

This file keeps only examples. It does not repeat the workflow or rule definitions.

## Full sample

If the user wants a longer rule document example, open:

- [sdn-sample.md](sdn-sample.md)

## Example 1: the user wants historical writing patterns

User intent:

"Do not read tens of thousands of cases. Summarize the writing patterns from older testcases."

Good response shape:

1. Narrow to one project or one suite first.
2. Read structure before titles.
3. Output naming, granularity, coverage, and anti-pattern rules.

Bad response shape:

1. Read the full corpus immediately.
2. Retell cases one by one in suite order.

## Example 2: the user wants grouped exports first

User intent:

"Export historical TestRail cases into grouped markdown so we can study them later."

Good response shape:

1. Check whether `export_testrail_cases.py` already exists.
2. Reuse the existing exporter.
3. Export to `testrail_cases_by_group/`.
4. Keep one markdown file per suite.

Bad response shape:

1. Generate only one giant markdown file.
2. Lose the project and suite hierarchy.

## Example 3: good summary

```markdown
## Naming Pattern
- Titles usually include object, condition, and result.
- A common shape is `[object] - [condition] - [result]`.

## Granularity Pattern
- One case should validate one core result.
- Split the case when it mixes UI, logs, config, and functional result.

## Coverage Dimensions
- Main flow
- Failure path
- Object variation
- State change
- Fault recovery
```

## Example 4: bad summary

```markdown
This suite starts with case A, then case B, then case C.
Most cases seem to test the feature and look similar.
```

Why it is bad:

1. It is not reusable.
2. It does not abstract rules.
3. It does not help design new testcases.

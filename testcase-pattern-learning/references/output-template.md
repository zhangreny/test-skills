# Output Template

Use this structure by default when summarizing testcase-writing patterns.

```markdown
## Organization Pattern
- How suites and sections are usually organized.

## Naming Pattern
- How titles usually combine object, condition, and expected result.

## Test Point Splitting Pattern
- How one feature is usually split into separate testcase ideas.

## Granularity Pattern
- What should stay in one case and what should be split out.

## Coverage Dimensions
- Which common dimensions should be covered by default.

## Tool / Observability Clues
- Which execution tools and verification signals should be made explicit.

## Coverage Expansion Inputs
- Which must-pair paths, must-expand dimensions, and unsupported gaps should feed testcase drafting.

## Anti-Patterns
- Which habits should not be copied into new testcase design.
```

Checklist for the final output:

1. Prefer generalized rules over product-specific trivia.
2. Include both happy path and failure or recovery guidance when relevant.
3. Make tool / observability expectations actionable when they affect testcase writing.
4. Make the conclusions actionable for writing future testcases.

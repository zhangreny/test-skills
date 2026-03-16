# Historical Neighbor Learning

Use this reference when the goal is not just to summarize old testcase style, but to improve the detail coverage of a new testcase draft by learning from nearby historical sources.

## Purpose

Turn nearby historical cases into reusable detail guidance.
Do not copy old business content directly.
Do not expand the testcase scope just because old suites are large.

The output of this process should help answer:

1. Which matrix dimensions should be expanded explicitly?
2. Which dimensions can be sampled instead of fully enumerated?
3. Which success and failure paths usually appear in pairs?
4. Which edge or recovery cases are easy to miss if only reading the requirement?
5. Which execution tools and observability methods should be made explicit in new testcases?

## Source Layers

Default to two source layers when testcase coverage is the goal:

1. Curated local historical suites in `former_cases/`.
   Use these to learn stable domain matrix dimensions and recurring long-lived blind spots.
2. Live or recent grouped exports from TestRail.
   Use these to learn current suite organization, recent naming style, newer regression focus, and what the team is testing now.

It is acceptable to finish with only one source layer only when:

1. The other layer is unavailable or blocked.
2. The missing dimensions are already fully explained by the layer you used.
3. You explicitly say why the other layer was unnecessary or unavailable.

## Scope First

Always narrow before reading.

For network, security, port-control, connectivity, or forwarding features:

1. Start from `former_cases/15_SDN` only.
2. Prefer matching by suite name, section name, object name, action name, and symptom words.
3. Do not scan other project folders unless `15_SDN` clearly lacks relevant samples.

For live grouped exports:

1. Start from the same product, same feature family, or same object family first.
2. Prefer the smallest relevant project or grouped export slice.
3. Do not scan unrelated projects just because they share one keyword.

Recommended priority inside `15_SDN`:

1. Same feature family suite.
2. Same object or same action suite.
3. Same failure mode or same lifecycle suite.

## Search Strategy

Use these signals to find candidate suites or sections:

1. Object words.
   Examples: firewall, whitelist, VPC, gateway, port, rule, policy, VNC, migration.
2. Action words.
   Examples: create, edit, delete, enable, disable, attach, detach, upgrade, recover.
3. Symptom words.
   Examples: timeout, fallback, not effective, failed, cannot connect, pending, retry.
4. Result-layer words.
   Examples: UI display, log, connectivity, forwarding, audit, alert, task result.
5. Tool and observability words.
   Examples: API, CLI, script, trace, packet capture, counter, report, task, diagnosis tool.
6. Version and compatibility words.
   Examples: upgrade, downgrade, inherited config, existing cluster, compatibility, architecture.

Keep only the top few candidates.
Default target:

1. 3-5 suites.
2. 1-3 relevant sections per suite.
3. About 20 representative cases first, across the source layers you decided to use.

Expand only if the pattern is still unstable.

## Reading Order

Read in this order:

1. Suite structure.
   Check whether the suite is grouped by lifecycle, matrix, object type, fault mode, or UI area.
2. Section titles.
   Check what dimensions the author made explicit at the section level.
3. Representative case titles.
   Check how conditions and expected results are paired.
4. A small number of case bodies.
   Only read enough to understand what detail the title alone does not reveal.
5. Cross-source comparison.
   Check what the curated local suites emphasize versus what live grouped exports emphasize.

Do not default to full-file reading.

## What To Extract

The goal is to extract reusable matrix detail, not a suite recap.

Always try to produce these outputs:

### 1. Historical Neighbors

Record the most relevant sources:

1. Which suite matched.
2. Which section matched.
3. Which source layer it came from.
4. Why it matched the current feature.

### 2. Matrix Dimensions

Separate dimensions into:

1. Object matrix.
   Examples: object type, endpoint role, single vs multiple resources, same vs cross cluster.
2. Action matrix.
   Examples: create, edit, delete, enable/disable, associate/disassociate, upgrade, recover.
3. Result matrix.
   Examples: takes effect, does not take effect, timeout, fallback, display correct, log correct.

### 3. Must-Cover Detail Points

Extract detail points that appear repeatedly in historical suites and are easy to miss from the requirement alone.

Examples:

1. Success and failure must appear in pairs.
2. Switching state often needs before/after validation.
3. A fallback path may need both correctness and latency validation.
4. UI and real effect should not always stay in one case.

### 4. Tool and Observability Clues

Always extract how historical suites make hidden results testable.

Capture at least:

1. Execution tools.
   Examples: UI, API, CLI, setup scripts, diagnosis tools.
2. Observability methods.
   Examples: logs, alerts, counters, reports, packet capture, trace, task state.
3. Tool-required paths.
   Which case families only become valid when the tool or observation step is made explicit.

### 5. Sampling Guidance

Split dimensions into two groups:

1. Can sample.
   These dimensions can use representative values if the result pattern is stable.
2. Must not sample.
   These dimensions must be explicitly expanded because they often change behavior.

Typical must-not-sample dimensions:

1. Protocol difference.
2. Endpoint role difference.
3. Same-path vs cross-path difference.
4. Upgrade-before vs upgrade-after.
5. Recovery-before vs recovery-after.

### 6. Coverage Expansion Inputs

Always try to leave behind inputs that another skill can turn into a `coverage_expansion_plan`:

1. Must-pair paths.
   Examples: success/failure, before/after edit, enable/disable, upgrade before/after, fault/recovery.
2. Must-expand dimensions.
   Dimensions that should become explicit independent cases.
3. Tool-required paths.
   Paths that need UI / API / CLI / log / alert / capture / trace / report steps to be explicit.
4. Unsupported dimensions.
   Gaps that still lack enough historical evidence.

## How To Use The Result

When another skill uses this output to generate new testcases:

1. Keep the current requirement as the primary source of truth.
2. Use the historical result only to expand detail and close common coverage gaps.
3. Let curated local suites contribute broad matrix dimensions and recurring long-lived blind spots.
4. Let live grouped exports contribute current naming, organization, and recent regression focus.
5. Convert the learned dimensions into a `coverage_expansion_plan` before drafting final cases.
6. Prefer “condition + action + single result” even after matrix expansion.

## Stop Conditions

Stop reading more historical suites when:

1. The matrix dimensions are already stable.
2. New suites only repeat known dimensions.
3. The missing detail points are already concrete enough to drive testcase drafting.
4. The tool / observability clues are already concrete enough to drive testcase drafting.

If relevant historical suites are still too weak:

1. Say exactly which detail dimension is still unsupported.
2. Say whether the gap comes from the curated local layer, the live layer, or both.
3. Do not invent a matrix just to make the output look complete.

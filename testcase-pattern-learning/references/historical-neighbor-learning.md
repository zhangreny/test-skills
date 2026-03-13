# Historical Neighbor Learning

Use this reference when the goal is not just to summarize old testcase style, but to improve the detail coverage of a new testcase draft by learning from nearby historical suites.

## Purpose

Turn nearby historical cases into reusable detail guidance.
Do not copy old business content directly.
Do not expand the testcase scope just because old suites are large.

The output of this process should help answer:

1. Which matrix dimensions should be expanded explicitly?
2. Which dimensions can be sampled instead of fully enumerated?
3. Which success and failure paths usually appear in pairs?
4. Which edge or recovery cases are easy to miss if only reading the requirement?

## Scope First

Always narrow before reading.

For network, security, port-control, connectivity, or forwarding features:

1. Start from `former_cases/15_SDN` only.
2. Prefer matching by suite name, section name, object name, action name, and symptom words.
3. Do not scan other project folders unless `15_SDN` clearly lacks relevant samples.

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

Keep only the top few candidates.
Default target:

1. 3-5 suites.
2. 1-3 relevant sections per suite.
3. About 20 representative cases first.

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

Do not default to full-file reading.

## What To Extract

The goal is to extract reusable matrix detail, not a suite recap.

Always try to produce these outputs:

### 1. Historical Neighbors

Record the most relevant sources:

1. Which suite matched.
2. Which section matched.
3. Why it matched the current feature.

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

### 4. Sampling Guidance

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

## How To Use The Result

When another skill uses this output to generate new testcases:

1. Keep the current requirement as the primary source of truth.
2. Use the historical result only to expand detail and close common coverage gaps.
3. Convert the learned dimensions into a `coverage_expansion_plan` before drafting final cases.
4. Prefer “condition + action + single result” even after matrix expansion.

## Stop Conditions

Stop reading more historical suites when:

1. The matrix dimensions are already stable.
2. New suites only repeat known dimensions.
3. The missing detail points are already concrete enough to drive testcase drafting.

If relevant historical suites are still too weak:

1. Say exactly which detail dimension is still unsupported.
2. Do not invent a matrix just to make the output look complete.

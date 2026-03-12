# Learning Rules

This file answers one question: what rules should be extracted first from historical testcases?

## 1. Naming pattern

High quality titles usually include:

1. The test object.
2. A key condition.
3. The expected result.

Recommended title shapes:

1. `[object or path] - [condition] - [result]`
2. `[page or entry] - [capability] - [result]`
3. `[resource condition] - [action] - [result]`
4. `[fault action] - [observed object] - [recovery result]`

Avoid vague titles such as:

1. Feature test
2. Verify normal flow
3. Comprehensive scenario
4. Other test

## 2. Test point splitting

When extracting test points, ask:

1. What is the core capability of the feature?
2. Which conditions change the result?
3. At which layer does the result appear?
4. Which failure paths are mandatory?
5. Are there lifecycle actions to cover?

Common test point categories:

1. Main flow
2. Object or parameter variation
3. Boundary behavior
4. Invalid input or bad configuration
5. State transition
6. Fault recovery
7. Display and observability
8. Resource constraint
9. Upgrade or compatibility
10. Regression from historical issues

## 3. Granularity rules

An ideal single case usually contains:

1. One clear condition
2. One clear object
3. One clear action
4. One core result

Split a case when:

1. One title implies multiple independent results.
2. It validates UI, logs, configuration, and forwarding all at once.
3. It covers multiple object types in one case.
4. It mixes multiple protocols or paths.
5. It mixes multiple lifecycle actions.
6. It combines success and failure into one case.

## 4. Coverage dimensions

Check these common dimensions first:

1. Main flow
2. Failure path
3. Object variation
4. Parameter variation
5. Lifecycle action
6. State change
7. Display or reporting
8. Logs or counters
9. Fault and recovery
10. Upgrade and compatibility
11. Resource limits
12. Historical regression

## 5. Anti-patterns

Common bad smells:

1. The title contains only an action and no result.
2. One case validates too many points.
3. Only happy path is covered.
4. The analysis only checks UI and not real effectiveness.
5. Old case titles are copied without abstraction.
6. The final rules only work for one product and cannot generalize.

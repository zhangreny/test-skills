---
name: testcase-pattern-learning
description: Extracts reusable testcase design rules from historical TestRail cases and grouped markdown exports. Use when the user wants to study old testcase style, summarize naming and granularity patterns, review grouped suite exports, or derive coverage and anti-pattern guidance for writing new testcases.
---

# Testcase Pattern Learning

## Quick Start

Use this skill to turn old testcases into reusable testcase-writing rules instead of restating old cases one by one.

Use it when the user wants to:
1. 总结旧测试用例写法。
2. 从 TestRail 导出结果里学习规律。
3. 按项目或 suite 学习，而不是阅读一个超大导出文件。
4. 整理后续写新 feature 用例可复用的方法论。

## Instructions

按下面顺序执行：
1. 先确认历史用例来源，优先复用已有导出脚本或现成导出目录。
2. 默认使用按项目和 suite 拆分的目录版导出，不优先使用单个大文件。
3. 先缩小范围，再看结构，再看标题，最后提炼规则。
4. 最终输出规则文档，而不是阅读笔记或 suite 流水账。

如果仓库里存在 `export_testrail_cases.py`，优先检查并复用它。

默认命令：

```bash
python scripts/export_testrail_cases.py --days 365 --output-dir testcase_tutorail_of_groups
```

默认目录结构：

```text
testcase_tutorail_of_groups/
  <project>/
    <suite>.md
```

## Output Template

最终总结默认使用下面结构：

```markdown
## 命名规律
- [标题通常如何组织]

## 测试点拆分规律
- [一个 feature 通常如何拆点]

## 粒度规律
- [一条 case 的理想粒度]

## 覆盖维度
- [默认应补的维度]

## 反模式
- [应避免的坏味道]
```

总结应能回答：
1. 旧用例通常怎么命名。
2. 一个 feature 通常怎么拆测试点。
3. 一条 case 的理想粒度是什么。
4. 哪些覆盖维度默认要补。
5. 哪些坏味道要避免。

## Quality Check

完成前检查：
1. 是否优先使用了目录化导出。
2. 是否先看结构再看细节内容。
3. 是否输出了规则，而不是旧用例流水账。
4. 是否明确提到了粒度、覆盖维度、异常与恢复。
5. 是否保持结论可泛化，而不是只适用于单一产品。

## Additional Resources

- 执行流程见 [references/workflow.md](references/workflow.md)
- 提炼框架见 [references/learning-rules.md](references/learning-rules.md)
- 正反例见 [references/examples.md](references/examples.md)
- SDN 长样例见 [tutorial-all-groups/sdn.md](tutorial-all-groups/sdn.md)
- 导出脚本见 [scripts/export_testrail_cases.py](scripts/export_testrail_cases.py)

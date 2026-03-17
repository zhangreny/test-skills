# Step 5：测试设计收敛

## 目录

- 5.1 读取资料
- 5.2 完成测试设计分析
- 5.2.1 引入通用测试设计维度
- 5.3 测试对象核对
- 5.4 建立执行工具与观测矩阵
- 5.5 学习历史近邻用例并补全矩阵
- 5.6 生成 `coverage_expansion_plan`
- 5.7 输出测试角度与历史矩阵补全结果，并等待确认

## 5.1 读取资料

读取以下输入：

- 用户原始需求文档
- Step 3 下载到本地的相关补充文档
- `../smartx-docs-download/markdown_docs` 中与当前 feature 直接相关的本地文档
- Step 4 的 Jira 摘要

读取要求：

- `.md` 直接读取内容。
- `.pdf`、`.docx` 使用当前环境中可行的本地读取方式。
- 如果某个关键文件无法读取，立即说明受阻文件和影响，不要跳过。

## 5.2 完成测试设计分析

基于“原始需求 + Drive 补充文档 + SmartX 本地文档 + Jira 摘要”完成以下分析：

1. Feature 定位
2. 核心对象
3. 主流程
4. 结果落点
5. 边界与异常
6. 依赖关系
7. 执行工具与观测手段
8. 历史问题与回归风险
9. 未决疑点
10. 依据来源

要求：

- 不要只复述原文，要抽象出测试设计真正需要的信息。
- 结论必须能回指到具体文档或 Jira issue，而不是纯猜测。
- 如果 SmartX 产品、术语、版本、对象职责仍有疑点，先回到 `../smartx-docs-download/markdown_docs` 继续检索。
- 如果检索后仍无法确定，停止推进并向用户说明缺口。

## 5.2.1 引入通用测试设计维度

按需读取 `references/test-design-dimensions.md`，把其中的通用测试维度作为 Step 5 的显式设计输入，而不是留到生成 testcase 时再临时判断。

执行要求：

- 至少逐项判断以下维度：验收测试、功能测试、边界测试、可靠性测试、用户场景测试、压力测试、规格测试、兼容性测试、集群扩缩容验证、集群升级验证。
- 对每个维度都必须给出 `must_cover`、`sample_cover` 或 `not_applicable` 之一。
- 对每个维度都要补充原因、映射对象、映射测试角度和预计承接的 case 分组。
- 如果某一维度需要特殊环境、特殊前置条件或额外资料，例如压测环境、升级链路、兼容矩阵、扩缩容资源池，要在 Step 5 先显式标记，不要推迟到 Step 6。
- 如果 feature 明确涉及前后端联动、端到端集成、故障恢复、稳定性、兼容性、扩缩容或升级，不允许把对应维度直接标记为 `not_applicable`。

## 5.3 测试对象核对

在进入用例生成前，显式列出“需要被测试的独立对象”。

推荐格式：

| 测试对象 | 来源 | 是否已有对应测试角度 |
|----------|------|----------------------|
| 对象名 | 需求 / 补充文档 / Jira | 是 / 否 |

核对重点：

- 需求文档直接提到的对象
- 补充文档中补出的独立对象
- Jira 历史问题暴露出的高风险对象
- CRUD、状态切换、异常、恢复是否均有测试视角
- 对象差异、动作差异、结果差异是否都能在后续 case 中落地，而不是只停留在分析表述

## 5.4 建立执行工具与观测矩阵

在进入历史近邻学习前，先显式列出“每类测试角度准备如何执行、如何观察结果”。

推荐格式：

| 测试角度 / 对象 | 关键动作 | 执行工具 | 观测手段 | 预期信号 | 是否已有覆盖 |
|----------------|----------|----------|----------|----------|--------------|
| 角度名 / 对象名 | 动作名 | UI / API / CLI / 脚本 / 工具 | 日志 / 告警 / 任务 / 计数 / 抓包 / trace / 报表 | 关键验证信号 | 是 / 否 |

执行要求：

- 优先从需求文档、Drive 补充文档、Jira 结果、SmartX 本地文档中识别用户和测试实际会使用的工具，而不是生成时再临时脑补。
- 对每个高优先级测试角度，至少给出一条“如何执行”路径和一条“如何观察结果”路径。
- 如果某个结果并不直接体现在 UI 中，就不能只写 UI 验证；要补齐 API、CLI、日志、告警、计数、报表、抓包、trace、任务状态等观测方式。
- 如果 feature 本身就是工具 / 诊断能力，则既要覆盖“工具功能是否正确”，也要覆盖“工具输出是否能支撑问题定位”；这两类不应混在一条 case 中。
- 如果某个关键测试角度目前没有明确的执行工具或观测手段，要显式标记为缺口，后续不得在未补齐的情况下直接生成 final case。

本步骤至少要产出：

1. `execution_tool_matrix`
2. `observability_matrix`
3. `tool_required_paths`
   - 哪些测试角度必须显式带出 API / CLI / 脚本 / 日志 / 告警 / 抓包 / trace / 报表等执行或观测动作

## 5.5 学习历史近邻用例并补全矩阵

在正式向用户展示测试角度前，先补做一轮“历史近邻用例学习”，目标不是复述旧 case，而是补全当前 feature 的细节矩阵。

读取入口：

- 先读取并遵循 `../testcase-pattern-learning/SKILL.md`
- 如需具体方法，再按需读取 `../testcase-pattern-learning/references/historical-neighbor-learning.md`
- 如需确认取样顺序，再按需读取 `../testcase-pattern-learning/references/workflow.md`

执行规则：

- 这一轮必须采用“双源历史学习”：
  - 本地样本源：优先从 `../testcase-pattern-learning/former_cases` 中找同域、同对象、同动作或同故障模式的历史 suite。
  - 实时 / 近期 TestRail 源：优先复用已有 grouped export；如果没有可用的当前分组导出，按 `../testcase-pattern-learning/SKILL.md` 中的导出 guidance 调用 `scripts/export_testrail_cases.py` 拉取结构化分组结果，再做近邻检索。
- 如果 feature 属于网络 / 安全 / 端口控制 / 连通性 / 转发链路类，本地样本源只允许优先读取 `../testcase-pattern-learning/former_cases/15_SDN`，且不要扩散到其他项目目录，除非 `15_SDN` 明显没有相关样本且已经向用户说明。
- 如果 feature 属于 ELF 虚拟化、虚拟机生命周期、虚拟机迁移、v2v、Guest 工具、虚拟化与 ZBS 联动、Tower 纳管或虚拟化管理面联动类，先读取 `../testcase-pattern-learning/tutorial-all-groups/elf-group.md`，并优先把以下两个 suite 作为本地样本源：
  - `../testcase-pattern-learning/former_cases/1_SmartX/121_Master.md`
  - `../testcase-pattern-learning/former_cases/1_SmartX/300_SMTX ZBS.md`
- 对上述 ELF 组场景，不要先扩散到其他 `former_cases` 目录；只有当 `121_Master.md` 与 `300_SMTX ZBS.md` 明显不足以覆盖当前 feature，且已经说明缺口后，才补充其他高相关样本。
- 实时 / 近期 TestRail 源的检索要复用 Step 2 的 `core_keywords` 和 `expansion_keywords`，至少覆盖 suite 名、section 名、对象词、动作词、症状词、结果层词、工具词、版本词这些入口。
- 先看结构，再看标题，再看代表性 case，不要一上来通读整份历史 suite。
- 历史用例只用于学习矩阵维度、拆点方式、正反成对关系、工具 / 观测习惯、边界与恢复，不直接照抄旧业务内容。
- 如果实时 / 近期 TestRail 检索因认证、网络、导出失败或数据量受限而受阻，要明确说明受阻点，并继续使用本地样本源推进，但要把“缺少实时近邻样本”的影响显式记入本轮分析结论。

本步骤至少要产出以下分析结果，并在 Step 5.7 展示给用户、在 Step 6 中复用：

1. `historical_neighbors`
   - 本地样本源命中的 suite / section / case 来源
   - 实时 / 近期 TestRail 源命中的 suite / section / case 来源
2. `matrix_dimensions`
   - 对象矩阵
   - 动作矩阵
   - 结果矩阵
3. `must_cover_detail_points`
   - 历史样本里高频出现、但需求文档未充分展开的细节点
4. `can_sample_dimensions`
   - 可以抽样覆盖的维度
5. `must_not_sample_dimensions`
   - 必须显式展开、不能只抽样的维度
6. `paired_paths`
   - 历史近邻中稳定成对出现、当前 feature 应继承的正反路径、前后状态、异常 / 恢复路径
7. `tool_observability_clues`
   - 历史近邻里反复出现的执行工具、观测手段、定位信号和易漏验证层
8. `must_split_axes`
   - 即使已经形成原子 case，也必须继续显式展开的拆分轴，例如对象差异、前置条件差异、输入取值差异、权限差异、状态前后差异、入口差异、结果差异、观测差异、生命周期阶段差异

要求：

- 如果历史样本不足以支持矩阵补全，要明确说明“不足在哪里”，而不是强行脑补。
- 如果历史样本与当前需求冲突，以当前需求为准。
- 如果本地样本源与实时 / 近期 TestRail 源不一致，要明确说明差异点；命名和当前团队写法优先参考实时 / 近期 TestRail 源，领域矩阵和高频漏测点优先吸收高质量本地样本源，但都不能覆盖当前需求本身。
- 如果当前 feature 命中 ELF 组范围，要显式吸收 `elf-group.md` 中的操作链路拆分方式，以及 `121_Master.md`、`300_SMTX ZBS.md` 中稳定出现的平台 / 版本 / 架构 / vhost / Guest / 迁移路径 / ZBS 联动 / 升级与回收站等矩阵线索。
- 这一轮的目标是“补细节”，不是“扩大范围”。
- 对“场景已覆盖、但用例仍偏粗”的情况，优先继续提炼 `must_split_axes`，不要因为已经有原子 seeds 就提前停止；后续 Step 6 必须把这些拆分轴落实成更多独立 case。

## 5.6 生成 `coverage_expansion_plan`

在正式生成 testcase 前，必须把 Step 5.3、Step 5.4、Step 5.5 的分析结果收敛成一份显式的 `coverage_expansion_plan`，用于约束后续生成与 review。

`coverage_expansion_plan` 至少包含：

1. `requirement_points_to_cover`
   - 每个需求点将由哪些测试角度 / case 分组承接
2. `jira_risk_points_to_cover`
   - Jira 暴露出的历史风险如何映射到具体 case
3. `historical_inherited_points`
   - 从本地样本源和实时 / 近期 TestRail 源继承的细节点、成对路径、高频漏测点
4. `must_pair_paths`
   - 必须成对出现的成功 / 失败、修改前 / 修改后、启用 / 停用、存在 / 不存在、升级前 / 升级后、故障中 / 恢复后等路径
5. `tool_required_paths`
   - 必须显式带出 UI / API / CLI / 脚本 / 日志 / 告警 / 抓包 / trace / 报表等执行或观测手段的 case 分组
6. `must_expand_dimensions`
   - 不能只抽样、必须显式展开成独立 case 的维度
7. `sampled_dimensions`
   - 允许抽样覆盖的维度，以及为何可以抽样
8. `unsupported_dimensions`
   - 当前资料仍不足以支撑、需要保留风险提示的维度
9. `test_dimension_coverage`
   - 对验收、功能、边界、可靠性、用户场景、压力、规格、兼容性、扩缩容、升级这 10 类维度逐项记录 `must_cover` / `sample_cover` / `not_applicable`
   - 记录每类维度映射到的测试角度、case 分组、特殊环境依赖或残余风险
10. `case_granularity_strategy`
   - 记录哪些维度已经细到可以直接生成 testcase，哪些维度即使已有原子 seeds 仍要继续按 `must_split_axes` 扩写成更多独立 case

要求：

- `coverage_expansion_plan` 不是内部笔记，而是后续生成和 reviewer 复核的直接对账依据。
- 每个 `must_cover_detail_points`、`paired_paths`、`tool_required_paths` 都必须能在 `coverage_expansion_plan` 中找到落点。
- 每个 `must_split_axes` 都必须在 `coverage_expansion_plan` 中明确说明“拆成哪些独立 case 类别”，不能只写成一句“后续补充覆盖”。
- 如果某个需求点、高风险点或历史继承点还找不到对应 case 承接位置，要先显式标记为缺口，而不是默认“生成时自然会补到”。
- 如果某个维度被标记为可抽样，要写明“为什么可抽样”，避免把本该展开的高风险差异维度误判为低优先级。
- 如果某类通用测试维度被标记为 `must_cover`，但还没有明确映射到测试角度或 case 分组，必须先补齐，不能进入 Step 6。
- 默认倾向是“多生成细 case”，而不是“少生成大 case”；只有当多个组合确实共享同一对象、同一条件、同一动作、同一核心结果、同一观测方式时，才允许合并。

## 5.7 输出测试角度与历史矩阵补全结果，并等待确认

向用户展示建议测试角度，以及 Step 5.5 学到的历史矩阵补全结果，再进入 Step 6。

这一轮确认时至少同时展示：

1. 测试对象核对表
2. `execution_tool_matrix` 与 `observability_matrix`
3. 建议测试角度
4. `historical_neighbors`
5. `matrix_dimensions`
6. `must_cover_detail_points`
7. `paired_paths`
8. `coverage_expansion_plan`
9. `must_split_axes`
10. `test_dimension_coverage` 摘要

要求：

- 不要把工具矩阵和 `coverage_expansion_plan` 只留作内部信息，必须与测试角度一起展示给用户确认。
- 必须等待用户确认后再生成最终用例。

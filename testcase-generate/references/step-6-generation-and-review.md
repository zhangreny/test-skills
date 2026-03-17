# Step 6：生成、补缺并 review 测试用例

## 目录

- 6.1 先参考历史模式，但不被模式绑死
- 6.2 输出格式要求
- 6.3 先生成原子 case seeds
- 6.4 执行有上限的补缺循环
- 6.5 从 seeds 渲染主稿与补缺增量
- 6.6 合并最终版
- 6.7 reviewer 准备复核输入
- 6.8 reviewer 复核业务范围与覆盖
- 6.9 reviewer 复核原子性与结构格式
- 6.10 reviewer 回修与输出规则

## 6.1 先参考历史模式，但不被模式绑死

生成前先检查 `../testcase-pattern-learning/tutorial-all-groups`，并复用 Step 5.4 的工具矩阵、Step 5.5 的历史近邻学习结果以及 Step 5.7 已确认的测试设计与 `coverage_expansion_plan`。

规则：

1. 优先找与当前 feature 高相关的模式文档。
2. 先阅读 `../testcase-pattern-learning/tutorial-all-groups/all-groups-common.md`，获取所有组通用的拆点、粒度、命名和覆盖规则。
3. 再根据当前 feature 所属组别，按需阅读 `../testcase-pattern-learning/tutorial-all-groups` 下对应组的补充文档；如果当前只有通用文档，则只使用通用文档。
4. 如果 feature 属于网络 / 安全 / 端口控制类，再阅读 `../testcase-pattern-learning/tutorial-all-groups/network-group.md`。
5. 如果 feature 不属于网络组，但属于 ELF 虚拟化、虚拟机生命周期、v2v、Guest 工具、虚拟化与 ZBS 联动、Tower 纳管或虚拟化管理面联动类，再阅读 `../testcase-pattern-learning/tutorial-all-groups/elf-group.md`，并按需回看：
   - `../testcase-pattern-learning/former_cases/1_SmartX/121_Master.md`
   - `../testcase-pattern-learning/former_cases/1_SmartX/300_SMTX ZBS.md`
6. 对 ELF 组 feature，优先继承 `elf-group.md` 中按操作链路拆分的方式，以及 `121_Master.md`、`300_SMTX ZBS.md` 中稳定出现的平台 / 版本 / 架构 / vhost / Guest / 迁移路径 / ZBS 联动 / 升级与回收站的成对覆盖结构。
7. 如果 Step 5.5 已从本地样本源或实时 / 近期 TestRail 源提炼出细节矩阵，生成时必须显式吸收这些矩阵结论，而不是只复用抽象 pattern。
8. 模式文档用于补充拆点、粒度、命名和覆盖维度；历史近邻用例用于补充矩阵细节、正反路径、高频漏测点、工具 / 观测习惯。
9. `coverage_expansion_plan`、`tool_required_paths`、`must_pair_paths` 不是展示材料，生成时必须显式落实到具体 case 或 case 分组。
10. 当前需求与模式文档或历史样本冲突时，以当前需求为准。

## 6.2 输出格式要求

复用 `references/testrail_default.md` 的结构规范，不要复用其中任何示例业务内容。

### 6.2.1 中间产物输出目录约定

Step 6 中生成的 `case_seed_plan.md`、`case_seeds_round*.md`、`case_seed_gap_report.md`、`testcase_base.md`、`testcase_delta_*.md`、`testcase_final.md` 都属于本技能的中间产物或过程产物，不能默认散落到当前工作目录。

目录规则：

- 如果调用方或用户明确给了 `output_dir`，则在该目录下创建独立子目录：`.codex-testcase-generate`
- 如果没有提供 `output_dir`，则自动创建系统临时目录下的时间戳工作目录：
  - Windows：`%TEMP%\\codex-testcase-generate-YYYYMMDD-HHMMSS`
  - macOS / Linux：`/tmp/codex-testcase-generate-YYYYMMDD-HHMMSS`
- 本步骤后续提到的所有文件名，默认都指这个 `working_dir` 下的文件，而不是当前工作目录
- 如果用户只需要最终正文、不需要落盘文件，可以继续在内部生成这些中间产物，但仍应把它们视为位于 `working_dir`，不要污染用户仓库
- 如果调用方希望保留最终文件，返回时明确说明最终文件位于哪个 `working_dir`

输出要求：

- 采用 `## 模块 -> ### 子模块 -> #### 用例` 的层级。
- 每条用例包含：
  - `描述：`
  - `【Step1】`
  - `【Step2】`
  - `【Step3】`
- 一条 case 只验证一个核心结果。
- 如果某条 case 的关键验证依赖 API / CLI / 日志 / 告警 / 任务状态 / 抓包 / trace / 报表等工具或观测手段，要在 `描述：` 或 `【Step3】` 中显式体现，不要写成“结果正确”但看不出如何判断。
- 不输出模板说明文字，不输出“示例”“占位提示”等内容。

## 6.3 先生成原子 case seeds

不要直接从测试角度生成最终 markdown testcase。先生成一份“原子级 case 种子表”，用于防止产出停留在大纲层。

先生成：

- `working_dir/case_seed_plan.md`
  - 记录本轮计划从哪些测试角度、矩阵维度、历史风险点生成 case seeds
- `working_dir/case_seeds_round0.md`
  - 第一轮原子 case 种子表

每条 `case_seed` 至少包含以下字段：

1. `feature_area`
2. `test_theme`
3. `object`
4. `precondition`
5. `action`
6. `expected_result`
7. `observability`
8. `source`
9. `priority`
10. `mapped_dimensions`
11. `mapped_requirements`

生成要求：

- 一条 `case_seed` 只能对应一个核心结果，不允许用“基础功能验证”“异常场景验证”“权限检查”等主题词直接充当 testcase。
- `case_seed` 的最小粒度应接近“对象 + 条件 + 动作 + 单一结果 + 观测方式”；这只是下限，不是目标上限。
- `case_seed` 允许暂时不按最终 markdown 结构书写，但必须足够原子，能够稳定渲染为一条 testcase。
- `coverage_expansion_plan` 中的每个需求点、风险点、历史继承点，都必须先映射到一个或多个 `case_seed`，再进入最终 markdown 生成。
- 如果某个需求点、风险点或历史继承点已经形成原子 seed，但仍然混合了多个对象、多个条件区间、多个输入取值、多个状态前后、多个入口、多个结果信号或多个观测方式，必须继续拆成多条 seeds。
- 默认按以下拆分轴检查是否还要继续细化：对象差异、前置条件差异、输入值 / 边界值差异、权限或角色差异、入口差异、状态变化前后差异、异常类型差异、恢复路径差异、生命周期阶段差异、观测方式差异。
- 除非 `coverage_expansion_plan` 已明确标记为 `sampled_dimensions`，否则不要因为“已经有一条原子 seed”就停止扩写；默认要把高风险差异拆成更多独立 seeds。
- 如果当前输出仍像“主题大纲”而不是原子种子，必须继续拆分，不能直接进入下一步。

## 6.4 执行有上限的补缺循环

在 `case_seeds_round0.md` 基础上，进入“补缺循环”，每轮都只补当前缺口，不重写全部内容。

循环产物：

- `working_dir/case_seeds_round1.md`
- `working_dir/case_seeds_round2.md`
- `working_dir/case_seeds_round3.md`
- `working_dir/case_seed_gap_report.md`

每轮循环必须执行：

1. 对照 `coverage_expansion_plan` 检查当前 seeds 是否已覆盖：
   - `requirement_points_to_cover`
   - `jira_risk_points_to_cover`
   - `historical_inherited_points`
   - `must_pair_paths`
   - `tool_required_paths`
   - `must_expand_dimensions`
2. 找出当前仍停留在“大纲层”的主题：
   - 只有主题，没有明确对象
   - 只有动作，没有明确结果
   - 只有结果，没有明确触发条件
   - 没写观测方式
   - 把多个变量、多种结果混在同一条 seed 里
   - 已经原子，但仍把多个高风险拆分轴合并在同一条 seed 里
3. 仅补这些缺口，生成本轮 delta seeds：
   - 新增 seeds
   - 必拆 seeds
   - 必删 seeds
   - 必调整 seeds
4. 将本轮 delta 合并进 working seeds，形成新的 `working_dir/case_seeds_roundN.md`
5. 输出本轮 `gap_report`，说明本轮补了什么、还剩什么

循环停止条件：

- 所有 P0 / P1 缺口都已有对应 seeds
- `must_pair_paths` 已全部落地到 seeds
- `tool_required_paths` 已全部落地到 seeds
- `must_expand_dimensions` 已全部展开成独立 seeds
- `must_split_axes` 已全部落地到 seeds，不再存在“虽然原子，但仍合并了多个高风险差异”的情况
- 连续 1 轮未发现新的高价值缺口
- 或达到最大 3 轮补缺

循环约束：

- 不允许写开放式“继续补到满意为止”的循环，必须有明确停止条件和最大轮数。
- 每轮循环的目标是“继续拆细、继续补缺”，不是再生成一版新的大纲。
- 如果某类 feature 天然是矩阵型需求，应优先补对象差异、条件差异、结果差异，而不是只增加新的章节标题。
- 如果某类 feature 天然是矩阵型需求，不要满足于“每个主题一条原子 seed”；要优先把矩阵的关键组合拆成更多独立 seeds。
- 如果某个主题经检查仍无法拆成原子 seeds，要明确说明缺少了什么输入，而不是用笼统 case 顶替。

## 6.5 从 seeds 渲染主稿与补缺增量

只有在 `working_dir/case_seeds_roundN.md` 满足停止条件后，才允许渲染最终 testcase markdown。

渲染顺序：

- `working_dir/testcase_base.md`
  - 由当前 working seeds 直接渲染出的主稿
- `working_dir/testcase_delta_matrix_lifecycle.md`
  - 记录本轮从对象差异、动作差异、状态切换、生命周期闭环补出的 seeds 所对应的 testcase
- `working_dir/testcase_delta_failure_recovery.md`
  - 记录本轮从风险、异常、边界、恢复、回滚、清理、重试、权限、兼容补出的 testcase
- `working_dir/testcase_delta_tools_observability.md`
  - 记录本轮从执行工具、观测手段、日志 / 告警 / 报表 / 计数 / 任务 / 抓包 / trace 补出的 testcase
- `working_dir/testcase_delta_historical_regression.md`
  - 记录本轮从 Jira、本地样本源、实时近邻样本继承的 testcase

渲染要求：

- `working_dir/testcase_base.md` 中的每条 case 必须能回溯到一个或多个 seeds。
- 只有当多个 seeds 共享同一对象、同一条件、同一动作、同一核心结果、同一观测方式，并且不会掩盖任何高风险差异时，才允许合并为一条 testcase；否则必须拆开。
- 如果某条 testcase 仍然看起来像“角度标题”而不是“可执行 testcase”，必须回到 seeds 阶段继续拆。
- 渲染时优先保证“原子性”和“覆盖密度”，不要为了篇幅好看把多个核心结果或多个高风险差异合并成一条。

## 6.6 合并最终版

将 `working_dir/testcase_base.md` 与各个 `working_dir/testcase_delta_*.md` 合并为 `working_dir/testcase_final.md`。

合并规则：

- 内容等价时，保留表达更清晰、步骤更具体的一条。
- 视角互补时，保留两条或合并为一条更完整的 case，但不能破坏“一条 case 只验证一个核心结果”的原则。
- 需求中明确存在、但主稿和各个补缺专家都遗漏的点，必须补写。
- `coverage_expansion_plan` 中仍未被主稿或补缺专家承接的点，必须补写。
- `must_pair_paths` 和 `tool_required_paths` 在合并后必须逐项对账，确认已经显式落到最终 case。
- 不要丢失已有的关键执行步骤。

## 6.7 reviewer 准备复核输入

在向用户输出前，必须把 `working_dir/testcase_final.md` 作为 review 对象，再做一轮“reviewer 专家”复核；这一轮不是润色，而是像测试用例评审人一样查缺补漏、纠正范围污染并回修终稿。

复核时必须重新对照以下输入，而不是只看最终 case：

- 用户原始需求文档
- Step 3 的 Drive 补充文档
- Step 4 已确认的 Jira 结果
- Step 5 已确认的测试对象、工具矩阵、测试角度、历史矩阵补全结果、`coverage_expansion_plan`
- 如有必要，再回看 `../smartx-docs-download/markdown_docs` 中直接相关的本地文档

要求：

- 先完成输入对齐，再进入后续 reviewer 子步骤，不要边看终稿边随意补判。
- 如果关键输入缺失，例如未确认的 Jira 结果、未确认的 `coverage_expansion_plan`、缺失的补充文档，先回到前序步骤补齐，再继续 reviewer。

## 6.8 reviewer 复核业务范围与覆盖

先检查终稿是否覆盖了正确范围，且没有遗漏高风险业务路径。

复核重点：

1. 是否遗漏需求中明确存在的对象、条件、状态、特例、生命周期动作。
2. 是否把本应拆成多条 case 的对象差异、条件差异、输入差异、状态差异、入口差异、结果差异或观测差异粗暴合并成一条“看起来覆盖了”的大 case。
3. 是否把“系统服务 / 插件 / 上下游依赖能力”误写成目标 feature 本体；若本次需求主体不是这些能力，只允许保留必要联动回归，不得喧宾夺主。
4. 是否遗漏失败回滚、残留清理、状态恢复、对账重试、升级继承等高风险路径。
5. 是否遗漏需求中的差异化分支，例如：
   - 新建集群 vs 升级集群
   - 集群级规则 vs 主机级规则
   - 普通集群 vs VMware / SCVM / 双活特例
   - 默认允许 vs 默认拒绝
6. 是否遗漏 `tool_required_paths` 中要求显式出现的 UI / API / CLI / 脚本 / 日志 / 告警 / 任务 / 抓包 / trace / 报表等执行或观测手段。
7. 是否遗漏 `must_pair_paths` 中要求成对出现的成功 / 失败、修改前 / 修改后、启用 / 停用、升级前 / 升级后、故障中 / 恢复后等路径。
8. 是否存在历史 Jira / 设计文档 / 本地样本源 / 实时近邻样本已经暴露的高风险场景，但终稿没有体现。
9. 是否存在越界内容：与当前 feature 仅弱相关、只能算背景信息的内容，不应大面积进入最终用例。
10. 是否存在 `test_dimension_coverage` 中被标记为 `must_cover` 的维度，但终稿没有落点。

## 6.9 reviewer 复核原子性与结构格式

在业务范围确认后，再单独检查原子性、可执行性与输出结构，避免把结构问题埋在业务检查里一起漏掉。

复核重点：

1. 是否满足“原子性”：
   - 一条 case 是否只验证一个核心结果
   - 是否明确写出了对象、条件、动作、预期结果、观测方式
   - 是否仍然停留在“主题/角度/模块标题”层，而不是可执行 testcase
   - 是否把多个变量组合、多层验证或多种结果混在同一条 case 中
2. 是否存在“看起来覆盖了，其实粒度过粗”的情况；若一条 case 混了多个核心结果，或把多个高风险差异轴合并到同一条 case 中，必须拆开。
3. 是否已经对 `must_split_axes` 做到逐项兑现，而不是只做到“有一个原子 case”。
4. 是否与 `references/testrail_default.md` 的结构模板对齐：
   - `## 模块 -> ### 子模块 -> #### 用例` 的层级和编号是否完整
   - 每个模块、子模块、用例是否都有明确名称
   - 每个子模块下是否显式包含 `描述：`
   - 每条用例下是否显式包含 `描述：`、`【Step1】`、`【Step2】`、`【Step3】`
   - 是否存在缺编号、缺名称、缺描述、缺 Step 的格式缺口

## 6.10 reviewer 回修与输出规则

按 6.8 和 6.9 的结果统一回修终稿，再决定是否可以对用户输出。

输出与处理规则：

- 先在内部完成 review，再直接修改 `working_dir/testcase_base.md`、各个 `working_dir/testcase_delta_*.md`、`working_dir/testcase_final.md`，不要把未修订的草案直接交给用户。
- 如果 reviewer 发现终稿缺项、范围错误、优先级错位或粒度不合适，必须先回修终稿，再继续。
- 如果 reviewer 发现终稿格式未对齐 `references/testrail_default.md`，必须先补齐编号、名称、描述和 Step，再继续。
- 如果 reviewer 发现 `coverage_expansion_plan` 中仍有未兑现项，必须先回修终稿，再继续。
- 如果 reviewer 发现终稿中的某些 case 仍然停留在“主题大纲”层，而不是原子 testcase，必须回到 seeds 阶段重拆，再重新渲染。
- 如果 reviewer 发现终稿中的某些 case 虽然已经原子，但仍把多个高风险拆分轴揉在同一条里，必须回到 seeds 阶段继续拆细，再重新渲染。
- 只有当 reviewer 发现“关键需求本身存在歧义，且不澄清会明显影响最终 case 正确性”时，才向用户提问。
- 最终返回给用户的必须是 **review 后的 `working_dir/testcase_final.md` 正文**，而不是未复核版本。

最终对用户的输出要求：

- 以 `【测试用例处理完成】` 开头。
- 直接展示 review 后的最终测试用例正文。
- 除非用户额外要求，否则不要附加解释性长文。

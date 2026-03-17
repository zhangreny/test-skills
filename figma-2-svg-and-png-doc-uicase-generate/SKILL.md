---
name: figma-2-svg-and-png-doc-uicase-generate
description: 根据需求文档和 Figma 设计稿生成以 UI 为核心、但覆盖深度不能只停留在截图层的测试用例。需求输入既支持本地 `.docx`、`.pdf`、`.md` 文件路径，也支持一个或多个 Google Doc URL；若收到 Google Doc URL，先提取 `/d/` 与下一个 `/` 之间的文档 id，下载到系统 Downloads 下带时间戳的 `figma-ui-download-*` 目录，再纳入后续分析。之后识别 Figma 中每个最大场景块并为每个场景准备 PNG 与 SVG，再结合历史近邻 testcase 学习、成对路径、交叉场景、工具与观测矩阵、coverage_expansion_plan 生成更完整的 UI testcase。适用于“先把 Figma 大场景拆开再写 testcase”“按最大 layer 分别导出 PNG 和 SVG”“希望减少整页 Figma 精读、改为逐场景分析”“限制 Figma MCP 读取次数并控制预算”“想让 UI 用例生成继承 testcase-generate 的深度思考、历史学习和交叉覆盖”等请求。
---

# Figma 2 SVG And PNG Doc UI Case Generate

按以下顺序执行：

**Step 1：盘点输入 -> Step 2：先分析需求文档并让用户确认 -> Step 3：识别最大场景块并按场景准备 PNG + SVG -> Step 4：基于场景资产做 UI 场景分析并确认 -> Step 5：补历史近邻、工具矩阵与 coverage_expansion_plan -> Step 6：先出主稿，再补缺并 review 终稿**

目标不是直接通读整页 Figma，也不是拿文档和几张 PNG 直接堆 testcase。
这份 skill 必须同时解决 3 个问题：

1. 把长白板拆成有限个最大场景块。
2. 把每个场景的 UI 证据来源讲清楚：文档、PNG、SVG、推断分别是什么。
3. 把 testcase-generate 中“历史近邻学习、成对路径、交叉场景、工具/观测、coverage_expansion_plan”的深度约束补进来，避免产出只像需求点罗列。

额外强制目标：

- 不只保证“场景覆盖率”，还要尽量提高“用例覆盖率”。
- 不要把“已经有原子 case”当成停止条件；只要还能继续按对象差异、条件差异、状态差异、结果差异、观测差异或交叉场景差异拆成更细的独立 case，就继续拆。

每个场景优先保留两份资产：

- `scene.png`：用于视觉回看、布局确认、颜色和状态差异判断。
- `scene.svg`：用于结构理解、文本抽取、图层关系和相对位置分析。

如果当前会话的 Figma MCP 不支持“直接把任意节点导出为 SVG”，不要假装 SVG 已经拿到。必须明确记录哪些场景已经得到真实 SVG，哪些场景仍需通过 Figma 原生导出或现成脚本补齐。

## Step 1：盘点输入

先把用户输入归一化，再围绕文档、Figma 链接和已有截图做轻量盘点。

### 1.1 输入归一化

需求文档入口支持两类，且都允许一次提供多个：

- 本地需求文件路径：例如 `.docx`、`.pdf`、`.md`。
- Google Doc URL：例如 `https://docs.google.com/document/d/1kRbOppUeD34YnqnwL2HdvZ9NW4iVQSoGitHNjOxycBo/edit?tab=t.7q8myxjn8ndc`。

如果收到 Google Doc URL，先按下面规则处理，再进入后续文档分析：

1. 从 URL 中提取文档 id，规则是取 `/d/` 紧接其后、直到下一个 `/` 之前的内容。
2. 为本轮任务创建下载目录：系统 `Downloads` 目录下的 `figma-ui-download-YYYYMMDD-HHMMSS`。
3. 下载目录按当前操作系统取值：
   - Windows：`%USERPROFILE%\Downloads\figma-ui-download-YYYYMMDD-HHMMSS`
   - macOS：`~/Downloads/figma-ui-download-YYYYMMDD-HHMMSS`
   - Linux：`~/Downloads/figma-ui-download-YYYYMMDD-HHMMSS`
4. 参照 `google-drive-file-download` skill 的逐 id 下载方式，对每个 Google Doc id 单独执行一次下载，不要把多个 id 合并到一次调用里；每次调用都只传两个核心参数：当前 `id=<doc_id>`，以及 `output=<系统 Downloads>/figma-ui-download-YYYYMMDD-HHMMSS`。
5. 下载完成后，把下载得到的文档文件加入本轮“会参与分析的需求文档”列表，与用户直接给出的本地文件一起继续后续步骤。

如果用户同时给了本地需求文件和 Google Doc URL，两类输入都要保留，并在盘点结果中区分“用户原始本地文件”和“从 Google Doc URL 下载得到的文件”。

围绕归一化后的文档、Figma 链接和已有截图做轻量盘点：

- 展示会参与分析的 `.docx`、`.pdf`、`.md` 文件。
- 若某些文件来自 Google Doc URL，额外标出原始 URL、提取出的 `doc_id` 和下载目录。
- 标出 Figma URL、`fileKey`、`node-id`。
- 标出用户是否已经提供部分 PNG 或 SVG；若有，记录文件与场景名的对应关系。
- 记录用户额外约束：
  - 是否限制 Figma MCP 读取次数。
  - 是否要求优先靠 SVG 做结构学习。
  - 是否要求 TestRail 风格输出。
  - 是否要求你先判断哪个 layer 才是“最大场景块”。
  - 是否要求继承历史 testcase 风格或补更多交叉场景。
- 区分原始需求文档和补充说明。

这一阶段只盘点，不直接写 testcase。

## Step 2：先分析需求文档并让用户确认

先读文档，再进 Figma。
默认产出以下结构化结论：

1. 功能目标。
2. 涉及页面或入口。
3. 关键对象。
4. 关键数值口径。
5. 关键展示字段。
6. 关键校验、限制和报错。
7. 已知状态变化。
8. 当前不确定点。
9. 依据来源。

重点提前提炼：

- 哪些 UI 入口会受影响。
- 哪些数值需要展示、比较、计算、扣减、归还或汇总。
- 哪些文案属于提示、说明、错误、状态标签、tooltip 或 footnote。
- 哪些状态会切换，例如正常、不足、禁用、隐藏、过期或半透明。
- 哪些规则是单对象维度，哪些是群组维度，哪些是全局汇总维度。
- 哪些结论未来需要由 PNG 视觉证据确认，哪些必须等待 SVG 结构证据确认。

继续前，必须把文档分析结果展示给用户确认。

## Step 3：识别最大场景块并按场景准备 PNG + SVG

### 3.1 默认策略

优先少读、分块读，不要围绕整页长白板做一次性重分析。默认顺序：

1. 先用一次 `get_metadata` 看根节点或目标 section 的结构。
2. 识别候选“最大场景块”。
3. 对每个场景分别准备 `PNG` 和 `SVG`。
4. 用这两份资产做场景级 UI 分析。
5. 只有在 PNG 和 SVG 仍无法解释关键差异时，才补最少量的 `get_design_context`。

### 3.2 “最大场景块”识别规则

优先把下面对象当作导出单元：

- 独立白底大 `Frame` 或 `Section`，内部已包含完整页面、弹窗、表单或卡片。
- 独立业务场景块，内部已包含标题、主体区、关键字段和操作区。
- 长白板中的多个并列白块，每个白块单独处理，不把整板合并成一个超长场景。

不要把下面对象当作独立导出单元：

- 纯标题标签。
- 便利贴、批注、说明连线。
- 单个按钮、输入框或单个 icon。
- 仅用于说明选中态的辅助元素。

### 3.3 场景资产准备规则

每个场景的目标产物是：

- `scene-name.png`
- `scene-name.svg`

执行规则：

1. 优先选择该场景最外层的 `Frame` 或 `Section`。
2. 一个大容器里如果并排放了多个独立白块，改选每个子 `Frame`。
3. PNG 优先用 `get_screenshot` 获取。
4. SVG 优先使用“节点级真实导出”路径；若当前 MCP 没有该能力，则明确转入 Figma 原生导出或已有脚本，不得把截图、metadata 或 design context 冒充 SVG。
5. 若用户已经手工导出过 PNG 或 SVG，直接复用，不重复下载。

### 3.4 MCP 预算规则

把预算当作硬约束。默认公式：

- `1` 次：根节点或目标 section 的 `get_metadata`
- `N` 次：每个最大场景块各一次 PNG 获取
- `N` 次：每个最大场景块各一次 SVG 获取；仅在当前导出路径真实存在时成立
- `0-2` 次：只在双格式资产仍不足以解释关键差异时补 `get_design_context`

结论：

- `N` 个大场景的双格式标准预算通常是 `2N + 1`。
- 如果当前环境没有真实 SVG 导出能力，则自动化 MCP 预算会退化为 `1 + N (+0-2)`。
- 预算退化时必须给出“待补 SVG 场景清单”，并在后续 testcase 中显式标注哪些结论缺少 SVG 证据。

## Step 4：基于场景资产做 UI 场景分析并确认

围绕每个场景完成以下分析：

1. UI 场景名称。
2. 场景入口。
3. 关键控件或信息块。
4. 数值展示位置。
5. 数值比较规则。
6. 正常态展示。
7. 异常态展示。
8. 状态变化。
9. 报错位置与提示方式。
10. 哪些结论来自 PNG 视觉确认。
11. 哪些结论来自 SVG 结构理解。
12. 哪些结论仍只是文档推断。

同时显式产出：

- `scene_asset_matrix`
- `ui_scene_matrix`
- `scene_to_requirement_map`

继续前，必须把以下内容展示给用户确认：

1. 已识别的大场景列表。
2. 每个场景是否已拿到真实 PNG。
3. 每个场景是否已拿到真实 SVG。
4. 哪些场景仍待补导出。
5. 每个场景的关键对象、数值、展示、报错和状态差异。

## Step 5：补历史近邻、工具矩阵与 coverage_expansion_plan

这一阶段是本 skill 相比“只看文档 + Figma”最重要的加深步骤。
不要在 Step 4 后直接生成 testcase。

### 5.1 测试对象核对

进入 testcase 生成前，先列出“独立测试对象表”：

| 测试对象 | 来源 | 是否已有对应测试角度 |
|----------|------|----------------------|
| 对象名 | 文档 / PNG / SVG / 推断 | 是 / 否 |

核对重点：

- 文档直接提到的对象。
- Figma 中可见的独立页面、弹窗、卡片、错误区域、状态块。
- 文案变化对象、数值变化对象、校验变化对象。
- 生命周期动作：创建、编辑、删除、启用、停用、扩容、缩容、归还、升级、恢复。

### 5.2 建立 UI 执行工具与观测矩阵

即使是 UI 用例，也不能只写“点了以后结果正确”。
必须显式列出：

- `execution_tool_matrix`
- `observability_matrix`
- `tool_required_paths`

推荐格式：

| 测试角度 / 对象 | 关键动作 | 执行工具 | 观测手段 | 预期信号 | 是否已有覆盖 |
|----------------|----------|----------|----------|----------|--------------|
| 角度名 / 对象名 | 动作名 | UI / API / CLI / 脚本 | 卡片 / tooltip / footer / 日志 / 告警 / 任务 / 计数 / 报表 | 关键验证信号 | 是 / 否 |

要求：

- 如果结果不只体现在 UI，要补齐日志、告警、任务状态、计数、报表、API 或 CLI 等观测方式。
- 如果某个关键测试角度没有明确的执行工具或观测手段，要显式标记为缺口。

### 5.3 学习历史近邻 testcase

默认必须读取并遵循：

- `../testcase-pattern-learning/SKILL.md`
- `../testcase-pattern-learning/tutorial-all-groups/all-groups-common.md`

如 feature 属于网络 / 安全 / 端口控制 / 连通性 / 转发 / VPC / DFW / LB 类，再额外读取：

- `../testcase-pattern-learning/tutorial-all-groups/network-group.md`

如需要补具体方法，再按需读取：

- `../testcase-pattern-learning/references/historical-neighbor-learning.md`
- `../testcase-pattern-learning/references/workflow.md`

执行规则：

1. 先找本地近邻样本，优先从 `../testcase-pattern-learning/former_cases/15_SDN` 中读取同域、同对象、同动作、同故障模式的 suite。
2. 先看结构，再看标题，再看代表性 case，不要一上来通读整份历史 suite。
3. 如果用户明确要求更强 coverage，或本地样本仍不足以稳定补矩阵，再继续按 `testcase-generate` 的思路补实时 / 近期 TestRail grouped export。
4. 历史样本只用于学习矩阵维度、成对路径、工具/观测习惯、高频漏测点，不直接照抄旧业务内容。

本步骤至少要产出：

1. `historical_neighbors`
2. `matrix_dimensions`
3. `must_cover_detail_points`
4. `can_sample_dimensions`
5. `must_not_sample_dimensions`
6. `paired_paths`
7. `tool_observability_clues`
8. `must_split_axes`

重点检查：

- 历史近邻是否稳定把“成功 / 失败”“新集群 / 旧集群”“有额度 / 无额度”“唯一对象 / 非唯一对象”“修改前 / 修改后”“故障中 / 恢复后”写成成对路径。
- 历史近邻是否对边界值做了显式展开，而不是只写笼统的“额度不足”。
- 历史近邻是否把交叉功能场景拆成“只影响 A / 只影响 B / 同时影响 A+B”。
- 历史近邻是否把原本看似“已经原子”的 case 继续按状态、对象、入口、数值区间或观测方式拆成更多独立 case；若有，当前 feature 默认继承这种细粒度写法。

### 5.4 生成 coverage_expansion_plan

不要把前面的矩阵只当分析笔记。
在正式生成 testcase 前，必须收敛成一份显式的 `coverage_expansion_plan`。

至少包含：

1. `requirement_points_to_cover`
2. `figma_scene_points_to_cover`
3. `historical_inherited_points`
4. `must_pair_paths`
5. `tool_required_paths`
6. `must_expand_dimensions`
7. `sampled_dimensions`
8. `unsupported_dimensions`
9. `case_granularity_strategy`

要求：

- 每个需求点、场景点、历史继承点都要能映射到后续某组 case。
- 如果某个维度只允许抽样，要写明为什么可抽样。
- 如果某个维度必须显式展开，后续不得只写成一句总括 case。
- 每个 `must_split_axes` 都要在 `case_granularity_strategy` 中写清楚准备拆成哪些独立 case 类别；默认宁可多几条细 case，也不要少几条粗 case。

### 5.5 向用户展示并确认

继续前，必须向用户展示并确认：

1. 测试对象核对表
2. `execution_tool_matrix`
3. `observability_matrix`
4. 建议测试角度
5. `historical_neighbors`
6. `matrix_dimensions`
7. `must_cover_detail_points`
8. `can_sample_dimensions`
9. `must_not_sample_dimensions`
10. `must_split_axes`
11. `coverage_expansion_plan`
12. `case_granularity_strategy`
13. 当前仍存在的测试设计疑点

不要把历史学习结果、工具矩阵和 `coverage_expansion_plan` 只留作内部信息。

## Step 6：先出主稿，再补缺并 review 终稿

### 6.1 生成 testcase 主稿

先生成 `ui_case_seeds.md`，再据此生成 `testcase_base.md`，不要直接把第一版当终稿。
主稿必须显式吸收：

- Step 2 的文档分析结果
- Step 4 的场景资产和 UI 场景矩阵
- Step 5 的历史近邻学习结果
- `coverage_expansion_plan`

`ui_case_seeds.md` 中每条 seed 至少包含：

1. `scene`
2. `feature_area`
3. `object`
4. `precondition`
5. `action`
6. `expected_result`
7. `observability`
8. `evidence_source`
9. `priority`

要求：

- 一条 case 只验证一个核心结果。
- 不要直接从“页面/弹窗/卡片/异常态/交叉场景”这些主题词生成 testcase；必须先拆成“对象 + 条件 + 动作 + 单一结果 + 观测方式”的原子 seed。
- 上述原子 seed 只是下限；如果 seed 仍混合了多个对象、多个条件区间、多个状态前后、多个数值分段、多个入口、多个结果信号或多个观测方式，必须继续拆。
- 标题尽量同时体现对象、条件、结果。
- 主稿必须覆盖主流程、异常、边界、状态变化和交叉组合。
- 如果某条 case 依赖 UI 之外的观测手段，要在 `描述：` 或 `【Step3】` 中显式说明。
- 如果某个结论缺少真实 SVG，只能把它写成“待结构补证”或“基于 PNG/文档推断”，不要假装已经完成结构验证。
- 如果当前输出仍像“测试角度大纲”而不是原子 case，必须继续细化 `ui_case_seeds.md`，不能直接进入终稿阶段。
- 如果当前输出已经原子，但仍然没有把高风险拆分轴展开成足够细的独立 case，也不能直接进入终稿阶段。

优先使用 TestRail 风格结构，参考 `references/template.md`。

### 6.2 按缺口生成增量补丁

主稿完成后，再补做以下增量检查，不要让多个检查者重写整份 testcase：

- `testcase_delta_ui_states.md`
  - 只补场景状态、显隐、禁用、过期、半透明、tooltip、footer 等 UI 差异遗漏
- `testcase_delta_cross_feature.md`
  - 只补交叉对象、组合文案、只影响 A / 只影响 B / 同时影响 A+B 的遗漏
- `testcase_delta_historical_regression.md`
  - 只补历史近邻中反复出现的边界值、成对路径、回归点、升级/恢复闭环
- `testcase_delta_tools_observability.md`
  - 只补工具、观测、日志、任务、计数、报表等容易漏掉的验证路径

每个增量补丁都要显式标明自己覆盖的是 `coverage_expansion_plan` 中的哪些缺口。
每个增量补丁默认优先补“主稿里已经提到但拆得不够细”的缺口，而不只是补全新章节。

### 6.3 合并与 reviewer 复核

合并 `testcase_base.md` 与各个 `testcase_delta_*.md` 后生成 `testcase_final.md`。
reviewer 复核时必须重新对照：

- 原始需求文档
- 已确认的文档分析结果
- 已确认的场景资产结果
- 已确认的 UI 场景分析结果
- 已确认的测试对象、工具矩阵、历史矩阵补全结果
- `coverage_expansion_plan`
- `references/template.md`

reviewer 必查：

1. 是否漏掉文档里明确存在的入口、对象、条件、状态。
2. 是否漏掉 PNG 中可见的数值、文案、报错、状态差异。
3. 是否漏掉 SVG 中可解析的层级、文本、相对位置和结构分组。
4. 是否把“没有真实 SVG”的场景误当作已完成结构分析。
5. 是否满足“原子性”：
   - 一条 case 是否只验证一个核心结果
   - 是否明确写出了对象、条件、动作、预期结果、观测方式
   - 是否还停留在“场景标题/页面标题/主题标题”层，而不是可执行 testcase
   - 是否把多个变量、多层验证或多个结果混在同一条 case 中
6. 是否虽然已经原子，但仍把多个高风险拆分轴合并进同一条 case，导致用例覆盖率不足。
7. 是否漏掉边界值、切换链路、对象组合和一致性回归。
8. 是否漏掉 `must_pair_paths` 中要求成对出现的路径。
9. 是否漏掉 `tool_required_paths` 中要求显式出现的执行或观测手段。
10. 是否存在历史近邻已经暴露的高风险场景，但终稿没有体现。
11. 是否把本该显式展开的维度错误地降成了抽样。

如 reviewer 发现缺项、错项或粒度问题，先回修主稿或增量补丁，再生成 `testcase_final.md`。

如果 reviewer 发现任何 case 仍停留在“页面大纲”层，或一条 case 混入多个核心结果，必须先回到 `ui_case_seeds.md` 重拆，再重新渲染 `testcase_base.md` 和 `testcase_final.md`。
如果 reviewer 发现任何 case 虽然原子但仍然拆得不够细，必须继续回到 `ui_case_seeds.md` 扩写更多细粒度 seeds，再重新渲染。

最终输出要求：

- 以 `【测试用例处理完成】` 开头。
- 直接展示 `testcase_final.md` 正文。
- 除非用户额外要求，否则不附加长篇过程复述。

## 质量检查

完成前确认：

- 已先读文档，再拆 Figma 场景，而不是先看整页截图。
- 已把长白板拆成多个最大场景块，而不是把整张长图直接拿来写用例。
- 已明确区分真实拿到的 PNG、真实拿到的 SVG 和仍待补齐的 SVG。
- 已明确说明 Figma MCP 预算使用情况。
- 已输出并等待用户确认过“文档分析确认”“场景资产确认”“测试设计确认”。
- 已补做历史近邻 testcase 学习，而不是只拿文档和场景截图直接生成 case。
- 已显式产出 `execution_tool_matrix`、`observability_matrix`、`historical_neighbors` 和 `coverage_expansion_plan`。
- 已将 `must_pair_paths`、`tool_required_paths`、`must_expand_dimensions` 真正落实到最终 case 或显式标记残余风险。
- 已将 `must_split_axes` 与 `case_granularity_strategy` 真正落实到最终 case，而不是停留在设计确认阶段。
- 已先生成原子级 `ui_case_seeds`，再渲染 `testcase_base.md` 和 `testcase_final.md`，而不是直接从场景分析生成大纲式 testcase。
- 已显式完成“原子性检查”：确认每条 case 只验证一个核心结果，且都具备对象、条件、动作、预期结果、观测方式。
- 已显式完成“覆盖密度检查”：确认不会因为“已经有原子 case”就提前停止，且高风险拆分轴已继续细化成足够多的独立 case。
- 如 reviewer 发现任何 case 仍停留在页面/主题大纲层或混合多个核心结果，已回到 seeds 阶段重拆并重新渲染。
- 如 reviewer 发现任何 case 虽然原子但仍拆得不够细，已回到 seeds 阶段继续扩写并重新渲染。
- 已先出主稿，再做增量补缺和 reviewer 复核。

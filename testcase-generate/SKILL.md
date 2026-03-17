---
name: testcase-generate
description: 根据用户提供的需求文档路径、目录路径或 Google Docs URL 生成 SmartX 功能测试用例。适用于“生成测试用例”“根据文档写测试点”“输出 TestRail 格式用例”等请求。流程包括：先归一化输入并在需要时下载 Google Docs、再校验与盘点输入文件、先单独完成文档分析与用户确认、准备相关 Drive 资料、补充查询 Jira 历史 issue、再结合本地 SmartX 文档确认测试角度，最终输出符合 TestRail 结构的测试用例。
---

# Testcase Generate

按以下顺序执行：

**Step 0：归一化输入 -> Step 1：盘点输入文件 -> Step 2：先分析原始需求并让用户确认 -> Step 3：补齐相关 Drive 文档 -> Step 4：查询并摘要 Jira 并让用户确认 -> Step 5：整合资料、补齐工具与历史矩阵并统一确认测试设计 -> Step 6：生成、补缺并 review 测试用例**

---

## Step 0：归一化输入

先判断用户给的是哪一类输入，再统一转换为可继续处理的本地文件列表。

支持的输入类型：

- 单个需求文档路径
- 包含需求文档的目录路径
- 一个或多个 Google Docs URL
- 上述几类输入的混合

### 0.1 处理 Google Docs URL

如果用户输入中包含一个或多个 Google Docs URL，先逐个提取文档 id，再执行下载，不要直接把 URL 留到后续 Step 1。

Google Docs 文档 id 提取规则：

- 对形如 `https://docs.google.com/document/d/<ID>/edit?...` 的 URL，取 `/d/` 后、下一个 `/` 前的字符串作为文档 id。
- 例如 `https://docs.google.com/document/d/1kRbOppUeD34YnqnwL2HdvZ9NW4iVQSoGitHNjOxycBo/edit?tab=t.7q8myxjn8ndc` 的 id 为 `1kRbOppUeD34YnqnwL2HdvZ9NW4iVQSoGitHNjOxycBo`。
- 如果某个 URL 不符合该模式，必须显式说明哪个 URL 无法提取 id，并停止使用该 URL 继续后续流程。

### 0.2 下载 Google Docs 到本地

读取并遵循 `../all-related-file-preparer-4-testcase-generate/google-drive-file-download/SKILL.md`，但此处的目标目录不要由用户额外指定，而是自动使用当前操作系统的系统 `Downloads` 目录下新建一个时间戳文件夹。

目标目录规则：

- Windows：`%USERPROFILE%\\Downloads\\testcase-download-YYYYMMDD-HHMMSS`
- macOS：`$HOME/Downloads/testcase-download-YYYYMMDD-HHMMSS`
- Linux：`$HOME/Downloads/testcase-download-YYYYMMDD-HHMMSS`
- 例如：`testcase-download-20260317-114005`

调用要求：

- 将提取出的 Google Docs 文档 id 列表逐个传给下载技能，不要在单次调用里混传多个 id。
- 传递的目标目录应是“系统 Downloads 目录 + 当前时刻时间戳文件夹”。
- 若用户同时还给了本地文件路径或目录路径，则将下载结果与这些本地输入合并，作为后续 Step 1 的输入集合。
- 若下载失败，必须明确指出失败的 id 与错误，不能跳过失败项继续假设文档已存在本地。

### 0.3 归一化输出

Step 0 结束后，后续步骤看到的输入应统一为“本地文件路径列表或目录列表”，不再把原始 Google Docs URL 直接传入 Step 1 之后的分析、Drive 搜索与 Jira 搜索流程。

---

## Step 1：盘点输入文件

围绕 Step 0 归一化后的原始需求文档或目录做一次轻量盘点：

- 展示目录结构或等价的文件清单。
- 明确标出会参与后续分析的 `.pdf`、`.docx`、`.md` 文件。
- 标记哪些是“原始需求文档”，哪些是同目录下的补充文件。

这一阶段只做盘点，不先调用 `all-related-file-preparer-4-testcase-generate`。

---

## Step 2：先分析原始需求文档并让用户确认

### 2.1 调用根目录文档分析技能

读取并严格遵循 `../smartx-doc-2-product-and-keywords/SKILL.md`。

- 输入优先使用“原始需求文档”。
- 如果用户一次给了多个文件，先判断它们是否都指向同一个 feature。
- 让该技能返回结构化结果，包括摘要、产品、关键词、证据和阻塞项。
- 优先使用该技能返回的标准字段：
  - `core_keywords`：供用户确认的核心关键词，控制在 1-2 个，用于代表 feature 主体。
  - `expansion_keywords`：供后续 Drive / Jira / TestRail 检索扩展使用的检索词包，按类别组织，至少覆盖：
    - 对象词
    - 动作词
    - 症状词
    - 结果层词
    - 依赖链路词
    - 工具 / 观测词
    - 版本 / 兼容词
- 如果上游仍只返回旧字段 `selected_keywords`，不要直接进入后续流程；必须先在本步骤内补做一次“关键词契约归一化”：
  - 将 `selected_keywords` 归一化为 `core_keywords`
  - 结合功能摘要、产品关系、文档证据，补齐 `expansion_keywords`
  - 只有在 `core_keywords` 和 `expansion_keywords` 都齐备后，才能进入 Step 2.2 及之后的流程
- `expansion_keywords` 的目标不是压缩成极少几个词，而是保留一个可复用的检索词包，避免后续检索只靠 1-2 个短词导致 coverage 不足。

### 2.2 需要澄清时的强制规则

如果候选产品数量大于 1，不要输出“只能机器解析的纯 JSON”。必须用当前运行环境可直接回答的简短澄清方式向用户提问，然后停止等待用户选择。

推荐形式：

1. 先用一句话说明需要确认什么。
2. 用编号列表给出候选项。
3. 明确告诉用户“回复编号或产品名即可”。

例如：

```text
这个功能最相关的 SmartX 产品还不够确定，请帮我确认：
1. 产品1
2. 产品2
3. 产品3
请直接回复编号或产品名。
```

如果候选核心关键词数量大于 2，同样不要输出“只能机器解析的纯 JSON”。必须用当前运行环境可直接回答的简短澄清方式向用户确认 1-2 个核心关键词，然后停止等待用户选择。

推荐形式：

```text
以下关键词里，哪些最能代表这篇文档的核心功能？请选择 1-2 个：
1. 关键词1
2. 关键词2
3. 关键词3
4. 你也可以直接回复自己的 1-2 个关键词
请直接回复编号、关键词，或两者组合。
```

这里的强制选择对象仅限 `core_keywords`。`expansion_keywords` 不在这一轮被压缩到 1-2 个，而是保留为后续检索词包。

### 2.3 向用户展示并确认分析结果

在继续之前，显式展示这一轮确认后的分析包：

1. 功能摘要
2. 主体产品及关系
3. 最终 `core_keywords`（1-2 个）
4. `expansion_keywords` 摘要（按类别展示，每类保留最有代表性的 2-5 个）
5. 使用到的原始需求文档
6. 当前仍存在的不确定点

这一轮必须等用户确认或修正。因为后续 Drive 搜索、Jira 搜索和历史 TestRail 检索都会复用这组关键词。
- 如果用户修正了 `core_keywords`，要同步回收并更新 `expansion_keywords`，不要继续沿用旧的扩展词包。

---

## Step 3：准备相关 Drive 文档

读取并严格遵循 `../all-related-file-preparer-4-testcase-generate/SKILL.md`。

调用要求：

- 输入使用 Step 1 的有效文件路径列表。
- 同时把 Step 2 已确认的摘要、产品、`core_keywords`、`expansion_keywords` 作为上游交接结果传入。
- 明确要求该技能跳过重复的产品 / 关键词确认，直接进入 Drive 搜索与下载流程。
- Drive 搜索仅用 `core_keywords` 定位即可，避免搜索过多不相关文件。

本步骤结束时，应拿到：

- 已确认的相关 Drive 文件链接和 id
- 如果用户选择下载，则拿到本地下载结果

---

## Step 4：查询并摘要 Jira 历史 issue

围绕 Step 2 确认后的关键词执行完整 Jira 检索流程，为测试设计补充“历史问题、告警变体、异常场景、回归风险”。

### 4.1 查询输入

复用 Step 2 的：

- `core_keywords`
- `expansion_keywords`
- 功能摘要
- 主体产品信息

默认先使用以下 Jira 配置直接执行检索：

- Jira 站点：`http://jira.smartx.com`
- 用户名：`renyu.zhang`
- 密码：`Zhangry-2001`

如果用户额外提供了新的 Jira 地址或凭据，则以用户最新提供的信息覆盖默认配置。
如果默认配置认证失败、返回 401/403，或搜索结果明显为空且与已知权限不符，要明确说明受阻点，再决定是否继续使用文档和 Drive 资料完成 testcase 流程。

### 4.2 查询策略

至少执行一轮“核心精确搜 + 链路搜 + 症状搜 + 结果层 / 工具搜”，必要时补版本 / 兼容搜：

- 核心精确搜：优先使用 `core_keywords` 做 `summary ~ "关键词"`、`text ~ "关键词"` 或短语查询，先确认是否存在与目标 feature 同名或同对象的历史 issue。
- 链路搜：从 `expansion_keywords` 中补 1-3 个“依赖链路词”后组合查询，例如入口、协议、服务名、对象名、关键端口、关键动作、上下游组件名。
- 症状搜：再从 `expansion_keywords` 中补 1-3 个“失败现象词”做窄搜，例如 `超时`、`失败`、`回退`、`重试`、`不生效`、`无法关联`、`无法迁移`、`VNC`、`白名单`、`访问限制` 等。
- 结果层 / 工具搜：如 feature 依赖日志、告警、报表、计数、任务状态、CLI、API、诊断工具、抓包、trace 等结果信号，从 `expansion_keywords` 中补 1-3 个相关词做查询，补充“如何观测问题”与“哪些工具最容易暴露问题”的线索。
- 版本 / 兼容搜：如果需求涉及版本、平台、架构、升级路径、存量配置或兼容约束，追加 1-3 个“版本 / 兼容词”组合查询。
- 如果主体产品已明确，优先限制到高相关项目或产品线后再搜，降低全库噪声。
- 如果有两个 `core_keywords`，优先做交集查询；如果交集过窄，再拆成单关键词查询并回收高相关结果。
- 如果第一轮结果明显被通用词污染，不要继续堆关键词；应改为更精确的对象词、调用链词、症状词、工具词或版本词重搜。

### 4.3 筛选规则

拿到结果后必须做相关性筛选，不要把全文检索的所有命中都当成有效线索。

优先保留这些 issue：

- 标题或正文直接命中同一对象、同一功能、同一异常现象，且与当前 feature 的主要对象一致。
- 虽然标题不是同名 feature，但问题由“当前 feature 的开关、限制、配置、状态切换或兼容路径”直接触发。
- 明确提到触发条件、恢复行为、误报、回退逻辑、版本回归、兼容性影响、性能退化、pending 卡住、超时或重试异常。
- 属于当前 feature 所在链路的联动问题：目标功能变化后，上下游能力出现失败或行为退化，这类 issue 要保留。

降级为“背景参考”而不是核心相关 issue：

- 主题是上游或下游组件自身的能力建设、功能增强、产品演进，但不是由当前 feature 触发出来的问题。
- 与当前 feature 共享名词或组件名，但本质是在做独立功能支持、接口扩展、配置能力补齐。
- 只能提供背景知识，不能直接转化为“目标 feature 的回归风险或测试点”。

优先剔除这些 issue：

- 只是在长文本里偶然提到关键词，但主题明显无关。
- 只有流程性内容，没有业务或技术关联。
- 与当前 feature 的对象、场景、触发条件、症状、结果层都对不上。
- 查询结果依赖过宽泛关键词命中，无法说明“为什么它会因为当前 feature 而失败”。

### 4.4 输出 Jira 摘要

至少输出两部分：

1. 直接相关 issue 摘要
   - `key`
   - `status`
   - `assignee`
   - `updated`
   - `summary`
   - `why relevant`
2. 可复用到测试设计的结论
   - 典型触发条件
   - 常见误报 / 漏报 / 边界场景
   - 版本或兼容性线索
   - 恢复、重试、状态回收、告警清除等测试点

如果存在“有帮助但不属于目标 feature 直接问题”的结果，可额外增加第三部分：

3. 背景参考 issue
   - `key`
   - `summary`
   - `why background only`

如果没有找到高相关 issue，要明确说明“已查 Jira，但暂无高相关历史问题”，然后继续后续步骤，不要因此中断整个 testcase 流程。

### 4.5 向用户展示并确认 Jira 结果

在继续 Step 5 之前，必须显式向用户展示本轮 Jira 检索结论，并等待用户确认或修正。

确认内容至少包括：

1. 直接相关 issue 摘要
2. 可复用到测试设计的结论
3. 如有的话，背景参考 issue
4. 当前是否存在 Jira 侧仍未澄清的疑点

要求：

- 不要在输出 Jira 摘要后直接进入 Step 5。
- 如果用户认为某些 issue 不相关、遗漏了某些 issue，先按用户反馈修正 Jira 结果，再继续后续步骤。
- Step 5 中的“历史问题与回归风险”必须基于这一轮已确认的 Jira 结果，而不是未确认版本。

---

## Step 5：整合文档、补齐工具与历史矩阵并统一确认测试设计

### 5.1 读取资料

读取以下输入：

- 用户原始需求文档
- Step 3 下载到本地的相关补充文档
- `../smartx-docs-download/markdown_docs` 中与当前 feature 直接相关的本地文档
- Step 4 的 Jira 摘要

读取要求：

- `.md` 直接读取内容。
- `.pdf`、`.docx` 使用当前环境中可行的本地读取方式。
- 如果某个关键文件无法读取，立即说明受阻文件和影响，不要跳过。

### 5.2 完成测试设计分析

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

### 5.3 测试对象核对

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

### 5.4 建立执行工具与观测矩阵

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

### 5.5 学习历史近邻用例并补全矩阵

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

要求：

- 如果历史样本不足以支持矩阵补全，要明确说明“不足在哪里”，而不是强行脑补
- 如果历史样本与当前需求冲突，以当前需求为准
- 如果本地样本源与实时 / 近期 TestRail 源不一致，要明确说明差异点；命名和当前团队写法优先参考实时 / 近期 TestRail 源，领域矩阵和高频漏测点优先吸收高质量本地样本源，但都不能覆盖当前需求本身
- 这一轮的目标是“补细节”，不是“扩大范围”

### 5.6 生成 coverage_expansion_plan

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

要求：

- `coverage_expansion_plan` 不是内部笔记，而是后续生成和 reviewer 复核的直接对账依据。
- 每个 `must_cover_detail_points`、`paired_paths`、`tool_required_paths` 都必须能在 `coverage_expansion_plan` 中找到落点。
- 如果某个需求点、高风险点或历史继承点还找不到对应 case 承接位置，要先显式标记为缺口，而不是默认“生成时自然会补到”。
- 如果某个维度被标记为可抽样，要写明“为什么可抽样”，避免把本该展开的高风险差异维度误判为低优先级。

### 5.7 输出测试角度与历史矩阵补全结果，并等待确认

向用户展示建议测试角度，以及 Step 5.5 学到的历史矩阵补全结果，再进入 Step 6。

这一轮确认时至少同时展示：

1. 测试对象核对表
2. `execution_tool_matrix` 与 `observability_matrix`
3. 建议测试角度
4. `historical_neighbors`
5. `matrix_dimensions`
6. `must_cover_detail_points`
7. `can_sample_dimensions`
8. `must_not_sample_dimensions`
9. `coverage_expansion_plan`
10. 当前仍存在的测试设计疑点

要求：

- 测试角度按主题分组，而不是按文件分组。
- 优先给出能直接指导生成 case 的视角，如“基础配置与展示”“告警触发与清除”“异常恢复与误报控制”“升级与兼容”。
- 不要把 Step 5.5 的历史学习结果只留作内部信息，必须与测试角度一起展示给用户确认。
- 不要把工具矩阵和 `coverage_expansion_plan` 只留作内部信息，必须与测试角度一起展示给用户确认。
- 必须等待用户确认后再生成最终用例。

---

## Step 6：生成、补缺并 review 测试用例

### 6.1 先参考历史模式，但不被模式绑死

生成前先检查 `../testcase-pattern-learning/tutorial-all-groups`，并复用 Step 5.4 的工具矩阵、Step 5.5 的历史近邻学习结果以及 Step 5.7 已确认的测试设计与 `coverage_expansion_plan`。

规则：

1. 优先找与当前 feature 高相关的模式文档。
2. 先阅读 `../testcase-pattern-learning/tutorial-all-groups/all-groups-common.md`，获取所有组通用的拆点、粒度、命名和覆盖规则。
3. 再根据当前 feature 所属组别，按需阅读 `../testcase-pattern-learning/tutorial-all-groups` 下对应组的补充文档；如果当前只有通用文档，则只使用通用文档。
4. 如果 feature 属于网络 / 安全 / 端口控制类，再阅读 `../testcase-pattern-learning/tutorial-all-groups/network-group.md`。
5. 如果 Step 5.5 已从本地样本源或实时 / 近期 TestRail 源提炼出细节矩阵，生成时必须显式吸收这些矩阵结论，而不是只复用抽象 pattern。
6. 模式文档用于补充拆点、粒度、命名和覆盖维度；历史近邻用例用于补充矩阵细节、正反路径、高频漏测点、工具 / 观测习惯。
7. `coverage_expansion_plan`、`tool_required_paths`、`must_pair_paths` 不是展示材料，生成时必须显式落实到具体 case 或 case 分组。
8. 当前需求与模式文档或历史样本冲突时，以当前需求为准。

### 6.2 输出格式要求

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

### 6.3 先生成原子 case seeds

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
- `case_seed` 的最小粒度应接近“对象 + 条件 + 动作 + 单一结果 + 观测方式”。
- `case_seed` 允许暂时不按最终 markdown 结构书写，但必须足够原子，能够稳定渲染为一条 testcase。
- `coverage_expansion_plan` 中的每个需求点、风险点、历史继承点，都必须先映射到一个或多个 `case_seed`，再进入最终 markdown 生成。
- 如果当前输出仍像“主题大纲”而不是原子种子，必须继续拆分，不能直接进入下一步。

### 6.4 执行有上限的补缺循环

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
- 连续 1 轮未发现新的高价值缺口
- 或达到最大 3 轮补缺

循环约束：

- 不允许写开放式“继续补到满意为止”的循环，必须有明确停止条件和最大轮数。
- 每轮循环的目标是“继续拆细、继续补缺”，不是再生成一版新的大纲。
- 如果某类 feature 天然是矩阵型需求，应优先补对象差异、条件差异、结果差异，而不是只增加新的章节标题。
- 如果某个主题经检查仍无法拆成原子 seeds，要明确说明缺少了什么输入，而不是用笼统 case 顶替。

### 6.5 从 seeds 渲染主稿与补缺增量

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
- 如果多个 seeds 仅是同一结果的组成部分，可以合并为一条 testcase；否则必须拆开。
- 如果某条 testcase 仍然看起来像“角度标题”而不是“可执行 testcase”，必须回到 seeds 阶段继续拆。
- 渲染时优先保证“原子性”，不要为了篇幅好看把多个核心结果合并成一条。

### 6.6 合并最终版

将 `working_dir/testcase_base.md` 与各个 `working_dir/testcase_delta_*.md` 合并为 `working_dir/testcase_final.md`。

合并规则：

- 内容等价时，保留表达更清晰、步骤更具体的一条。
- 视角互补时，保留两条或合并为一条更完整的 case，但不能破坏“一条 case 只验证一个核心结果”的原则。
- 需求中明确存在、但主稿和各个补缺专家都遗漏的点，必须补写。
- `coverage_expansion_plan` 中仍未被主稿或补缺专家承接的点，必须补写。
- `must_pair_paths` 和 `tool_required_paths` 在合并后必须逐项对账，确认已经显式落到最终 case。
- 不要丢失已有的关键执行步骤。

### 6.7 reviewer 专家复核终稿

在向用户输出前，必须把 `working_dir/testcase_final.md` 作为 review 对象，再做一轮“reviewer 专家”复核；这一轮不是润色，而是像测试用例评审人一样查缺补漏、纠正范围污染并回修终稿。

复核时必须重新对照以下输入，而不是只看最终 case：

- 用户原始需求文档
- Step 3 的 Drive 补充文档
- Step 4 已确认的 Jira 结果
- Step 5 已确认的测试对象、工具矩阵、测试角度、历史矩阵补全结果、`coverage_expansion_plan`
- 如有必要，再回看 `../smartx-docs-download/markdown_docs` 中直接相关的本地文档

复核重点：

1. 是否遗漏需求中明确存在的对象、条件、状态、特例、生命周期动作。
2. 是否把“系统服务 / 插件 / 上下游依赖能力”误写成目标 feature 本体；若本次需求主体不是这些能力，只允许保留必要联动回归，不得喧宾夺主。
3. 是否遗漏失败回滚、残留清理、状态恢复、对账重试、升级继承等高风险路径。
4. 是否遗漏需求中的差异化分支，例如：
   - 新建集群 vs 升级集群
   - 集群级规则 vs 主机级规则
   - 普通集群 vs VMware / SCVM / 双活特例
   - 默认允许 vs 默认拒绝
5. 是否满足“原子性”：
   - 一条 case 是否只验证一个核心结果
   - 是否明确写出了对象、条件、动作、预期结果、观测方式
   - 是否仍然停留在“主题/角度/模块标题”层，而不是可执行 testcase
   - 是否把多个变量组合、多层验证或多种结果混在同一条 case 中
6. 是否遗漏 `tool_required_paths` 中要求显式出现的 UI / API / CLI / 脚本 / 日志 / 告警 / 任务 / 抓包 / trace / 报表等执行或观测手段。
7. 是否遗漏 `must_pair_paths` 中要求成对出现的成功 / 失败、修改前 / 修改后、启用 / 停用、升级前 / 升级后、故障中 / 恢复后等路径。
8. 是否存在“看起来覆盖了，其实粒度过粗”的情况；若一条 case 混了多个核心结果，必须拆开。
9. 是否存在历史 Jira / 设计文档 / 本地样本源 / 实时近邻样本已经暴露的高风险场景，但终稿没有体现。
10. 是否存在越界内容：与当前 feature 仅弱相关、只能算背景信息的内容，不应大面积进入最终用例。
11. 是否与 `references/testrail_default.md` 的结构模板对齐：
   - `## 模块 -> ### 子模块 -> #### 用例` 的层级和编号是否完整
   - 每个模块、子模块、用例是否都有明确名称
   - 每个子模块下是否显式包含 `描述：`
   - 每条用例下是否显式包含 `描述：`、`【Step1】`、`【Step2】`、`【Step3】`
   - 是否存在缺编号、缺名称、缺描述、缺 Step 的格式缺口

输出与处理规则：

- 先在内部完成 review，再直接修改 `working_dir/testcase_base.md`、各个 `working_dir/testcase_delta_*.md`、`working_dir/testcase_final.md`，不要把未修订的草案直接交给用户。
- 如果 reviewer 发现终稿缺项、范围错误、优先级错位或粒度不合适，必须先回修终稿，再继续。
- 如果 reviewer 发现终稿格式未对齐 `references/testrail_default.md`，必须先补齐编号、名称、描述和 Step，再继续。
- 如果 reviewer 发现 `coverage_expansion_plan` 中仍有未兑现项，必须先回修终稿，再继续。
- 如果 reviewer 发现终稿中的某些 case 仍然停留在“主题大纲”层，而不是原子 testcase，必须回到 seeds 阶段重拆，再重新渲染。
- 只有当 reviewer 发现“关键需求本身存在歧义，且不澄清会明显影响最终 case 正确性”时，才向用户提问。
- 最终返回给用户的必须是 **review 后的 `working_dir/testcase_final.md` 正文**，而不是未复核版本。

最终对用户的输出要求：

- 以 `【测试用例处理完成】` 开头。
- 直接展示 review 后的最终测试用例正文。
- 除非用户额外要求，否则不要附加解释性长文。

---

## 质量检查

完成前确认：

- 已实际读取相关补充文档，而不只是看文件名。
- 已先完成“原始需求分析 + 用户确认”，再去搜 Drive 和 Jira。
- 已输出分析结果，并分别完成“需求分析确认”“Jira 摘要确认”“测试对象 + 工具矩阵 + 测试角度 + 历史矩阵补全结果 + coverage_expansion_plan 确认”。
- 最终 case 与需求主线一致，没有被模板示例内容带偏。
- 最终 case 兼顾主流程、异常、边界、运维联动、工具 / 观测手段、升级兼容和历史回归风险。
- 已先生成原子级 `case_seeds`，再通过补缺循环扩展到最终 testcase，而不是直接从测试角度生成大纲式终稿。
- 已执行有上限的补缺循环，并明确记录每轮 gap report 与停止条件。
- 已显式完成“原子性检查”：确认每条 case 只验证一个核心结果，且都具备对象、条件、动作、预期结果、观测方式。
- 如 reviewer 发现任何 case 仍停留在主题大纲层或混合多个核心结果，已回到 seeds 阶段重拆并重新渲染。
- 已在最终输出前完成 reviewer 专家复核，并已将 review 结论实际落实到 `working_dir/testcase_final.md`。
- 已完成“双源历史学习”：本地样本源 + 实时 / 近期 TestRail 源；如果其中一侧受阻，已明确说明影响。
- 已将 `coverage_expansion_plan` 中的 `must_pair_paths`、`tool_required_paths`、`must_expand_dimensions` 实际落实到最终 case 或明确标注残余风险。
- 已检查并修正与 `references/testrail_default.md` 的格式差异，确保编号层级、名称、描述、`【Step1】`、`【Step2】`、`【Step3】` 均完整。
- 最终输出给用户的是 review 后的终稿，而不是 draft 或未修订版本。
- 标题和粒度符合 TestRail 风格，单条 case 不臃肿。

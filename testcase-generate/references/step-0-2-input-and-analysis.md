# Step 0-2：输入归一化与需求分析

## 目录

- Step 0：归一化输入
- Step 1：盘点输入文件
- Step 2：分析原始需求并让用户确认
- Step 2.4：推荐 workflow mode

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

## Step 1：盘点输入文件

围绕 Step 0 归一化后的原始需求文档或目录做一次轻量盘点：

- 展示目录结构或等价的文件清单。
- 明确标出会参与后续分析的 `.pdf`、`.docx`、`.md` 文件。
- 标记哪些是“原始需求文档”，哪些是同目录下的补充文件。

这一阶段只做盘点，不先调用 `all-related-file-preparer-4-testcase-generate`。

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
7. 推荐 workflow mode（`lite` / `standard` / `deep`）及理由

这一轮必须等用户确认或修正。因为后续 Drive 搜索、Jira 搜索、本地历史 testcase 近邻检索和组别 pattern 选择都会复用这组关键词。

- 如果用户修正了 `core_keywords`，要同步回收并更新 `expansion_keywords`，不要继续沿用旧的扩展词包。
- 如果用户没有明确指定 workflow mode，默认采用这一轮推荐 mode。

### 2.4 推荐 workflow mode

在 Step 2 输出里给出推荐 mode，并说明理由：

- 推荐 `lite`：
  - 变更范围单一，只有 1 个主体对象或 1 条主路径。
  - 文档没有明显的升级、兼容、扩缩容、故障、性能、跨模块联动信号。
  - 用户更关心快速得到一版基础覆盖。
- 推荐 `standard`：
  - 默认模式。
  - 需要 Jira、历史近邻和 pattern 补全，但不一定需要把 Step 9-15 全开。
- 推荐 `deep`：
  - feature 明确涉及版本矩阵、升级路径、兼容性、故障恢复、容量、扩缩容、跨模块端到端。
  - 文档或用户预期强调“尽量把高风险专项都展开”。

说明规则：

- mode 决定 Step 8、Step 9-15、Step 17 的默认轮次与是否默认执行专项，但不影响 Step 4 的全文读取要求。
- 如果用户要求“先快一点”或“先给基础版”，优先降到 `lite` 或 `standard`。
- 如果用户要求“做全一点”或“高风险功能”，优先升到 `deep`。

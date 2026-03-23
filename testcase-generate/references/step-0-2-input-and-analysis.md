# Step 0-2：输入工作目录、归一化与需求分析

## 目录

- Step 0：创建输入工作目录并写入 `input-manifest.json`
- Step 1：检查输入并让用户确认本轮资料范围
- Step 1.5：把已确认输入归一化为本地文件集合
- Step 2：分析原始需求并让用户确认
- Step 2.5：展示三种 workflow mode 并让用户选择

## Step 0：创建输入工作目录并写入 `input-manifest.json`

先创建统一 intake 工作目录，再把当前轮收到的输入写成固定 JSON，为 Step 1 的输入检查脚本提供稳定入口。

支持的输入类型：

- 单个需求文档路径
- 包含需求文档的目录路径
- 一个或多个 Google Docs URL
- 通过 agent 上传的本地文件
- 上述几类输入的混合

### 0.1 创建 intake working_dir

先运行：

```bash
python scripts/create_workdir.py
```

脚本默认会在当前操作系统用户的 `Downloads` 目录下创建：

```text
testcase-generate-YYYYMMDD-HHMMSS/
  input-manifest.json
```

如果用户明确要求使用别的下载根目录，可以改用：

```bash
python scripts/create_workdir.py --downloads-dir <绝对路径>
```

### 0.2 填写 `input-manifest.json`

固定结构如下：

```json
{
  "google doc url": [],
  "uploaded files by agent": [],
  "user file directory": []
}
```

填写规则：

- `google doc url`
  - 只放 Google Docs 链接。
  - 一轮内有多个链接时全部写入数组。
- `uploaded files by agent`
  - 如果当前轮有用户上传给 agent 的文档，先保存到 Step 0 创建的 `working_dir` 内，再把这些已保存文件的绝对路径回写到这里。
  - 如果当前环境拿不到上传文件的本地可读路径，先停下来让用户改用“本地文件路径”或“目录路径”的方式提供，不要假装已经保存成功。
- `user file directory`
  - 记录用户明确提供的本地绝对路径。
  - 既可以是文件，也可以是目录。
  - 这一阶段只记录路径，不提前展开目录内容。

### 0.3 Step 0 的边界

- Step 0 只负责建目录和记录输入，不在这一步下载 Google Docs、分析正文或生成 testcase。
- 如果用户在 Step 1 期间补充了新的链接、文件或目录，先回写 `input-manifest.json`，再重新执行 Step 1。

## Step 1：检查输入并让用户确认本轮资料范围

### 1.1 运行输入检查脚本

运行：

```bash
python scripts/inspect_input_manifest.py <input-manifest.json 的绝对路径>
```

脚本会做这些事：

- 校验 `google doc url` 里的 Google Docs URL 是否能解析出文档 id
- 检查 `uploaded files by agent` 里的每个路径是否存在且可读
- 检查 `user file directory` 里的每个路径是否存在
- 如果某个 `user file directory` 项是目录，则递归展开其中“像需求/设计文档”的文件
- 输出候选需求文件列表、目录展开结果、阻塞项和推荐确认文案

目录展开时，默认只纳入这些后缀的文件：

- `.doc`
- `.docx`
- `.pdf`
- `.md`
- `.markdown`
- `.txt`
- `.ppt`
- `.pptx`
- `.rtf`
- `.xls`
- `.xlsx`

### 1.2 Google Docs URL 校验规则

- 对形如 `https://docs.google.com/document/d/<ID>/edit?...` 的 URL，取 `/d/` 后、下一个 `/` 前的字符串作为文档 id。
- 例如 `https://docs.google.com/document/d/1kRbOppUeD34YnqnwL2HdvZ9NW4iVQSoGitHNjOxycBo/edit?tab=t.7q8myxjn8ndc` 的 id 为 `1kRbOppUeD34YnqnwL2HdvZ9NW4iVQSoGitHNjOxycBo`。
- 如果某个 URL 不符合该模式，必须显式说明哪个 URL 无法提取 id，并停在 Step 1 等用户修正。

### 1.3 Step 1 的强制确认

在继续之前，必须把 Step 1 的结果返回给用户确认，至少包含：

- 已收到的 Google Docs URL
- 已保存的上传文件路径
- 用户提供的本地文件 / 目录路径
- 每个目录展开出的候选文件
- 当前的阻塞项或不确定点
- 建议本轮纳入的原始需求文档与补充资料

确认要求：

- 必须等用户明确确认或修正后，才能进入 Step 1.5 / Step 2。
- 如果目录里有多个候选文件，不要默认全量纳入；先请用户确认哪些属于本轮 testcase 生成输入。
- 如果用户补充、删除或替换了输入，先更新 `input-manifest.json`，再重新执行 Step 1。
- 没有用户确认前，不要下载 Google Docs，不要分析需求正文，不要进入 Step 2。

## Step 1.5：把已确认输入归一化为本地文件集合

Step 1 用户确认后，再把输入真正变成后续可消费的本地文件集合。

### 1.5.1 下载 Google Docs 到本地

读取并遵循 `../all-related-file-preparer-4-testcase-generate/google-drive-file-download/SKILL.md`，但此处的目标目录不要由用户额外指定，而是直接使用：

```text
<Step 0 创建的 working_dir>/google-docs/
```

调用要求：

- 将已确认的 Google Docs 文档 id 列表逐个传给下载技能，不要在单次调用里混传多个 id。
- 若下载失败，必须明确指出失败的 id 与错误，不能跳过失败项继续假设文档已存在本地。
- 若用户同时还确认了本地文件路径、目录中的部分文件或上传文件，则把下载结果与这些已确认本地资料合并，作为 Step 2 的输入集合。

Google Docs 下载失败时，强制按下面规则处理：

- 必须明确告诉用户：哪些 Google Docs 链接 / 文档 id 下载失败了。
- 必须明确告诉用户：不要继续假设这些文档已经落到本地。
- 必须明确要求用户：手动上传这些失败链接对应的 Markdown 文件，不能只补一个新链接继续往下走。
- 在用户上传 Markdown 后，先更新 `input-manifest.json`：
  - 把失败的 URL 从 `google doc url` 中移除
  - 把新上传 Markdown 的绝对路径写入 `uploaded files by agent`
- 更新完 `input-manifest.json` 后，重新执行 Step 1，让用户重新确认本轮资料范围，再进入 Step 2。

优先使用：

```bash
python scripts/update_input_manifest.py --manifest <input-manifest.json 的绝对路径> --remove-google-doc-url "<失败的 Google Docs URL>" --add-uploaded-file "<用户上传的 markdown 绝对路径>"
```

如果有多个失败链接或多个 Markdown 文件，可以重复传入 `--remove-google-doc-url` 和 `--add-uploaded-file`。

### 1.5.2 Step 1.5 的输出

Step 1.5 结束后，后续步骤看到的输入应统一为：

- 已确认的本地文件绝对路径列表
- 必要时保留一份“Google Docs URL -> 下载后本地文件”的映射

不要再把未经确认的目录扫描结果，或未经下载的原始 Google Docs URL，直接传入 Step 2 之后的需求分析、Drive 搜索与 Jira 搜索流程。

## Step 2：先分析原始需求文档并让用户确认

### 2.1 调用根目录文档分析技能

读取并严格遵循 `../smartx-doc-2-product-and-keywords/SKILL.md`。

- 输入优先使用 Step 1.5 已确认并归一化后的“原始需求文档”。
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
7. 三种 workflow mode（`lite` / `standard` / `deep`）的对比说明，并标出推荐项

这一轮必须等用户确认或修正。因为后续 Drive 搜索、Jira 搜索、本地历史 testcase 近邻检索和组别 pattern 选择都会复用这组关键词。

- 如果用户修正了 `core_keywords`，要同步回收并更新 `expansion_keywords`，不要继续沿用旧的扩展词包。
- mode 选择同样是这一轮的强制确认点。
- 如果用户明确选择了某个 mode，后续按该 mode 继续。
- 如果用户明确表示“你定”“按推荐的来”，才可以采用推荐 mode。
- 如果用户没有明确选择，也没有授权代选，不要继续进入 Step 3。

### 2.5 展示三种 workflow mode 并让用户选择

在 Step 2 输出里，必须同时展示 `lite` / `standard` / `deep` 三种 mode，让用户选择；不要只给一个推荐值。

每种模式都要强调“实际会走哪些步骤”：

- `lite`
  - 会走：Step 0-4、Step 8、Step 16、Step 17
  - 这代表会做：
    - 输入整理、资料确认、产品 / 关键词 / mode 确认
    - 搜索并补充直接相关的 Drive 文档
    - 全文读取资料并生成第一版 baseline testcase
    - review 和细化基础稿
    - 合并成最终稿并做 finalcheck 终稿校验
  - 默认不走：Step 5-7、Step 9-15
  - 只在用户明确要求或文档出现强信号时，才补做 Step 5-7 或专项步骤
- `standard`
  - 会走：Step 0-8、Step 16、Step 17
  - 这代表会做：
    - `lite` 的全部内容
    - Jira 场景补充
    - 本地历史近邻 testcase 补充
    - 组别 pattern / 常见写法补充
  - 默认会做：Step 5-7
  - 按 feature 风险按需做：Step 9-15
- `deep`
  - 会走：Step 0-8、Step 16、Step 17
  - 这代表会做：
    - `standard` 的全部内容
    - 边界、兼容性、压力、用户场景、升级、扩缩容、故障等专项尽量全开
    - 更高轮次的 review 和补强
  - 会尽量展开：Step 9-15 中所有可适用专项
  - Step 8、Step 17 以及专项步骤的多轮 review 深度更高

然后再给出推荐 mode，并说明理由：

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

推荐输出时，优先使用这种结构：

```markdown
以下是三种生成模式，请你选择 1 个继续：

1. `lite`
   会走：Step 0-4、Step 8、Step 16、Step 17
   会做：输入确认、补充直接相关资料、生成并 review 基础稿、合并终稿、finalcheck 校验
   默认跳过：Step 5-7、Step 9-15
   适合：先快速拿到一版基础覆盖

2. `standard`
   会走：Step 0-8、Step 16、Step 17
   会做：在 `lite` 基础上，补 Jira、历史近邻 testcase、组别 pattern
   默认追加：Step 5-7
   按需追加：Step 9-15
   适合：常规需求，兼顾效率和补充覆盖

3. `deep`
   会走：Step 0-8、Step 16、Step 17
   会做：在 `standard` 基础上，尽量补全边界、兼容性、压力、用户场景、升级、扩缩容、故障等专项
   会尽量展开：Step 9-15 所有可适用专项
   review 轮次更高
   适合：高风险、跨模块、升级 / 兼容 / 故障 / 容量类需求

我当前推荐：`<lite|standard|deep>`
推荐理由：<一句到两句理由>

请直接回复：`lite` / `standard` / `deep`。
如果你希望我代选，也请明确回复“按你推荐的来”。
```

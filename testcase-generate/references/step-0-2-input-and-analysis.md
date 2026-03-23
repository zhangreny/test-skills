# Step 0-2：输入工作目录、归一化与需求分析

## 目录

- Step 0：创建输入工作目录并写入 `input-manifest.json`
- Step 1：检查输入并让用户确认本轮资料范围
- Step 1.5：把已确认输入归一化为本地文件集合
- Step 2：分析原始需求并让用户确认
- Step 2.5：说明固定完整流程并确认继续

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

脚本默认会在当前系统用户的 `Downloads` 目录下创建：

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
  - 如果当前轮有用户上传给 agent 的文档，先保存到 Step 0 创建的 `working_dir` 内，再把这些文件的绝对路径回写到这里。
  - 如果当前环境拿不到上传文件的本地可读路径，先停下来让用户改用“本地文件路径”或“目录路径”的方式提供。
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
- 如果某个 `user file directory` 项是目录，则递归展开其中像需求或设计文档的文件
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
- 如果某个 URL 不符合该模式，必须显式说明哪个 URL 无法提取 id，并停在 Step 1 等用户修正。

### 1.3 Step 1 的强制确认

继续之前，必须把 Step 1 的结果返回给用户确认，至少包含：

- 已收到的 Google Docs URL
- 已保存的上传文件路径
- 用户提供的本地文件或目录路径
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

读取并遵循 `../all-related-file-preparer-4-testcase-generate/google-drive-file-download/SKILL.md`，但此处的目标目录直接使用：

```text
<Step 0 创建的 working_dir>/google-docs/
```

调用要求：

- 将已确认的 Google Docs 文档 id 列表逐个传给下载技能，不要在单次调用里混传多个 id。
- 若下载失败，必须明确指出失败的 id 与错误，不能跳过失败项继续假设文档已存在本地。
- 若用户同时还确认了本地文件路径、目录中的部分文件或上传文件，则把下载结果与这些已确认资料合并，作为 Step 2 的输入集合。

Google Docs 下载失败时，强制按下面规则处理：

- 明确告诉用户哪些 Google Docs 链接或文档 id 下载失败了。
- 明确告诉用户不要继续假设这些文档已经落到本地。
- 明确要求用户手动上传这些失败链接对应的 Markdown 文件。
- 在用户上传 Markdown 后，先更新 `input-manifest.json`：
  - 把失败的 URL 从 `google doc url` 中移除
  - 把新上传 Markdown 的绝对路径写入 `uploaded files by agent`
- 更新完 `input-manifest.json` 后，重新执行 Step 1，让用户重新确认本轮资料范围，再进入 Step 2。

优先使用：

```bash
python scripts/update_input_manifest.py --manifest <input-manifest.json 的绝对路径> --remove-google-doc-url "<失败的 Google Docs URL>" --add-uploaded-file "<用户上传的 markdown 绝对路径>"
```

### 1.5.2 Step 1.5 的输出

Step 1.5 结束后，后续步骤看到的输入应统一为：

- 已确认的本地文件绝对路径列表
- 必要时保留一份“Google Docs URL -> 下载后本地文件”的映射

不要再把未经确认的目录扫描结果，或未下载的原始 Google Docs URL，直接传入 Step 2 之后的需求分析、Drive 搜索或 Jira 搜索流程。

## Step 2：先分析原始需求文档并让用户确认

### 2.1 调用文档分析技能

读取并严格遵循 `../smartx-doc-2-product-and-keywords/SKILL.md`。

要求：

- 输入优先使用 Step 1.5 已确认并归一化后的“原始需求文档”。
- 如果用户一次给了多个文件，先判断它们是否都指向同一个 feature。
- 让该技能返回结构化结果，包括摘要、产品、关键词、证据和阻塞项。
- 优先使用标准字段：
  - `core_keywords`
  - `expansion_keywords`
- 如果上游仍只返回旧字段 `selected_keywords`，先在本步骤内完成归一化，再继续后续流程。

### 2.2 需要澄清时的规则

- 如果候选产品数量大于 1，用简短可直接回复的方式向用户确认，不要只输出机器可解析 JSON。
- 如果候选核心关键词超过 2 个，同样用简短可直接回复的方式让用户确认 1-2 个 `core_keywords`。
- `expansion_keywords` 不在这一轮被压缩到 1-2 个，而是保留为后续检索词包。

### 2.3 向用户展示并确认分析结果

继续之前，显式展示这一轮确认后的分析包：

1. 功能摘要
2. 主体产品及关系
3. 最终 `core_keywords`（1-2 个）
4. `expansion_keywords` 摘要（按类别展示）
5. 使用到的原始需求文档
6. 当前仍存在的不确定点
7. 固定完整流程的执行说明

这一轮必须等用户确认或修正。因为后续 Drive 搜索、Jira 搜索、本地历史 testcase 近邻检索和组别 pattern 选择都会复用这组关键词。

- 如果用户修正了 `core_keywords`，要同步回收并更新 `expansion_keywords`。
- 固定完整流程的说明同样是这一轮的强制确认点。
- 如果用户还没有确认分析结果，不要继续进入 Step 3。

### 2.5 说明固定完整流程并确认继续

在 Step 2 输出里，不再展示任何 workflow 分级选项。要直接明确说明：

- 后续默认执行完整 Step 0-17。
- Step 5-7 会默认执行。
- Step 9-15 也会逐步执行，并分别产出 evidence report 与 delta；如果某一步最后没有新增 case，也要写明“已执行但无新增”的收敛结论。
- Step 8、Step 9-15、Step 17 的默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy`。
- 固定完整流程不会降低 Step 4 的全文读取要求。

推荐输出时，优先使用这种结构：

```markdown
我先确认一下这轮分析结果，确认后会直接按固定完整流程继续，不再区分任何 workflow 档位：

- 后续会依次执行 Step 0-17。
- Step 5-7 会补 Jira、历史近邻 testcase、组别 pattern。
- Step 9-15 会逐项执行边界、兼容性、压力、用户场景、升级、扩缩容、故障等专项补强。
- Step 8、Step 9-15、Step 17 的轮次与收敛规则以 `working_dir/workflow_state.json` 为准。

如果上面的分析结果没问题，我就继续进入 Step 3。
```

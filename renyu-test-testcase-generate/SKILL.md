---
name: renyu-test-testcase-generate
description: 根据用户给出的单文件路径、目录路径、Google 文档链接或通过 agent 输入框上传的文件，先统一创建 `testcase-generate-YYYYMMDD-HHMMSS` 工作目录并整理 `temp_inputs`，再强制让用户确认本次用于测试用例生成的资料后才继续。适用于用户说“帮我生成测试用例”且输入只会包含以下四种之一时：(1) 文件路径在 xxx，(2) 文件所属目录在 xxx，(3) 一组 Google 文档链接，(4) 已上传文件。
---

# Renyu Test Testcase Generate

按顺序执行，不要跳步：

**Step 1：统一化用户输入 -> Step 2：整理 `temp_inputs` 并等待用户确认 -> Step 3：收到“继续”之类明确确认后再进入下游测试用例生成**

## 快速规则

- 一次只处理一种输入形态；如果用户同时给了多种输入，先请用户明确本轮以哪一种为准。
- 所有会话目录、临时目录、目录扫描、Google Doc ID 提取、文件复制与整理，优先调用 `scripts/testcase_session.py`，不要手写一套重复逻辑。
- 会话根目录固定命名为 `testcase-generate-YYYYMMDD-HHMMSS`，其下固定使用 `temp_inputs` 作为本轮测试用例生成的临时文件夹。
- 所有报错都要立即停止在当前步骤，不要带着缺失输入继续推断。
- Step 2 是强制确认门：只有用户明确输入“继续”“continue”“开始生成”“进入下一步”等继续含义的话，才能进入后续测试用例生成。
- 目录模式下，即使只发现 1 个文件，也必须先列出来并询问用户要不要用它，再复制到 `temp_inputs`。
- Google 文档模式下，如果任何一个链接解析失败或任何一个下载失败，都要停止，并要求用户自行导出后通过 agent 上传文件。

## 资源导航

- 会话辅助脚本：`scripts/testcase_session.py`
- 目录扫描与确认口径：`references/intake-checklist.md`
- Google Drive 下载子技能：`../all-related-file-preparer-4-testcase-generate/google-drive-file-download/SKILL.md`
- 下游完整测试用例流程：`../testcase-generate/SKILL.md`

## Step 1：统一化用户输入

### 1.0 创建会话目录

先调用：

```bash
python <SKILL_DIR>/scripts/testcase_session.py prepare-session
```

脚本会按当前操作系统推断用户的 `Downloads` 目录，并创建：

```text
<Downloads>/testcase-generate-YYYYMMDD-HHMMSS/
<Downloads>/testcase-generate-YYYYMMDD-HHMMSS/temp_inputs/
```

后续所有输入都要汇总进这个 `temp_inputs` 目录。

如果用户明确要求使用别的下载根目录，可在脚本里通过 `--downloads-dir` 覆盖；否则不要自定义目录结构。

### 1.1 输入形态 1：用户给出文件路径

当用户输入类似“文件路径在 xxx”时：

1. 调用 `stage-files` 校验并复制文件：

```bash
python <SKILL_DIR>/scripts/testcase_session.py stage-files --session-dir "<session_dir>" --source "<file_path>"
```

2. 如果路径不存在、不是文件，或复制失败，立即停止并向用户报错。
3. 路径里可能包含中文或空格；始终用带引号的绝对路径，不要自行转码或改名。
4. 复制成功后进入 Step 2。

### 1.2 输入形态 2：用户给出文件所属目录

当用户输入类似“文件所属目录在 xxx”时：

1. 先扫描目录：

```bash
python <SKILL_DIR>/scripts/testcase_session.py scan-dir --source-dir "<dir_path>"
```

2. 把目录内文件完整列给用户，并额外给出脚本推断的“最可能用于测试用例生成的需求/设计文档”候选。
3. 必须停下来让用户明确选择本轮要用哪些文件；即使目录里只有 1 个文件，也必须问。
4. 用户确认后，再调用 `stage-files` 复制所选文件到 `temp_inputs`：

```bash
python <SKILL_DIR>/scripts/testcase_session.py stage-files --session-dir "<session_dir>" --source "<selected_file_1>" --source "<selected_file_2>"
```

5. 复制成功后进入 Step 2。

### 1.3 输入形态 3：用户给出一堆 Google 文档链接

当用户输入类似“扔给你一堆 Google 文档链接”时：

1. 先创建会话目录，再解析 URL：

```bash
python <SKILL_DIR>/scripts/testcase_session.py parse-gdocs --url "<url_1>" --url "<url_2>"
```

2. 只提取每个链接里 `/d/` 与下一个 `/` 之间的内容作为文档 ID。
3. 如果任何一个 URL 无法解析出 ID，立即停止并把失败链接列给用户。
4. 全部解析成功后，读取并遵循 `../all-related-file-preparer-4-testcase-generate/google-drive-file-download/SKILL.md`，把这些 ID 下载到刚创建的会话根目录。
   目标目录传 `<session_dir>`，不要传 `temp_inputs`。
5. 该子技能会把文件放到：

```text
<session_dir>/google-drive-file-download/
```

6. 下载全部成功后，再调用：

```bash
python <SKILL_DIR>/scripts/testcase_session.py import-downloaded --session-dir "<session_dir>" --source-dir "<session_dir>/google-drive-file-download"
```

7. 如果任何一个下载失败，立即停止，不要继续分析；明确要求用户自行下载或导出这些文档，再通过 agent 上传文件。
8. 向用户索取手动导出文件时，额外提醒：
   - 如果只想导出当前正在看的那个 Google 文档，选择 `Current tab`
   - 如果这次打开了多个相关文档并且都要导出，选择 `All tabs`

### 1.4 输入形态 4：用户通过 agent 输入框上传文件

当用户直接上传文件时：

1. 先创建会话目录。
2. 如果当前环境已经把上传文件暴露为本地临时路径，直接调用 `stage-files` 复制到 `temp_inputs`。
3. 如果当前环境没有可读路径、只有附件元信息，先尝试使用当前线程可读取到的本地附件文件；只有在确实拿不到文件时，才请用户改用“本地文件路径”或“目录路径”的方式重新提供。
4. 复制成功后进入 Step 2。

## Step 2：整理 `temp_inputs` 并要求用户确认

无论 Step 1 来自哪种输入，都必须执行：

```bash
python <SKILL_DIR>/scripts/testcase_session.py summarize-session --session-dir "<session_dir>"
```

然后：

1. 把 `temp_inputs` 里的文件整理成清单返回给用户，至少包含文件名、相对路径、大小。
2. 明确告诉用户：这些就是当前将用于测试用例生成的输入资料。
3. 明确询问用户是否继续；示例话术可参考 `references/intake-checklist.md`。
4. 只有用户输入带有继续含义的明确确认词，才能进入下一步。
5. 如果用户要增删替换文件，就留在 Step 1/Step 2，重新整理后再次确认。

## Step 3：确认后再进入下游测试用例生成

收到用户的继续确认后：

1. 优先把 `temp_inputs` 中的绝对路径列表作为输入，交给 `../testcase-generate/SKILL.md` 继续完整的测试用例生成流程。
2. 把 `<session_dir>` 当作本轮产物根目录继续沿用，避免后续中间文件散落到别处。
3. 如果当前任务只要求做输入准备与确认，而未要求继续生成测试用例，就停在 Step 2 的确认结果处，不要擅自进入下游。

## 失败处理

- 会话目录创建失败：立即报错并停止。
- 文件路径不存在：立即报错并停止。
- 目录不存在：立即报错并停止。
- 目录扫描结果为空：告知用户目录下没有可用文件，并停止等待新的输入。
- Google 文档链接解析失败：列出失败链接并停止。
- Google Drive 任一文件下载失败：不要部分继续，改为要求用户手动导出后上传。
- `temp_inputs` 为空：不要进入 Step 2 之后的流程。

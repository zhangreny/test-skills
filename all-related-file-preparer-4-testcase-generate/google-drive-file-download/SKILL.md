---
name: google-drive-file-download
description: 根据 Google Drive 文件 ID 列表，使用 gog CLI 将文件下载到用户指定的本地目录下的 google-drive-file-download 文件夹，下载结果为 markdown 文件。通过脚本对每个 ID 单独调用脚本 scripts/drive_download_by_id.py。在用户提到「按 ID 下载 Drive 文件」「把 Drive 文件下载到某目录」「根据文件 id 批量下载」或提供 Drive 文件 id 与目标目录时使用此技能。
---

# Google Drive File Download

根据给定的 Google Drive 文件 ID 与目标目录，优先逐个调用 `scripts/drive_download_by_id.py` 脚本将文件下载到本地下的 `google-drive-file-download` 文件夹。每个 ID 单独执行，便于错误定位与重试；如果脚本失败，再退回 `gog drive download` 命令行继续下载。

## 前置条件

- 本技能优先依赖脚本：`scripts/drive_download_by_id.py`。执行前确认脚本存在；若脚本不存在，直接改用 `gog drive download` 命令行。
- 环境需已安装并授权 **gog**（Google Workspace CLI），且具备 Drive 访问权限。

## 输入

| 输入 | 说明 |
|------|------|
| **目标目录** | 本地已存在的目录路径，下载文件将写入该目录。 |
| **文件 ID 列表** | 一个或多个 Google Drive 文件 ID（可从 keyword-related-file-from-google-drive 等技能的输出中获得）。 |

## 工作流程

### 步骤 1：校验输入

- 若用户**未提供目标目录**：提示用户指定一个已存在的本地目录。
- 若用户**未提供任何文件 ID**：提示用户提供至少一个 Drive 文件 ID，或先通过其他技能（如 keyword-related-file-from-google-drive）获取 id 列表。
- 若**目标目录不存在或不可写**：明确报错并停止，不执行下载。

### 步骤 2：执行下载（按 ID 循环，每次只传一个 ID）

在目标文件夹下创建一个 google-drive-file-download 文件夹，将下载的文件保存在该文件夹下。

```text
<目标目录>/google-drive-file-download
```

**必须**在循环中**依次只传递和下载一个 ID**：对列表中的每个文件 ID，优先**单独调用一次**脚本，每次调用只传入一个 ID，实现「一次只下载一个文件」。不得在一次调用中传入多个 ID。

```text
python <SKILL_DIR>/scripts/drive_download_by_id.py --output "<目标目录>/google-drive-file-download" --id "<单个文件ID>"
```

**执行要点：**

- 对每个待下载的 ID 循环：每次调用脚本时只传**一个** ID，下载完成或失败后再处理下一个 ID；单个失败不影响后续 ID。
- 进度与错误信息输出到 **stderr**，必须捕获并保留；成功/失败会按 `[序号/总数] id 下载成功` 或 `[序号/总数] id 失败: 具体错误` 的形式输出。
- 若脚本退出码非 0、运行环境不兼容，或脚本本身不可用，不要直接停止；对当前 ID 改用命令行 fallback：

```text
gog drive download "<单个文件ID>" --output "<目标目录>/google-drive-file-download" --format md
```

- fallback 时仍然保持“一次只下载一个 ID”，不要把多个 ID 合并到一次命令中
- 如果某个 ID 的命令行 fallback 成功，则继续处理下一个 ID
- 只有脚本和命令行都失败时，才把该 ID 记为失败并汇总错误信息反馈给用户

### 步骤 3：反馈结果与错误

- **全部成功**：告知用户文件已下载到目标目录，并列出已下载的 ID 或数量。
- **部分或全部失败**：将 stderr 中每条失败行的「具体错误」原样或归纳后呈现给用户，格式建议：

```
以下文件下载失败，请根据错误信息排查或重试：

| 文件 ID | 错误信息 |
|---------|----------|
| ID1    | 具体错误内容 |
| ID2    | 具体错误内容 |
```

并说明可针对失败 ID 再次执行本技能进行重试。

## 错误处理速查

| 场景 | 处理方式 |
|------|----------|
| 未提供目标目录 | 提示用户指定已存在的本地目录 |
| 未提供文件 ID | 提示用户提供 ID 或通过其他技能获取 |
| 目标目录不存在 | 报错并停止，不执行下载 |
| 脚本不存在 | 直接尝试 `gog drive download` 命令行 |
| 脚本返回非零 | 对失败 ID 先尝试 `gog drive download` 命令行 |
| 命令行 fallback 失败 | 捕获 stderr，将每个失败 ID 及对应错误反馈给用户，建议重试 |
| 未找到 gog 命令 | 提示用户安装 gog 并完成 Drive 授权 |

## 与 keyword-related-file-from-google-drive 配合

用户可先使用 **keyword-related-file-from-google-drive** 得到相关文件的 `id` 与 `webViewLink`，再使用本技能将指定 id 的文件下载到本地目录。本技能只负责「按 id + 目录下载」，不解析关键词或分析结果。

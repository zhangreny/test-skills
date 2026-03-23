# Skills 使用教程

本文档用于指导你在自己的 agent 工具中接入本项目里的 skills，并调用 `testcase-generate` 生成测试用例。

## 1. 将本项目克隆到 agent 工具的 skills 目录

### 1.1 自动操作

将 https://newgh.smartx.com/renyu-zhang/skills-for-Smartx_QA_AI 内的所有子文件夹放到你的 skills 目录下

### 1.2 手动操作

先找到你的 agent 工具本地 skills 目录，然后将本项目克隆进去。

示例：

```bash
cd /path/to/your-agent/skills
git clone https://newgh.smartx.com/renyu-zhang/skills-for-Smartx_QA_AI
```

如果你的 agent 工具要求 skills 必须直接位于某个固定目录下，请确保本项目被克隆后，`testcase-generate`、`smartx-doc-2-product-and-keywords`、`all-related-file-preparer-4-testcase-generate` 等目录都能被 agent 正确发现。

建议克隆完成后检查以下内容：

- 能看到顶层 `SKILL.md` 所在的各个技能目录
- agent 工具支持按目录读取本地 skills
- agent 工具可以访问这些 skills 内的 `scripts/` 和 `references/`

## 2. 安装运行依赖

### 2.1 安装 Python

请安装 `Python >= 3.9`。

可用以下命令确认版本：

```bash
python --version
```

或：

```bash
python3 --version
```

### 2.2 安装 gog

`testcase-generate` 相关流程会依赖 Google Drive 检索和下载能力，因此建议提前安装并配置 `gog`。

不同系统安装方式如下：

- macOS：需要手动执行安装命令，例如 `brew install steipete/tap/gogcli`
- Windows：调用 skills [gog-windows-install](C:/Users/27845/.codex/skills/gog-windows-install/SKILL.md)
- Linux：调用 skills [gog-linux-installer](C:/Users/27845/.codex/skills/gog-linux-installer/SKILL.md)

其中，Windows 和 Linux 的 `gog` 安装流程已经封装成 skill，通常可以直接让 agent 工具执行。`gog auth credentials` 和 `gog auth add` 也属于这两个 skill 的流程范围；如果过程中需要 Google 登录授权、浏览器确认或其他必须由用户亲自完成的步骤，再由 agent 在中途返回提示用户操作，完成后继续后续步骤。
macOS 这两步需要在安装完 gog 后手动操作，具体文件如何获取可参考 gog-windows-install/SKILL.md 的 Step6 & Step7

## 3. 在 agent 工具中调用 `testcase-generate`

完成 skills 接入和环境准备后，就可以在 agent 工具中直接通过 prompt 调用 `testcase-generate`。

### 3.1 已知本地文件目录时

可以使用类似下面的语句：

```text
请调用 testcase-generate skills，文件目录位于 xx/xx/xx
```

更明确一点的写法也可以：

```text
请调用 testcase-generate skills，基于目录 xx/xx/xx 下的需求文档生成测试用例。
```

如果目录下有多个文件，建议把原始需求文档和补充文档放在同一目录，方便 skill 先做盘点，再按流程继续分析、补料和生成用例。

### 3.2 在 agent 工具中直接上传文档时

如果你的 agent 工具支持文件上传，可以使用类似下面的 prompt：

```text
请将我上传的文档存储于 xx/xx/xx，调用 testcase-generate skills 生成测试用例。
```

建议目标目录使用一个单独的工作目录，便于后续：

- 保存上传的原始需求文档
- 保存中间分析结果或补充资料
- 输出最终测试用例

## 4. 推荐使用方式

为了让 `testcase-generate` 输出更稳定，建议：

- 上传或提供尽量完整的需求文档、README、补充说明
- 保证文档内容聚焦同一个 feature，避免多个不相关主题混在一起
- 如果 agent 工具支持多轮确认，保留产品归属、关键词、Jira 摘要等确认步骤

## 5. 常见问题

### 5.1 为什么需要安装 gog

因为 `testcase-generate` 的完整流程通常会调用与 Google Drive 搜索、下载相关的 skills，用于补齐历史资料和参考文档。

### 5.2 只有文档，没有 Drive 权限，也能用吗

可以先仅基于本地文档做分析和初步测试用例生成，但如果缺少 Drive 资料、历史 issue 或内部补充文档，最终结果可能不如完整流程充分。

### 5.3 推荐最小技能集合是什么

如果你的目标只是生成测试用例，建议至少保证以下技能在 agent 工具中可用：

- `testcase-generate`
- `smartx-doc-analyzer`
- `all-related-file-preparer-4-testcase-generate`

如果还需要本地补充 SmartX 内部文档，可再接入：

- `smartx-docs-download`

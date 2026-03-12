---
name: keyword-related-file-from-google-drive
description: Search Google Drive for files related to keywords extracted from document analysis results. Use this skill whenever the user provides document analysis output (containing a description summary and keywords) and wants to find related files in Google Drive. Trigger when the user mentions "Google Drive search", "keyword search", "find related files", or provides analysis results with keywords to search against Drive. Also trigger when the user says things like "根据分析结果搜索文件", "用关键词搜 Drive", or "帮我找相关文件".
---

# Keyword Related File From Google Drive

根据文档分析结果（描述摘要 + 关键词），在 Google Drive 中搜索每个关键词对应的相关文件，去重后汇总返回。

## 前置条件

本技能依赖位于技能目录 `scripts/drive_search_by_keywords.py` 的脚本。执行前请确认脚本存在：

```bash
ls "$(dirname "$0")/scripts/drive_search_by_keywords.py" 2>/dev/null \
  || echo "⚠️ 脚本不存在，请检查技能目录结构"
```

---

## 工作流程

### 步骤 1：校验输入

检查用户输入是否同时包含以下两项：

| 字段 | 识别特征 |
|------|----------|
| **描述摘要** | 含有 `### 文档对主要功能点的描述摘要` 或类似标题 |
| **关键词列表** | 含有 `### 关键词` 或类似标题，其下有具体词条 |

若缺少任一字段，立即告知用户缺失哪些内容，**不要继续执行**：

```
请确认输入内容：
- 描述摘要：❌ 缺失 / ✅ 存在
- 关键词：❌ 缺失 / ✅ 存在

请提供完整的分析结果后再试。
```

---

### 步骤 2：提取关键词

从 `### 关键词` 区块下提取所有关键词。

**注意事项：**
- 只提取关键词区块的内容，不要混入描述摘要中出现的词汇
- 跳过空白行和纯标点符号行
- 若关键词数量为 0，告知用户后停止

---

### 步骤 3：执行搜索

使用技能目录下的脚本批量搜索，脚本内部会自动处理关键词中的特殊字符（单引号、反斜杠等）：

```bash
# SKILL_DIR 为本技能的安装目录，需替换为实际路径
python3 "${SKILL_DIR}/scripts/drive_search_by_keywords.py" 关键词1 关键词2 关键词3
```

**执行要点：**
- 将所有关键词作为独立参数传入，一次调用完成（避免多次调用导致重复 OAuth 授权）
- 若脚本报错（非零退出码），捕获 stderr 并向用户说明原因，不要静默失败

**处理脚本缺失：** 若脚本不存在，说明技能未正确安装，提示用户检查 `scripts/` 目录。

---

### 步骤 4：相关性筛选

脚本输出的 JSON 数组仅基于关键词字面匹配，可能包含无关文件。在返回结果前，需结合**描述摘要**和**关键词列表**对每个文件的标题进行相关性判断，过滤掉明显不相关的文件。

**筛选规则：**

对每个文件的 `name` 字段进行判断，若满足以下任意条件则**保留**，否则**丢弃**：
- 文件名包含任意一个关键词（精确或部分匹配）
- 文件名所指示的主题与描述摘要的核心内容存在合理关联

**筛选示例：**

| 场景 | 处理 |
|------|------|
| 关键词为"erspan"，文件名为"ERSPAN 流量镜像使用实践与性能说明" | ✅ 保留 |
| 关键词为"erspan"，文件名为"OS/ELF 6.3 项目管理文档" | ❌ 丢弃 |
| 描述摘要涉及"网络流量镜像"，文件名为"erspan 文档" | ✅ 保留 |
| 描述摘要涉及"网络流量镜像"，文件名为"SMTX OS 及配套工具产品路线图" | ❌ 丢弃 |

**筛选后为空的处理：**

若所有文件均被过滤掉，停止执行并提示用户：

```
搜索到 {原始数量} 个文件，但经相关性筛选后全部被过滤。

可能原因：
- Drive 中匹配到的文件与当前文档主题关联度较低
- 关键词在 Drive 中存在歧义，命中了不相关内容

建议：
- 检查关键词是否足够具体
- 尝试手动在 Drive 中搜索核心关键词确认是否有相关文件
```

---

### 步骤 5：返回结果

将筛选后的文件列表以如下格式返回给用户：

**结果展示规范：**

- ✅ **有结果**：务必列出每个文件的 id、名称、可点击链接，不要遗漏任何字段任何文件，用 Markdown 表格呈现，格式如下：

```
**共找到 {筛选后数量} 个相关文件（原始匹配 {原始数量} 个）：**

| 序号 | 文件名 | id | 链接 |
|------|--------|-----|------|
| 1 | 文件名 | id | webViewLink |
| 2 | 文件名 | id | webViewLink |
```

- ❌ **筛选后为空**：按步骤 4 的提示处理，不展示文件列表
- ❌ **脚本执行失败**：展示错误信息，引导用户排查（权限、网络、认证等）

---

## 错误处理速查

| 场景 | 处理方式 |
|------|----------|
| 输入缺少描述摘要或关键词 | 步骤 1 中止，提示用户补全 |
| 关键词提取结果为空 | 告知用户，停止执行 |
| 脚本文件不存在 | 提示检查技能安装，停止执行 |
| 脚本返回非零退出码 | 展示 stderr，引导排查 |
| JSON 解析失败 | 展示原始输出，提示脚本可能有问题 |
| 所有关键词均无结果 | 友好提示，建议调整关键词 |
| 搜索有结果但筛选后为空 | 步骤 4 中止，说明原因并给出建议 |
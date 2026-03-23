# Step 3：先询问是否需要补充相关 Drive 文档，再按用户选择处理

在调用 `../all-related-file-preparer-4-testcase-generate/SKILL.md` 之前，必须先显式问用户：

`是否需要我根据刚确认的关键词，再去 Google Drive 搜索一批关联文档作为补充资料？如果不需要，我就只用你当前已上传 / 已确认的文档继续生成 testcase。`

只有在用户明确回答“需要”“去搜一下”“补充一下关联文档”之类肯定语义时，才进入下面的 Drive 搜索与下载流程。

如果用户明确回答“不需要”“只用当前文档”“先不要搜 Drive”之类否定语义，则：

- 不调用 `../all-related-file-preparer-4-testcase-generate/SKILL.md`
- 直接把“本轮不补充 Drive 关联文档”记录为 Step 3 结论
- 进入 Step 4，并只使用当前已上传 / 已确认的文档进行用例生成

读取并严格遵循 `../all-related-file-preparer-4-testcase-generate/SKILL.md`。

## 调用要求

- 输入使用 Step 1 的有效文件路径列表。
- 同时把 Step 2 已确认的摘要、产品、`core_keywords`、`expansion_keywords` 作为上游交接结果传入。
- 明确要求该技能跳过重复的产品 / 关键词确认，直接进入 Drive 搜索与下载流程。
- Drive 搜索优先使用 `core_keywords` 定位；仅在需要消歧时补用 `expansion_keywords`，避免噪声扩散。
- 如果用户选择下载，保留本地下载结果，供 Step 4 全文读取。
- 如果某个候选 Drive 文件明显不相关，在本步骤就剔除，并说明理由；不要把大量无关文档带入 Step 4。

## 本步骤结束时应拿到

- 如果用户选择搜索：
  - 已确认的相关 Drive 文件链接和 id
  - 如果用户选择下载，则拿到本地下载结果
- 如果用户选择不搜索：
  - 明确的用户决定：本轮不补充 Drive 关联文档
  - 后续仅使用当前已上传 / 已确认文档继续生成
- 尚未解决的资料缺口或下载失败项

## 向下游交接

把以下内容完整交给 Step 4：

- 原始需求文件路径列表
- 已确认的 Drive 补充文档本地路径 / 链接 / id；如果用户选择不搜索，则这里明确写“无”
- Step 2 的功能摘要、产品信息、`core_keywords`、`expansion_keywords`
- 当前仍存在的不确定点

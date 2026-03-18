# Step 5：补充 Jira delta 并 review

## 目录

- 5.1 输入与全文读取要求
- 5.2 查询并筛选相关 Jira
- 5.3 置信度分流：高置信度直接继续，低置信度再向用户确认
- 5.4 输出 Jira delta `delta/delta_step5_jira.md`
- 5.5 review Jira delta 并输出 `delta/delta_step5_jira_reviewed.md`

## 5.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- Step 2 已确认的 `core_keywords`、`expansion_keywords`、功能摘要、主体产品信息
- Step 4 使用过的原始需求文档、Drive 补充文档、SmartX 产品手册 / 白皮书
- `working_dir/baseline/testcase_base_reviewed.md`

执行要求：

- 不要只拿 `testcase_base_reviewed.md` 的标题或少数 case 做 Jira 补充。
- 重新阅读全文版 testcase，先总结当前已经覆盖的测试角度，再去找 Jira 缺口。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤全文读取的资料和 testcase 文件。

## 5.2 查询并筛选相关 Jira

围绕 Step 2 已确认的关键词执行 Jira 检索。优先使用环境变量或调用方显式提供的配置：

- Jira 站点：`SMARTX_JIRA_BASE_URL`
- 用户名：`SMARTX_JIRA_USERNAME`
- 密码：`SMARTX_JIRA_PASSWORD`

如果环境变量不存在，再看用户是否明确给了地址或凭据；如果仍然没有：

- `lite` 模式：允许跳过 Step 5，并说明 Jira 资料缺口。
- `standard` / `deep` 模式：先说明阻塞，再决定是否请用户补充。

查询策略：

- 先用 `core_keywords` 做核心精确搜
- 再用 `expansion_keywords` 做链路搜、症状搜、结果层 / 工具搜
- 如果 feature 涉及版本、架构、平台、升级路径、兼容约束，再补版本 / 兼容搜

筛选规则：

- 只保留与当前 feature 直接相关、能转化为回归风险或测试点的 issue
- 对被保留的每条相关 Jira，至少完整读取：
  - `summary`
  - `description`
  - 关键评论
  - 环境 / 版本信息
  - 修复信息 / 结论信息
- 不要只看 Jira 标题就写 testcase
- 对明显无关的 issue 说明剔除理由

## 5.3 置信度分流：高置信度直接继续，低置信度再向用户确认

先输出：

- `working_dir/reports/jira_candidate_summary.md`

摘要里至少包含：

1. 直接相关 Jira 列表
2. 每条 Jira 为什么相关
3. 可转化为测试点的风险 / 异常 / 恢复 / 兼容性线索
4. 当前仍存疑的 Jira
5. 本轮置信度判断：`high` 或 `needs_confirmation`

要求：

- 满足以下条件时，可判定为 `high` 并继续：
  - 保留的 issue 都能直连当前 feature 的对象、动作、异常或版本链路。
  - 不存在两个及以上相互竞争的 Jira 候选簇。
  - 边缘命中项不超过 1 条，且已经写明剔除理由。
- 一旦出现以下情况，改为 `needs_confirmation` 并暂停：
  - 多组 Jira 看起来都可能相关。
  - 关键 issue 的正文与当前 feature 的映射仍有歧义。
  - 需要用户判断“是否值得吸收某一类历史问题”。

## 5.4 输出 Jira delta `delta/delta_step5_jira.md`

以 `working_dir/baseline/testcase_base_reviewed.md` 为参考，只输出 Jira 带来的新增 testcase delta：

- `working_dir/delta/delta_step5_jira.md`

delta 要求：

- 每条由 Jira 派生的用例都要显式标注 Jira 号。
- 推荐在用例名称或 `描述：` 中保留 Jira 号，例如 `JIRA: ABC-123`。
- 不要复制整份 baseline。
- 仅为 Jira 暴露出的新增风险、异常、恢复、边界或兼容场景补写用例。
- 如果 Jira 内容与现有用例部分重叠，优先补写缺失分支，而不是简单复制。

## 5.5 review Jira delta 并输出 `delta/delta_step5_jira_reviewed.md`

对 `working_dir/delta/delta_step5_jira.md` 做一次 review，再输出：

- `working_dir/delta/delta_step5_jira_reviewed.md`

在 review 开始前，先用以下脚本做格式测试：

```bash
python scripts/validate_testrail_case.py --source <working_dir/delta/delta_step5_jira.md 的绝对路径>
```

规则：

- `--source` 必须传 testcase 文件的绝对路径。
- 如果脚本解析失败、提示结构不合法或怀疑乱码，先修 testcase 格式或编码，再继续后续 review。

review 必查项：

1. 新增用例是否与 Jira issue 正文对齐，而不是只对齐标题
2. 能拆成多条用例的 Jira 场景是否已经拆开
3. 是否仍存在“把多条用例藏进一个 case 步骤里”的情况
4. 是否只保留了 Jira 带来的净新增项，而不是重复 baseline
5. 是否符合 `references/testrail_default.md` 的模板结构，并能被 parser 成功解析

回修规则：

- 发现与 Jira 正文不对齐、粒度过粗、场景漏写、模板不齐或 parser 解析失败时，先回修，再输出 reviewed 版本。
- 后续 Step 6 读取的是 `baseline/testcase_base_reviewed.md` + `delta/delta_step5_jira_reviewed.md`，不要把它们手工复制成新的整文件。

# Step 5：补充 Jira 用例并 review

## 目录

- 5.1 输入与全文读取要求
- 5.2 查询并筛选相关 Jira
- 5.3 向用户确认相关 Jira
- 5.4 追加 Jira 补充用例并输出 `testcase_jira.md`
- 5.5 review Jira 增补版并输出 `testcase_jira_reviewed.md`

## 5.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- Step 2 已确认的 `core_keywords`、`expansion_keywords`、功能摘要、主体产品信息
- Step 4 使用过的原始需求文档、Drive 补充文档、SmartX 产品手册 / 白皮书
- `working_dir/testcase_1_direct_reviewed.md`

执行要求：

- 不要只拿 `testcase_1_direct_reviewed.md` 的标题或少数 case 做 Jira 补充。
- 重新阅读全文版 testcase，先总结当前已经覆盖的测试角度，再去找 Jira 缺口。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤全文读取的资料和 testcase 文件。

## 5.2 查询并筛选相关 Jira

围绕 Step 2 已确认的关键词执行 Jira 检索。默认先使用以下配置：

- Jira 站点：`http://jira.smartx.com`
- 用户名：`renyu.zhang`
- 密码：`Zhangry-2001`

如果用户提供了新的 Jira 地址或凭据，则以用户最新提供的信息覆盖默认配置。

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

## 5.3 向用户确认相关 Jira

在继续之前，必须显式向用户展示并确认：

1. 直接相关 Jira 列表
2. 每条 Jira 为什么相关
3. 可转化为测试点的风险 / 异常 / 恢复 / 兼容性线索
4. 当前仍存疑的 Jira

要求：

- 必须等待用户确认或修正
- 未经用户确认，不要进入 Jira 用例补写

## 5.4 追加 Jira 补充用例并输出 `testcase_jira.md`

以 `working_dir/testcase_1_direct_reviewed.md` 为基础，在文件末尾追加 Jira 补充用例，输出：

- `working_dir/testcase_jira.md`

追加要求：

- 每条由 Jira 派生的用例都要显式标注 Jira 号
- 推荐在用例名称或 `描述：` 中保留 Jira 号，例如 `JIRA: ABC-123`
- 不要覆盖或删除 direct reviewed 版本中已有的有效用例
- 仅为 Jira 暴露出的新增风险、异常、恢复、边界或兼容场景补写用例
- 如果 Jira 内容与现有用例部分重叠，优先补写缺失分支，而不是简单复制

## 5.5 review Jira 增补版并输出 `testcase_jira_reviewed.md`

对 `working_dir/testcase_jira.md` 做一次 review，再输出：

- `working_dir/testcase_jira_reviewed.md`

review 必查项：

1. 新增用例是否与 Jira issue 正文对齐，而不是只对齐标题
2. 能拆成多条用例的 Jira 场景是否已经拆开
3. 是否仍存在“把多条用例藏进一个 case 步骤里”的情况
4. 是否保留了 `testcase_1_direct_reviewed.md` 的全部有效内容
5. 是否符合 `references/testrail_default.md` 的模板结构

回修规则：

- 发现与 Jira 正文不对齐、粒度过粗、场景漏写或模板不齐时，先回修，再输出 reviewed 版本。
- 后续 Step 6 只能以 `working_dir/testcase_jira_reviewed.md` 为基线，不要退回 `testcase_1_direct_reviewed.md`。

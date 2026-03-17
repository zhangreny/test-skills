---
name: testcase-generate
description: 根据用户提供的需求文档路径、目录路径或 Google Docs URL 生成 SmartX 功能测试用例。适用于“生成测试用例”“根据文档写测试点”“输出 TestRail 格式用例”等请求。流程包括：先归一化输入并在需要时下载 Google Docs、再校验与盘点输入文件、先单独完成文档分析与用户确认、准备相关 Drive 资料、补充查询 Jira 历史 issue、再结合本地 SmartX 文档确认测试角度，最终输出符合 TestRail 结构的测试用例。
---

# Testcase Generate

按以下顺序执行，不要跳步：

**Step 0：归一化输入 -> Step 1：盘点输入文件 -> Step 2：先分析原始需求并让用户确认 -> Step 3：补齐相关 Drive 文档 -> Step 4：查询并摘要 Jira 并让用户确认 -> Step 5：整合资料、补齐工具与历史矩阵并统一确认测试设计 -> Step 6：生成、补缺并 review 测试用例**

## 使用方式

- 先读本文件，再按当前阶段按需读取对应的 `references/*.md`，不要一开始把所有参考文件一次性载入上下文。
- 各种包含中文的 markdown、json、txt、中间产物文件，默认优先按 UTF-8 编码读取和写入；不要依赖系统默认编码，避免出现乱码。
- 如果任务只进行到某个阶段，例如用户只要需求分析或只要补查 Jira，就只读取并执行该阶段之前所需的参考文件。
- 只有完成本阶段要求的用户确认后，才能进入下一阶段：
  - Step 2 确认后，才能进入 Step 3 和 Step 4。
  - Step 4 确认后，才能进入 Step 5。
  - Step 5 确认后，才能进入 Step 6。
- `references/testrail_default.md` 只在最终 testcase 渲染和 reviewer 结构检查时读取，不要提前用它替代业务分析。

## 参考文件导航

- Step 0-2：读取 [references/step-0-2-input-and-analysis.md](references/step-0-2-input-and-analysis.md)
  - 适用：输入归一化、Google Docs 下载、文件盘点、需求摘要、产品与关键词确认
- Step 3-4：读取 [references/step-3-4-drive-and-jira.md](references/step-3-4-drive-and-jira.md)
  - 适用：相关 Drive 文档准备、Jira 检索、相关性筛选、Jira 结果确认
- Step 5：读取 [references/step-5-test-design.md](references/step-5-test-design.md)
  - 适用：整合原始需求、Drive 资料、SmartX 本地文档与 Jira 结果，输出测试对象、工具矩阵、历史矩阵与 `coverage_expansion_plan`
- Step 5 通用维度：按需读取 [references/test-design-dimensions.md](references/test-design-dimensions.md)
  - 适用：把验收、功能、边界、可靠性、用户场景、压力、规格、兼容性、扩缩容、升级等维度显式纳入测试设计
- Step 6：读取 [references/step-6-generation-and-review.md](references/step-6-generation-and-review.md)
  - 适用：按 TestRail 风格生成 testcase、做 seeds 补缺循环、合并终稿、执行 reviewer 复核
- 最终自检：读取 [references/quality-checklist.md](references/quality-checklist.md)
  - 适用：最终输出前做强制质量核对
- 输出结构模板：读取 [references/testrail_default.md](references/testrail_default.md)
  - 适用：检查 `## 模块 -> ### 子模块 -> #### 用例` 的层级、描述和 `【Step1】` 至 `【Step3】`

## 强制规则

- 不要跳过“原始需求分析确认”“Jira 摘要确认”“测试对象与 coverage_expansion_plan 确认”这三轮显式确认。
- 不要在缺少关键文档、关键 Jira 结果或关键执行/观测路径时直接生成终稿。
- 不要直接从测试角度写大纲式用例；必须先经过原子 `case_seed` 与补缺循环，再渲染最终 testcase。
- 把“原子”视为最低交付粒度，不要把它当成停止条件；只要还能继续按对象差异、条件差异、输入差异、状态差异、结果差异、观测差异、生命周期阶段或成对路径继续拆细，就继续拆，默认宁细勿粗。
- 不要把历史用例、模式文档或模板示例直接抄进最终业务用例；它们只用于补充拆点、矩阵和命名习惯。
- 不要把 review 前的草案直接交给用户；最终交付必须是 reviewer 回修后的 `testcase_final.md` 正文。

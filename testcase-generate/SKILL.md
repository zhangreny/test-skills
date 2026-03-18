---
name: testcase-generate
description: 根据用户提供的需求文档路径、目录路径或 Google Docs URL 生成 SmartX 功能测试用例。适用于“生成测试用例”“根据文档写测试点”“输出 TestRail 格式用例”等请求。流程包括：先归一化输入并在需要时下载 Google Docs、盘点输入文件、分析原始需求并确认产品与关键词、准备 Google Drive 补充文档、强制全量读取用户上传文档与 Drive 补充文档、按需读取 SmartX 产品手册与技术白皮书后直接生成详细 testcase 初稿、再结合 Jira 历史问题、本地历史 testcase 样本、通用测试维度和组别 pattern 逐步补齐并 review，最终输出 TestRail 结构的终稿。
---

# Testcase Generate

按以下顺序执行，不要跳步：

**Step 0：归一化输入 -> Step 1：盘点输入文件 -> Step 2：分析原始需求并让用户确认 -> Step 3：准备相关 Drive 文档 -> Step 4：强制全量读取用户与 Drive 文档、按需读取 SmartX 产品文档并直接生成首版用例 -> Step 5：补充 Jira 用例并 review -> Step 6：补充本地历史近邻用例并让用户确认 -> Step 7：按通用测试维度做缺口分析 -> Step 8：做组别 pattern 学习并输出终稿**

## 使用方式

- 先读本文，再按当前阶段按需读取对应的 `references/*.md`，不要一开始加载所有 reference。
- 默认按 UTF-8 读取和写入 markdown、json、txt 与中间产物，避免编码混乱。
- 如果任务只做到某一阶段，只读取到该阶段为止需要的 reference。
- 只有完成当前阶段要求的显式确认后，才能进入下一阶段：
  - Step 2 确认后，才能进入 Step 3 和 Step 4。
  - Step 5 的 Jira 相关性必须经用户确认后，才能写入 Jira 补充用例。
  - Step 6 的近邻缺口必须经用户确认后，才能写入历史近邻补充用例。
- 只在生成或 review testcase 时读取 `references/testrail_default.md`，不要让模板替代业务理解。
- 在 Step 4、Step 5、Step 6、Step 8 的 testcase review 阶段，可使用 `../testrail-testcase-extract-upload/scripts/parse_testrail_template.py` 对当前 testcase markdown 做结构校验；解析失败时先修格式，再继续业务 review。

## 全量读取与内容递增规则

- 从 Step 4 开始，把“用户上传文档 + Drive 补充文档全文读取”视为强制要求，不要只读关键词、标题、摘要或局部片段替代正文。
- 对进入 Step 4 的原始需求文档和 Drive 补充文档，逐份阅读全文或逐段完整读取提取后的全文。
- 对 `../smartx-docs-download/markdown_docs` 中选中的相关产品手册、管理指南、用户指南、技术白皮书、特性说明、升级/兼容/规格文档，必须读取，但允许按当前 feature 相关章节、相关对象、相关流程、相关限制和相关故障路径按需读取，不要求全文通读整本文档。
- 对每一步产出的 testcase 文件，下一步必须全文读取，不允许只看标题、部分章节或抽样用例。
- 从 Step 4 开始维护 `working_dir/full_read_manifest.md`，逐步记录每一步完整读取了哪些资料、按需读取了哪些产品文档章节，以及完整读取了哪些 testcase 文件。
- 保持下游输入集合单调递增：后一步允许新增资料，不允许把前一步已经纳入的有效正文缩减成更少的内容。
- 如果某份前序资料在后序步骤被判定为无关，明确说明剔除理由；否则默认继续保留并全文纳入后续分析。

## 参考文件导航

- Step 0-2：读取 [references/step-0-2-input-and-analysis.md](references/step-0-2-input-and-analysis.md)
- Step 3：读取 [references/step-3-drive-materials.md](references/step-3-drive-materials.md)
- Step 4：读取 [references/step-4-direct-generation.md](references/step-4-direct-generation.md)
- Step 5：读取 [references/step-5-jira-augmentation.md](references/step-5-jira-augmentation.md)
- Step 6：读取 [references/step-6-former-case-augmentation.md](references/step-6-former-case-augmentation.md)
- Step 7：读取 [references/test-design-dimensions.md](references/test-design-dimensions.md)
- Step 8：读取 [references/step-8-pattern-finalization.md](references/step-8-pattern-finalization.md)
- 最终自检：读取 [references/quality-checklist.md](references/quality-checklist.md)
- 模板结构：读取 [references/testrail_default.md](references/testrail_default.md)

## 强制规则

- 不要跳过“原始需求确认”“Jira 相关性确认”“近邻缺口确认”这三轮显式确认。
- 不要在 Step 4 之后退回到“只靠关键词检索”的窄上下文；后续阶段必须基于全文材料和全文 testcase 文件继续工作。
- 不要使用 seeds、seed plan、gap loop 等原子 seed 流程；从 Step 4 起直接生成 testcase 正文，并在各步做补充和 review。
- 不要把多个可独立验证的核心结果藏在同一条 case 的步骤里；能拆则拆。
- 不要让后续生成的 testcase 文件覆盖掉前一步已保留的正文；后续文件应在前一步基础上补充、修订，并保持内容不少于前一步。
- 不要把历史样本、pattern 文档或模板示例直接照抄到最终业务 testcase；只继承场景、矩阵、粒度、工具、命名和范围习惯。

---
name: testcase-generate
description: 根据用户提供的需求文档路径、目录路径、Google Docs URL 或上传文件生成 SmartX 功能测试用例。先在 Downloads 下创建工作目录并写入 `input-manifest.json`，展开并确认本轮输入资料后，再进入原始需求分析、Drive/Jira/历史近邻/pattern 增补与最终 TestRail 用例生成。固定执行完整流程，不再提供分级模式；默认依次执行 Step 0-17，并在 Step 5-15 产出各类 delta、在终稿前强制读取 `references/finalcheck.md` 做类似用户记忆的逐项校验。适用于“生成测试用例”“根据文档写测试点”“输出 TestRail 格式用例”等请求。
---

# Testcase Generate

按以下顺序执行，不要跳步；直接执行完整 workflow，不再做分级选择：

**Step 0：创建输入工作目录并写入 `input-manifest.json` -> Step 1：检查输入并确认本轮资料范围 -> Step 2：分析原始需求并确认产品 / 关键词 -> Step 3：先询问是否需要按关键词补充 Google Drive 关联文档，再按用户选择处理 -> Step 4：初始化 working_dir、全文读取资料并生成 baseline -> Step 5：补充 Jira delta -> Step 6：补充本地历史近邻 delta -> Step 7：补充组别 pattern delta -> Step 8：合并 baseline 与前置 delta，细化并输出 `merged/testcase_basic_final.md` -> Step 9：边界专项 delta -> Step 10：兼容性专项 delta -> Step 11：压力专项 delta -> Step 12：用户场景专项 delta -> Step 13：升级专项 delta -> Step 14：扩缩容专项 delta -> Step 15：故障专项 delta -> Step 16：结构化合并 baseline 与各专项 delta -> Step 17：review、执行 finalcheck 记忆校验并输出终稿**

## Fixed Workflow

- 不再让用户在不同 workflow 档位之间选择；默认直接执行完整 Step 0-17。
- Step 2 只确认分析结果本身：功能摘要、主体产品、`core_keywords`、`expansion_keywords` 与不确定点，不再确认 workflow 分级。
- Step 5-7 与 Step 9-15 默认全部执行；如果某一步经资料核对后确认没有新增有效 delta，也要保留 evidence / 收敛说明，而不是把该步骤当作未执行。
- 进入 Step 4 前，先运行：

```bash
python scripts/init_working_dir.py --existing-workdir <Step 0 创建的 working_dir 绝对路径>
```

- `scripts/init_working_dir.py` 会创建：
  - `working_dir/baseline`
  - `working_dir/delta`
  - `working_dir/merged`
  - `working_dir/reports`
  - `working_dir/full_read_manifest.md`
  - `working_dir/workflow_state.json`
  - 并保留 Step 0 已写入的 `working_dir/input-manifest.json`
  - 如果没有现成的 intake working_dir，也可以改用 `--output-dir`；未显式传入 `--output-dir` 时，新的 `working_dir` 默认创建在系统 `Downloads` 下，而不是系统临时目录。

## 使用方式

- 先读本文，再按当前阶段按需读取对应的 `references/*.md`，不要一开始加载所有 reference。
- 默认按 UTF-8 读取和写入 markdown、json、txt 与中间产物，避免编码混乱。
- 如果任务只做到某一阶段，只读取到该阶段为止需要的 reference。
- Step 1 的“输入检查 + 本轮资料范围确认”是强制确认点；用户没确认前，不要进入需求分析。
- Step 2 的“原始需求分析 + 产品 / 关键词确认”仍然是强制确认点。
- Step 1 结束后，后续流程应看到的是“已确认的本地文件集合 + 已确认的 Google Docs URL 清单”；不要把未经确认的目录扫描结果直接带入 Step 2 之后。
- 在调用 `../all-related-file-preparer-4-testcase-generate/SKILL.md` 之前，必须显式问用户：是否需要根据已确认关键词去 Google Drive 搜索关联文档。
- 如果用户明确表示“不需要”“只用当前文档”“不要搜 Drive”等语义，则跳过 `Step 3` 的子 skill 调用，后续只使用当前已上传 / 已确认的文档继续 testcase 生成。
- 如果 Step 1.5 下载用户提供的 Google Docs 失败，必须明确告诉用户“哪些链接/ID 下载失败了”，并要求用户手动上传这些链接对应的 Markdown 文件；拿到上传文件后，先更新 `input-manifest.json`，再回到 Step 1 重新确认输入范围。
- 从 Step 17 开始，把 `references/finalcheck.md` 视为“用户记忆型终稿校验清单”：终稿返回前必须全文读取，并逐条检查当前 testcase 是否满足其中的场景偏好、粒度偏好和常见修改习惯。
- `references/finalcheck.md` 是持久沉淀，不是本次需求文档的替代品；它只用于终稿收口和风格/覆盖纠偏，不能覆盖当前需求、产品文档和显式用户指令。
- `references/finalcheck.md` 的写入只能由用户主动触发；如果用户没有明确提出“保存这轮改进要点”“沉淀到 finalcheck”之类请求，一律不写入。
- 即使用户已触发写入，也必须先给出“拟写入 `finalcheck.md` 的预览摘要”，并明确提示“后续生成 testcase 时会把这些内容作为额外校验依据逐条检查”；只有用户确认后，才真正写入 `references/finalcheck.md`。
- 更新 `references/finalcheck.md` 时，只总结“用户这次明确修改过、确认过”的场景与用例写法，不要把整份 testcase 或未确认猜测直接贴进去。
- Step 5 与 Step 6 默认采用“高置信度直接继续，低置信度才强制确认”的策略：
  - 如果候选集高度集中、证据直连当前 feature、且没有 competing cluster，先写摘要到 `working_dir/reports/*.md`，再继续。
  - 如果存在多个等价候选簇、边缘命中项较多、或和当前 feature 的映射仍有分歧，再停下来让用户确认。
- 只在生成或 review testcase 时读取 `references/testrail_default.md`，不要让模板替代业务理解。
- 记录 `full_read_manifest.md` 时，优先使用：

```bash
python scripts/append_full_read_manifest.py --manifest <working_dir/full_read_manifest.md 的绝对路径> --step <步骤> --round <base|1|2|...> --source-type <类型> --path <绝对路径> --scope <读取范围> --why-read <原因>
```

- 对 testcase markdown 做 parser 校验时，优先使用：

```bash
python scripts/validate_testrail_case.py --source <testcase 文件绝对路径>
```

- 对 Step 9 到 Step 15 的专项 delta 做“资料依据 + 历史近邻 + 收敛记录”校验时，额外使用：

```bash
python scripts/validate_specialized_delta_context.py --step <9-15> --round <1|2|...> --manifest <working_dir/full_read_manifest.md 的绝对路径> --former-case-selection <working_dir/former_case_selection.md 的绝对路径> --base-testcase <working_dir/merged/testcase_basic_final.md 的绝对路径> --report <working_dir/reports/stepX_*_roundY_evidence.md 的绝对路径> --delta <working_dir/delta/delta_stepX_*_Y.md 的绝对路径> [--previous-delta <上一轮 delta 绝对路径>]
```

- 做基线与 delta 结构化合并时，优先使用：

```bash
python scripts/merge_testcase_variants.py --base <baseline 文件绝对路径> --delta <delta 文件绝对路径> --output <merged 文件绝对路径> --map-output <merge_map 文件绝对路径>
```

- 多轮步骤的起始轮次和最大轮次，不再固定写死为 3；先读取 `working_dir/workflow_state.json` 里的 `round_policy`。
- 所有多轮步骤都使用同一套硬收敛规则：
  - 连续两轮 `new_top_level_scenarios = 0` 且 `new_leaf_cases = 0` 时停止。
  - 当前轮 `new_leaf_cases < 3` 且没有未解决 blocker 时停止。
- 到达当前步骤配置的 `max_rounds` 时停止。
  - 只有在出现新的一级场景、当前轮净新增叶子 case 不少于 3、或仍有未解决 blocker 时，才继续下一轮。
- Step 5-15 默认产出 delta 文件，不要把完整 baseline 一遍遍复制到后续步骤。
- Step 8、Step 16、Step 17 才产出结构化合并后的完整 testcase 快照。

## 全量读取与内容递增规则

- 从 Step 4 开始，把“用户上传文档 + Drive 补充文档全文读取”视为强制要求，不要只读关键词、标题、摘要或局部片段替代正文。
- 对进入 Step 4 的原始需求文档和 Drive 补充文档，逐份阅读全文或逐段完整读取提取后的全文。
- 对 `../smartx-docs-download/markdown_docs` 中选中的相关产品手册、管理指南、用户指南、技术白皮书、特性说明、升级/兼容/规格文档，必须读取，但允许按当前 feature 相关章节、相关对象、相关流程、相关限制和相关故障路径按需读取，不要求全文通读整本文档。
- 对基线文件、delta 文件和最终 merged 文件，后续步骤读取“与当前步骤直接相关的完整输入集合”；不要只看标题、局部段落或抽样 case。
- 从 Step 4 开始维护 `working_dir/full_read_manifest.md`，逐步记录每一步完整读取了哪些资料、按需读取了哪些产品文档章节，以及完整读取了哪些 baseline / delta / merged testcase 文件。
- `working_dir/full_read_manifest.md` 中每条记录至少写清：`step`、`round`（无轮次时写 `base`）、`source_type`、`path`、`scope`、`why_read`。`source_type` 至少区分 `user_upload`、`drive_doc`、`product_doc`、`testcase`、`former_case`、`pattern`、`fault_reference`。
- 保持“有效合并后范围”单调递增：后一步允许新增资料，不允许把前一步已经确认有效的 testcase 内容无理由丢掉；但 delta 文件本身只保存新增、拆细或修订项，不需要复制整份基线。
- 如果某份前序资料在后序步骤被判定为无关，明确说明剔除理由；否则默认继续保留并全文纳入后续分析。
- Step 9 到 Step 15 的每一轮，在写 delta 前必须先输出一份 `working_dir/reports/stepX_*_roundY_evidence.md`，至少包含：
  - `## 本轮输入清单`
  - `## 历史近邻继承点`
  - `## 当前缺口判断`
  - `## 新增用例与依据映射`
  - `## 收敛记录`
- Step 9 到 Step 15 的新增内容，必须能映射回 `full_read_manifest.md` 中已读资料、`former_case_selection.md` 命中的历史样本，以及 Step 15 的 `references/fault/` 文件；不能只凭通用测试维度臆造专项。
- Step 15 额外强制要求：每一轮都必须全文读取 `references/fault/*.csv` 下全部 CSV 文件里的全部故障场景，不能只挑“看起来相关”的几个文件；并且要把这批文件逐个记到当轮的 `full_read_manifest.md` 与 `step15_fault_round<round>_evidence.md` 里。

## 参考文件导航

- Step 0-2：读取 [references/step-0-2-input-and-analysis.md](references/step-0-2-input-and-analysis.md)
- Step 3：读取 [references/step-3-drive-materials.md](references/step-3-drive-materials.md)
- Step 4：读取 [references/step-4-direct-generation.md](references/step-4-direct-generation.md)
- Step 5：读取 [references/step-5-jira-augmentation.md](references/step-5-jira-augmentation.md)
- Step 6：读取 [references/step-6-former-case-augmentation.md](references/step-6-former-case-augmentation.md)
- Step 7：读取 [references/step-7-basic-pattern.md](references/step-7-basic-pattern.md)
- Step 8：读取 [references/step-8-basic-final-review.md](references/step-8-basic-final-review.md)
- Step 9：读取 [references/step-9-border-augmentation.md](references/step-9-border-augmentation.md)
- Step 10：读取 [references/step-10-compatibility-augmentation.md](references/step-10-compatibility-augmentation.md)
- Step 11：读取 [references/step-11-stress-augmentation.md](references/step-11-stress-augmentation.md)
- Step 12：读取 [references/step-12-user-scenario-augmentation.md](references/step-12-user-scenario-augmentation.md)
- Step 13：读取 [references/step-13-upgrade-augmentation.md](references/step-13-upgrade-augmentation.md)
- Step 14：读取 [references/step-14-scale-augmentation.md](references/step-14-scale-augmentation.md)
- Step 15：读取 [references/step-15-fault-augmentation.md](references/step-15-fault-augmentation.md)
- Step 16：读取 [references/step-16-final-merge.md](references/step-16-final-merge.md)
- Step 17：读取 [references/step-17-final-review.md](references/step-17-final-review.md)
- 终稿记忆校验：读取 [references/finalcheck.md](references/finalcheck.md)
- 最终自检：读取 [references/quality-checklist.md](references/quality-checklist.md)
- 模板结构：读取 [references/testrail_default.md](references/testrail_default.md)

## 强制规则

- 不要跳过“原始需求确认”。
- Step 5 与 Step 6 只有在低置信度、强歧义或用户要求人工把关时，才升级为显式确认点。
- 不要在 Step 4 之后退回到“只靠关键词检索”的窄上下文；后续阶段必须基于全文材料和全文 testcase 文件继续工作。
- 不要使用 seeds、seed plan、gap loop 等原子 seed 流程；从 Step 4 起直接生成 testcase 正文，并在各步做补充和 review。
- 不要把多个可独立验证的核心结果藏在同一条 case 的步骤里；能拆则拆。
- 不要手工把整份 testcase 从上一步复制到下一步；Step 5-15 输出 delta，Step 8/16/17 再做结构化合并。
- 旧 `references/test-design-dimensions.md` 已废弃，不再作为执行入口。
- Step 8 到 Step 15 以及 Step 17 的每一轮都要明确记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases` 与 `continue_or_stop_reason`。
- Step 9 到 Step 15 的中间结果要按步骤自己的文件名保留，不要只在脑中“做过一轮”却不落盘。
- Step 9 到 Step 15 的每一轮都必须同时落盘 evidence report，并在 parser 通过后再跑 `scripts/validate_specialized_delta_context.py`；若 evidence report 或依据映射不完整，该轮不能算完成。
- 不要把历史样本、pattern 文档或模板示例直接照抄到最终业务 testcase；只继承场景、矩阵、粒度、工具、命名和范围习惯。
- 不要跳过 `references/finalcheck.md` 的终稿校验；其中每条“场景记录 / 用例记录”都要过一遍当前终稿，确认已满足、已显式不适用，或已在本轮修正。
- 没有用户主动触发时，不要改写 `references/finalcheck.md`；用户触发后，也必须先预览待写入内容并拿到确认，再记录稳定偏好和修改结论。
- 最终输出给用户的必须是 review 后的 `working_dir/merged/testcase_final_reviewed.md` 正文，而不是 baseline、delta、专项中间稿或未 review 的合并稿。

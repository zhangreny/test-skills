# Step 17：review 终稿并输出 `merged/testcase_final_reviewed.md`

## 目录

- 17.1 输入与全文读取要求
- 17.2 第 1 轮：来源覆盖与遗漏检查
- 17.3 第 2 轮：粒度与重复检查
- 17.4 第 3 轮：执行闭环与格式检查
- 17.5 合并 review delta 并输出 `merged/testcase_final_reviewed.md`

## 17.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_final.md`
- `working_dir/reports/final_merge_map.md`
- `working_dir/full_read_manifest.md`
- `working_dir/merged/testcase_basic_final.md`
- Step 9 到 Step 15 实际执行步骤中，编号最大的 delta 文件

执行要求：

- 每一轮都重新读取 `working_dir/merged/testcase_final.md` 或上一轮 review delta 输出，不允许只抽样读几段。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_17`。
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。

## 17.2 第 1 轮：来源覆盖与遗漏检查

使用 17.1 的同一批材料，从“所有来源是否都在终稿中有落点”角度做第一轮 review delta，输出：

- `working_dir/delta/delta_step17_final_review_1.md`

本轮重点：

- `testcase_basic_final.md` 的有效内容是否全部保留。
- 各专项 delta 中的有效新增内容是否都进入终稿。
- `final_merge_map.md` 是否存在明显错误的去重或遗漏。

输出后先跑一次 parser；解析失败先修格式，再进入下一轮。

## 17.3 第 2 轮：粒度与重复检查

继续使用 17.1 的同一批材料，并全文读取 `working_dir/delta/delta_step17_final_review_1.md`，从“还能否继续拆细、是否仍有重复或交叉污染”角度做第二轮 review delta，输出：

- `working_dir/delta/delta_step17_final_review_2.md`

本轮重点：

- 是否仍存在“在步骤里藏多条用例”的情况。
- 是否因为多专项合并，导致不同场景被错误地压回一条 case。
- 是否存在标题不同但正文几乎重复的 case，需要重新整理。

输出后先跑一次 parser；解析失败先修格式，再进入下一轮。

## 17.4 第 3 轮：执行闭环与格式检查

继续使用 17.1 的同一批材料，并全文读取 `working_dir/delta/delta_step17_final_review_2.md`，从“执行闭环、观测闭环、格式闭环”角度做第三轮 review delta，输出：

- `working_dir/delta/delta_step17_final_review_3.md`

本轮重点：

- 每条 case 是否具备清晰前置、执行、观测、预期与必要的回退 / 清理。
- 是否还有缺少日志、告警、任务状态、CLI / API / GUI 观测路径的 case。
- 是否完全符合 `references/testrail_default.md` 的模板结构。

输出后先跑一次 parser；解析失败先修格式，再进入收敛阶段。

## 17.5 合并 review delta 并输出 `merged/testcase_final_reviewed.md`

先用 merge 脚本把 review delta 合回终稿。命令里只传“本次实际存在”的 review delta 文件，不要硬凑不存在的轮次：

```bash
python scripts/merge_testcase_variants.py --base <working_dir/merged/testcase_final.md 的绝对路径> --delta <本次实际存在的 Step 17 review delta 文件绝对路径> --output <working_dir/merged/testcase_final_reviewed_assembled.md 的绝对路径> --map-output <working_dir/reports/final_review_merge_map.md 的绝对路径>
```

再基于 assembled 稿收敛输出：

- `working_dir/merged/testcase_final_reviewed.md`

要求：

- `testcase_final_reviewed_assembled.md` 是 review delta 合回后的结构化拼装稿，允许在此基础上做最后一轮去重和拆细。
- 这是最终返回给用户的正文。
- 不要返回 baseline、delta、各专项中间稿、`testcase_final.md` 或其他未修订版本。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step17_final_review_4.md`、`delta_step17_final_review_5.md`，直到硬收敛。

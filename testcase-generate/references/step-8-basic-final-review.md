# Step 8：合并 baseline 与前置 delta，拆细并输出 `merged/testcase_basic_final.md`

## 目录

- 8.1 输入与全文读取要求
- 8.2 第 1 轮：功能与验收闭环
- 8.3 第 2 轮：拆细隐藏的复合 case
- 8.4 第 3 轮：规格、约束与观测闭环
- 8.5 结构化合并并输出 `merged/testcase_basic_final.md`

## 8.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/baseline/testcase_base_reviewed.md`
- `working_dir/delta/delta_step5_jira_reviewed.md`
- `working_dir/delta/delta_step6_former_case_reviewed.md`
- `working_dir/delta/delta_step7_pattern_reviewed.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`
- Step 4 到 Step 7 使用过的正文资料

执行要求：

- 每一轮开始前都重新阅读 `working_dir/full_read_manifest.md`。
- 每一轮都要全文读取当前轮需要参考的 baseline 与 delta 输入。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加 `source_type: testcase` 的读取记录。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_8`：
  - 默认 3 轮，最多 5 轮
- 每一轮都记录：`new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`

## 8.2 第 1 轮：功能与验收闭环

使用与 8.1 相同的材料，从“功能闭环、验收闭环、主流程是否完整”的角度做第一轮 delta review，输出：

- `working_dir/delta/delta_step8_basic_review_1.md`

输出后先跑一次 parser；解析失败先修格式，再进入下一轮。

## 8.3 第 2 轮：拆细隐藏的复合 case

继续使用 8.1 的同一批材料，并全文读取上一轮输出 `working_dir/delta/delta_step8_basic_review_1.md`，从“粒度拆细”的角度做第二轮 delta review，输出：

- `working_dir/delta/delta_step8_basic_review_2.md`

输出后先跑一次 parser；解析失败先修格式，再进入下一轮。

## 8.4 第 3 轮：规格、约束与观测闭环

继续使用 8.1 的同一批材料，并全文读取上一轮输出 `working_dir/delta/delta_step8_basic_review_2.md`，从“规格与执行闭环”的角度做第三轮 delta review，输出：

- `working_dir/delta/delta_step8_basic_review_3.md`

输出后先跑一次 parser；解析失败先修格式，再进入收敛阶段。

如果第三轮后仍然满足继续条件且未触达 `max_rounds`，继续输出 `delta_step8_basic_review_4.md`、`delta_step8_basic_review_5.md`，直到硬收敛。

## 8.5 结构化合并并输出 `merged/testcase_basic_final.md`

先用 merge 脚本生成结构化合并稿，再收敛输出最终基础稿。命令里只传“本次实际存在”的 delta 文件和 round 文件：

```bash
python scripts/merge_testcase_variants.py --base <working_dir/baseline/testcase_base_reviewed.md 的绝对路径> --delta <本次实际存在的 Step 5/6/7/8 delta 文件绝对路径> --output <working_dir/merged/testcase_basic_assembled.md 的绝对路径> --map-output <working_dir/reports/testcase_basic_merge_map.md 的绝对路径>
```

再基于 assembled 稿做收敛输出：

- `working_dir/merged/testcase_basic_final.md`

要求：

- `testcase_basic_assembled.md` 是 merge 脚本生成的结构化拼装稿，允许在此基础上做去粗取精和手工去重。
- `testcase_basic_final.md` 必须保留 assembled 稿里的全部有效内容，但可以去掉已经被拆细替代的粗粒度重复 case。
- 明确把 `merged/testcase_basic_final.md` 视为后续专项步骤的基础底稿。
- 不要把 Step 9 到 Step 15 的专项内容提前混回这个文件；专项补充继续以 delta 形式单独产出。

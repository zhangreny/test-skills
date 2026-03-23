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
- `working_dir/delta/delta_step5_jira_reviewed.md`（如果 Step 5 实际执行）
- `working_dir/delta/delta_step6_former_case_reviewed.md`（如果 Step 6 实际执行）
- `working_dir/delta/delta_step7_pattern_reviewed.md`（如果 Step 7 实际执行）
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`
- Step 4 到 Step 7 使用过的正文资料

执行要求：

- 每一轮开始前都重新阅读 `working_dir/full_read_manifest.md`，确认前序已经完整读取过哪些资料。
- 每一轮都要全文读取当前轮需要参考的 baseline / delta 输入，不允许只抽样看几条 case。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加一条 `source_type: testcase` 的读取记录，并写明 `round`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_8`：
  - `lite`：默认 1 轮，最多 2 轮
  - `standard`：默认 2 轮，最多 3 轮
  - `deep`：默认 3 轮，最多 5 轮
- 每一轮都记录：`new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`

## 8.2 第 1 轮：功能与验收闭环

使用与 8.1 相同的材料，从“功能闭环、验收闭环、主流程是否完整”角度做第一轮 delta review，输出：

- `working_dir/delta/delta_step8_basic_review_1.md`

本轮重点：

- 用户文档和 Drive 文档中明确写过的功能、对象、入口和结果是否全部落进用例。
- 前后端联动、端到端主流程、常见运维闭环是否已经覆盖。
- 当前 baseline + 前置 delta 的有效合并范围里，是否还有明显缺的主场景。

输出后先跑一次 parser；解析失败先修格式，再进入下一轮。

## 8.3 第 2 轮：拆细隐藏的复合 case

继续使用 8.1 的同一批材料，并全文读取上一轮输出 `working_dir/delta/delta_step8_basic_review_1.md`，从“粒度拆细”角度做第二轮 delta review，输出：

- `working_dir/delta/delta_step8_basic_review_2.md`

本轮重点：

- 一条 case 里是否混进了多个前置条件、多个对象变化、多个异常分支或多个验证目标。
- 是否需要按入口差异、状态切换差异、清理 / 回退差异、观测方式差异拆成独立 case。
- 是否存在“描述里写了很多验证点，但步骤和预期仍然过粗”的情况。

输出后先跑一次 parser；解析失败先修格式，再进入下一轮。

## 8.4 第 3 轮：规格、约束与观测闭环

继续使用 8.1 的同一批材料，并全文读取上一轮输出 `working_dir/delta/delta_step8_basic_review_2.md`，从“规格与执行闭环”角度做第三轮 delta review，输出：

- `working_dir/delta/delta_step8_basic_review_3.md`

本轮重点：

- 文档里的前置条件、限制条件、角色权限、可观测信号、回退与清理要求是否都落进用例。
- 规格类信息是否只停留在描述，没有变成可执行 case。
- 是否还有能拆却未拆的 case。

输出后先跑一次 parser；解析失败先修格式，再进入收敛阶段。

## 8.5 结构化合并并输出 `merged/testcase_basic_final.md`

先用 merge 脚本生成结构化合并稿，再收敛输出最终基础稿。命令里只传“本次实际存在”的 delta 文件和 round 文件，不要虚构不存在的输入：

```bash
python scripts/merge_testcase_variants.py --base <working_dir/baseline/testcase_base_reviewed.md 的绝对路径> --delta <本次实际存在的 Step 5/6/7/8 delta 文件绝对路径> --output <working_dir/merged/testcase_basic_assembled.md 的绝对路径> --map-output <working_dir/reports/testcase_basic_merge_map.md 的绝对路径>
```

再基于 assembled 稿做收敛输出：

- `working_dir/merged/testcase_basic_final.md`

收敛要求：

- `testcase_basic_assembled.md` 是 merge 脚本生成的结构化拼装稿，允许在此基础上做去粗取精和手工去重。
- `testcase_basic_final.md` 必须保留 assembled 稿里的全部有效内容，但可以去掉已经被拆细替代的粗粒度重复 case。
- 明确把 `merged/testcase_basic_final.md` 视为后续专项步骤的基础底稿。
- 不要把 Step 9 到 Step 15 的专项内容提前混回这个文件；专项补充继续以 delta 形式单独产出。
- 如果第三轮后仍然满足继续条件且 mode 允许，继续输出 `delta_step8_basic_review_4.md`、`delta_step8_basic_review_5.md`，直到硬收敛。

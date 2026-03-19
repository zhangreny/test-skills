# Step 15：做故障专项 delta 增强

## 目录

- 15.1 输入与全文读取要求
- 15.2 触发条件与数据源
- 15.3 第 1 轮：单点故障映射
- 15.4 第 2 轮：组合故障与恢复路径
- 15.5 第 3 轮：一致性、告警与自愈
- 15.6 输出规则

## 15.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`

执行要求：

- 每一轮都必须全文读取 `references/fault/` 目录下全部 `.csv` 文件里的全部故障场景，不能只挑与当前 feature 看起来最相关的几个文件。
- 在“全部读完”之后，再标记哪些故障场景与当前 feature 直接相关、哪些是间接相关或可迁移参考。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 每一轮写 delta 前，先输出 `working_dir/reports/step15_fault_round<round>_evidence.md`，把本轮实际引用的故障资料、历史近邻与新增场景依据映射落盘。
- 每一轮都要把全部 fault CSV 的 reread 记录逐个追加到 `working_dir/full_read_manifest.md`，`source_type` 写 `fault_reference`；如果还重新打开了具体的历史近邻样本，也把这些 reread 记录追加进去，`source_type` 写 `former_case`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 15.2 触发条件与数据源

本步骤的数据源来自：

- 用户上传文档：`working_dir/full_read_manifest.md` 中的 `source_type: user_upload`
- Drive 补充文档：`working_dir/full_read_manifest.md` 中的 `source_type: drive_doc`
- 过往用例：`working_dir/former_case_selection.md` 及其对应的 `../testcase-pattern-learning/former_cases`
- 故障参考资料：`references/fault/` 目录下全部 `.csv` 文件中的全部故障场景；完成全量读取后，再按当前 feature 依赖链做相关性归类与优先级排序

优先触发本步骤的信号：

- 高可用、故障恢复、依赖组件异常、网络 / 硬件 / 软件故障、告警与自愈

## 15.3 第 1 轮：单点故障映射

使用 15.2 的同一批材料，从“当前 feature 依赖链上的单点故障注入”角度补充故障 delta，输出：

- `working_dir/delta/delta_step15_fault_1.md`

## 15.4 第 2 轮：组合故障与恢复路径

继续使用 15.2 的同一批材料，并全文读取 `working_dir/delta/delta_step15_fault_1.md`，从“连续故障、组合故障、人工干预恢复、重试与切换路径”角度补充故障 delta，输出：

- `working_dir/delta/delta_step15_fault_2.md`

## 15.5 第 3 轮：一致性、告警与自愈

继续使用 15.2 的同一批材料，并全文读取 `working_dir/delta/delta_step15_fault_2.md`，从“数据一致性、状态收敛、告警、日志、自愈 / 半自愈、恢复后清理”角度补充故障 delta，输出：

- `working_dir/delta/delta_step15_fault_3.md`

## 15.6 输出规则

- 每一轮输出后都先跑 parser；解析失败先修格式，再进入下一轮。
- parser 通过后，再执行：

```bash
python scripts/validate_specialized_delta_context.py --step 15 --round <round> --manifest <working_dir/full_read_manifest.md 的绝对路径> --former-case-selection <working_dir/former_case_selection.md 的绝对路径> --base-testcase <working_dir/merged/testcase_basic_final.md 的绝对路径> --report <working_dir/reports/step15_fault_round<round>_evidence.md 的绝对路径> --delta <working_dir/delta/delta_step15_fault_<round>.md 的绝对路径> [--previous-delta <上一轮 delta 绝对路径>]
```

- `step15_fault_round<round>_evidence.md` 至少包含以下章节：
  - `## 本轮输入清单`
  - `## 历史近邻继承点`
  - `## 当前缺口判断`
  - `## 新增用例与依据映射`
  - `## 收敛记录`
- `本轮输入清单` 必须逐个列出 `references/fault/*.csv` 下全部 fault CSV 的绝对路径，不能只写“看过 fault 目录”或只列其中一部分。
- `新增用例与依据映射` 可以只挑真正支撑当前 delta 的 fault 场景做映射，但前提仍然是全部 fault CSV 已在本轮完整读取并记录。
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step15_fault_4.md`、`delta_step15_fault_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step15_fault_*.md` 作为故障专项 delta。

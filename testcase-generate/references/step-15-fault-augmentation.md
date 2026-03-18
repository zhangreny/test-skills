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

- 每一轮都先重新确认 `references/fault/` 目录下哪些故障参考文件与当前 feature 相关。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 15.2 触发条件与数据源

本步骤的数据源来自：

- 用户上传文档：`working_dir/full_read_manifest.md` 中的 `source_type: user_upload`
- Drive 补充文档：`working_dir/full_read_manifest.md` 中的 `source_type: drive_doc`
- 过往用例：`working_dir/former_case_selection.md` 及其对应的 `../testcase-pattern-learning/former_cases`
- 故障参考资料：`references/fault/` 目录下的相关文件，按当前 feature 依赖链选择读取

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
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step15_fault_4.md`、`delta_step15_fault_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step15_fault_*.md` 作为故障专项 delta。

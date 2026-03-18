# Step 9：做边界测试专项 delta 增强

## 目录

- 9.1 输入与全文读取要求
- 9.2 触发条件与数据源
- 9.3 第 1 轮：输入值与范围边界
- 9.4 第 2 轮：状态与生命周期边界
- 9.5 第 3 轮：恢复、重复操作与阈值边界
- 9.6 输出规则

## 9.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`

执行要求：

- 每一轮都要从头全文读取 `working_dir/merged/testcase_basic_final.md` 或上一轮边界 delta，先判断哪些边界已经覆盖，哪些边界还没有。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 9.2 触发条件与数据源

本步骤的主要数据源来自：

- 用户上传文档：从 `working_dir/full_read_manifest.md` 中筛出 `source_type: user_upload`
- Drive 补充文档：从 `working_dir/full_read_manifest.md` 中筛出 `source_type: drive_doc`
- 过往用例：先读 `working_dir/former_case_selection.md`，再回到其中列出的 `../testcase-pattern-learning/former_cases` 文件
- 已读规格章节：从 `working_dir/full_read_manifest.md` 中筛出与限制、范围、阈值相关的 `product_doc`

优先触发本步骤的信号：

- 明确的最小值 / 最大值 / 默认值 / 空值 / 非法值 / 数量上限
- 状态切换、启用 / 禁用、删除 / 恢复、重复执行、阈值跨越

## 9.3 第 1 轮：输入值与范围边界

使用 9.2 的同一批材料，从“输入值、最小值、最大值、空值、非法值、长度 / 数量范围”角度补充边界 delta，输出：

- `working_dir/delta/delta_step9_border_1.md`

## 9.4 第 2 轮：状态与生命周期边界

继续使用 9.2 的同一批材料，并全文读取 `working_dir/delta/delta_step9_border_1.md`，从“状态切换、初始化 / 已配置 / 已启用 / 已删除、前后状态边界”角度补充边界 delta，输出：

- `working_dir/delta/delta_step9_border_2.md`

## 9.5 第 3 轮：恢复、重复操作与阈值边界

继续使用 9.2 的同一批材料，并全文读取 `working_dir/delta/delta_step9_border_2.md`，从“重复执行、接近阈值、刚跨阈值、回退 / 恢复、告警 / 日志 / 任务状态”角度补充边界 delta，输出：

- `working_dir/delta/delta_step9_border_3.md`

## 9.6 输出规则

- 每一轮输出后都先跑 parser；解析失败先修格式，再进入下一轮。
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step9_border_4.md`、`delta_step9_border_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step9_border_*.md` 作为边界专项 delta。

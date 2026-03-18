# Step 11：做压力专项 delta 增强

## 目录

- 11.1 输入与全文读取要求
- 11.2 触发条件与数据源
- 11.3 第 1 轮：容量与稳态压力
- 11.4 第 2 轮：突发、并发与长稳
- 11.5 第 3 轮：资源争用、恢复与观测
- 11.6 输出规则

## 11.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`

执行要求：

- 每一轮都先确认 `working_dir/full_read_manifest.md` 中已读过哪些白皮书、规格和运维文档描述了容量、性能、并发或资源限制。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 11.2 触发条件与数据源

本步骤的数据源来自：

- 用户上传文档：`working_dir/full_read_manifest.md` 中的 `source_type: user_upload`
- Drive 补充文档：`working_dir/full_read_manifest.md` 中的 `source_type: drive_doc`
- 过往用例：`working_dir/former_case_selection.md` 及其对应的 `../testcase-pattern-learning/former_cases`
- 产品白皮书与性能 / 规格章节：`working_dir/full_read_manifest.md` 中已读过的 `source_type: product_doc`

优先触发本步骤的信号：

- 吞吐、容量、并发、批量任务、长时间运行、资源上限

## 11.3 第 1 轮：容量与稳态压力

使用 11.2 的同一批材料，从“容量上限、典型负载、长时间稳态运行”角度补充压力 delta，输出：

- `working_dir/delta/delta_step11_stress_1.md`

## 11.4 第 2 轮：突发、并发与长稳

继续使用 11.2 的同一批材料，并全文读取 `working_dir/delta/delta_step11_stress_1.md`，从“突发流量、并发操作、批量任务、长时间运行期间的状态演化”角度补充压力 delta，输出：

- `working_dir/delta/delta_step11_stress_2.md`

## 11.5 第 3 轮：资源争用、恢复与观测

继续使用 11.2 的同一批材料，并全文读取 `working_dir/delta/delta_step11_stress_2.md`，从“CPU / 内存 / 磁盘 / 网络资源争用、性能退化、恢复、告警、日志和观测”角度补充压力 delta，输出：

- `working_dir/delta/delta_step11_stress_3.md`

## 11.6 输出规则

- 每一轮输出后都先跑 parser；解析失败先修格式，再进入下一轮。
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step11_stress_4.md`、`delta_step11_stress_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step11_stress_*.md` 作为压力专项 delta。

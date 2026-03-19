# Step 12：做用户场景专项 delta 增强

## 目录

- 12.1 输入与全文读取要求
- 12.2 触发条件与数据源
- 12.3 第 1 轮：主角色端到端场景
- 12.4 第 2 轮：跨模块与中断恢复场景
- 12.5 第 3 轮：多角色、误操作与审计场景
- 12.6 输出规则

## 12.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`

执行要求：

- 每一轮都重新确认用户文档和白皮书里描述的业务路径、角色、操作顺序和约束。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 每一轮写 delta 前，先输出 `working_dir/reports/step12_user_scenario_round<round>_evidence.md`，把本轮实际引用的用户路径资料、历史近邻与新增场景依据映射落盘。
- 如果本轮重新打开了具体的历史近邻样本文件，也要把这些 reread 记录追加到 `working_dir/full_read_manifest.md`，`source_type` 写 `former_case`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 12.2 触发条件与数据源

本步骤的数据源来自：

- 用户上传文档：`working_dir/full_read_manifest.md` 中的 `source_type: user_upload`
- Drive 补充文档：`working_dir/full_read_manifest.md` 中的 `source_type: drive_doc`
- 过往用例：`working_dir/former_case_selection.md` 及其对应的 `../testcase-pattern-learning/former_cases`
- 产品白皮书与用户 / 管理流程章节：`working_dir/full_read_manifest.md` 中已读过的 `source_type: product_doc`

优先触发本步骤的信号：

- 多角色协作、主业务链路、跨模块入口、误操作恢复、审计路径

## 12.3 第 1 轮：主角色端到端场景

使用 12.2 的同一批材料，从“主要用户角色、主业务链路、端到端闭环”角度补充用户场景 delta，输出：

- `working_dir/delta/delta_step12_user_scenario_1.md`

## 12.4 第 2 轮：跨模块与中断恢复场景

继续使用 12.2 的同一批材料，并全文读取 `working_dir/delta/delta_step12_user_scenario_1.md`，从“跨模块串联、不同入口切换、中断后继续、依赖前置对象已存在 / 不存在”角度补充用户场景 delta，输出：

- `working_dir/delta/delta_step12_user_scenario_2.md`

## 12.5 第 3 轮：多角色、误操作与审计场景

继续使用 12.2 的同一批材料，并全文读取 `working_dir/delta/delta_step12_user_scenario_2.md`，从“多角色协作、权限变化、误操作、审计 / 日志追踪”角度补充用户场景 delta，输出：

- `working_dir/delta/delta_step12_user_scenario_3.md`

## 12.6 输出规则

- 每一轮输出后都先跑 parser；解析失败先修格式，再进入下一轮。
- parser 通过后，再执行：

```bash
python scripts/validate_specialized_delta_context.py --step 12 --round <round> --manifest <working_dir/full_read_manifest.md 的绝对路径> --former-case-selection <working_dir/former_case_selection.md 的绝对路径> --base-testcase <working_dir/merged/testcase_basic_final.md 的绝对路径> --report <working_dir/reports/step12_user_scenario_round<round>_evidence.md 的绝对路径> --delta <working_dir/delta/delta_step12_user_scenario_<round>.md 的绝对路径> [--previous-delta <上一轮 delta 绝对路径>]
```

- `step12_user_scenario_round<round>_evidence.md` 至少包含以下章节：
  - `## 本轮输入清单`
  - `## 历史近邻继承点`
  - `## 当前缺口判断`
  - `## 新增用例与依据映射`
  - `## 收敛记录`
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step12_user_scenario_4.md`、`delta_step12_user_scenario_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step12_user_scenario_*.md` 作为用户场景专项 delta。

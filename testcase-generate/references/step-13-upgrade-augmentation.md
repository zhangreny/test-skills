# Step 13：做升级专项 delta 增强

## 目录

- 13.1 输入与全文读取要求
- 13.2 触发条件与数据源
- 13.3 第 1 轮：升级前检查与受支持路径
- 13.4 第 2 轮：升级过程中功能连续性
- 13.5 第 3 轮：回退、失败恢复与升级后验证
- 13.6 输出规则

## 13.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`

执行要求：

- 每一轮都重新确认 `working_dir/full_read_manifest.md` 中已读过的升级指南、兼容矩阵、版本限制和白皮书说明。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 每一轮写 delta 前，先输出 `working_dir/reports/step13_upgrade_round<round>_evidence.md`，把本轮实际引用的升级资料、历史近邻与新增场景依据映射落盘。
- 如果本轮重新打开了具体的历史近邻样本文件，也要把这些 reread 记录追加到 `working_dir/full_read_manifest.md`，`source_type` 写 `former_case`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 13.2 触发条件与数据源

本步骤的数据源来自：

- 用户上传文档：`working_dir/full_read_manifest.md` 中的 `source_type: user_upload`
- Drive 补充文档：`working_dir/full_read_manifest.md` 中的 `source_type: drive_doc`
- 过往用例：`working_dir/former_case_selection.md` 及其对应的 `../testcase-pattern-learning/former_cases`
- 产品白皮书、升级指南和兼容章节：`working_dir/full_read_manifest.md` 中已读过的 `source_type: product_doc`

优先触发本步骤的信号：

- 升级路径、版本前提、混合版本窗口、回退、升级后校验

## 13.3 第 1 轮：升级前检查与受支持路径

使用 13.2 的同一批材料，从“支持的升级路径、版本前提、环境检查、前置备份与风险提示”角度补充升级 delta，输出：

- `working_dir/delta/delta_step13_upgrade_1.md`

## 13.4 第 2 轮：升级过程中功能连续性

继续使用 13.2 的同一批材料，并全文读取 `working_dir/delta/delta_step13_upgrade_1.md`，从“升级中服务可用性、任务中断、节点分批升级、混合版本窗口”角度补充升级 delta，输出：

- `working_dir/delta/delta_step13_upgrade_2.md`

## 13.5 第 3 轮：回退、失败恢复与升级后验证

继续使用 13.2 的同一批材料，并全文读取 `working_dir/delta/delta_step13_upgrade_2.md`，从“升级失败、回退、数据一致性、配置兼容性、升级后业务与观测验证”角度补充升级 delta，输出：

- `working_dir/delta/delta_step13_upgrade_3.md`

## 13.6 输出规则

- 每一轮输出后都先跑 parser；解析失败先修格式，再进入下一轮。
- parser 通过后，再执行：

```bash
python scripts/validate_specialized_delta_context.py --step 13 --round <round> --manifest <working_dir/full_read_manifest.md 的绝对路径> --former-case-selection <working_dir/former_case_selection.md 的绝对路径> --base-testcase <working_dir/merged/testcase_basic_final.md 的绝对路径> --report <working_dir/reports/step13_upgrade_round<round>_evidence.md 的绝对路径> --delta <working_dir/delta/delta_step13_upgrade_<round>.md 的绝对路径> [--previous-delta <上一轮 delta 绝对路径>]
```

- `step13_upgrade_round<round>_evidence.md` 至少包含以下章节：
  - `## 本轮输入清单`
  - `## 历史近邻继承点`
  - `## 当前缺口判断`
  - `## 新增用例与依据映射`
  - `## 收敛记录`
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且 mode 允许，继续输出 `delta_step13_upgrade_4.md`、`delta_step13_upgrade_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step13_upgrade_*.md` 作为升级专项 delta。

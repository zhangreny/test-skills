# Step 10：做兼容性专项 delta 增强

## 目录

- 10.1 输入与全文读取要求
- 10.2 触发条件与数据源
- 10.3 第 1 轮：版本、平台与拓扑兼容
- 10.4 第 2 轮：接口、依赖与外围组件兼容
- 10.5 第 3 轮：混合环境与降级兼容
- 10.6 输出规则

## 10.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- `working_dir/full_read_manifest.md`
- `working_dir/former_case_selection.md`

执行要求：

- 每一轮开始前，都重新从 `working_dir/full_read_manifest.md` 中确认已读过的兼容性相关产品文档章节。
- 每一轮都在 `working_dir/full_read_manifest.md` 中追加本轮读取记录，并写明 `round`。
- 每一轮写 delta 前，先输出 `working_dir/reports/step10_compatibility_round<round>_evidence.md`，把本轮实际引用的兼容性资料、历史近邻与新增场景依据映射落盘。
- 如果本轮重新打开了具体的历史近邻样本文件，也要把这些 reread 记录追加到 `working_dir/full_read_manifest.md`，`source_type` 写 `former_case`。
- 默认轮次读取 `working_dir/workflow_state.json` 的 `round_policy.step_9_to_15`。

## 10.2 触发条件与数据源

本步骤的数据源来自：

- 用户上传文档：`working_dir/full_read_manifest.md` 中的 `source_type: user_upload`
- Drive 补充文档：`working_dir/full_read_manifest.md` 中的 `source_type: drive_doc`
- 过往用例：`working_dir/former_case_selection.md` 及其对应的 `../testcase-pattern-learning/former_cases`
- 产品白皮书与兼容 / 规格章节：`working_dir/full_read_manifest.md` 中已读过的 `source_type: product_doc`

优先触发本步骤的信号：

- 版本矩阵、平台差异、硬件 / OS / 浏览器 / 客户端差异
- 外部协议、CLI / API、第三方依赖、混合版本窗口

## 10.3 第 1 轮：版本、平台与拓扑兼容

使用 10.2 的同一批材料，从“版本矩阵、节点角色、部署拓扑、平台 / 硬件 / 操作系统差异”角度补充兼容性 delta，输出：

- `working_dir/delta/delta_step10_compatibility_1.md`

## 10.4 第 2 轮：接口、依赖与外围组件兼容

继续使用 10.2 的同一批材料，并全文读取 `working_dir/delta/delta_step10_compatibility_1.md`，从“协议、API、CLI、浏览器 / 客户端、外部依赖、第三方组件”角度补充兼容性 delta，输出：

- `working_dir/delta/delta_step10_compatibility_2.md`

## 10.5 第 3 轮：混合环境与降级兼容

继续使用 10.2 的同一批材料，并全文读取 `working_dir/delta/delta_step10_compatibility_2.md`，从“混合版本、部分节点差异、功能降级、兼容失败时的告警与回退”角度补充兼容性 delta，输出：

- `working_dir/delta/delta_step10_compatibility_3.md`

## 10.6 输出规则

- 每一轮输出后都先跑 parser；解析失败先修格式，再进入下一轮。
- parser 通过后，再执行：

```bash
python scripts/validate_specialized_delta_context.py --step 10 --round <round> --manifest <working_dir/full_read_manifest.md 的绝对路径> --former-case-selection <working_dir/former_case_selection.md 的绝对路径> --base-testcase <working_dir/merged/testcase_basic_final.md 的绝对路径> --report <working_dir/reports/step10_compatibility_round<round>_evidence.md 的绝对路径> --delta <working_dir/delta/delta_step10_compatibility_<round>.md 的绝对路径> [--previous-delta <上一轮 delta 绝对路径>]
```

- `step10_compatibility_round<round>_evidence.md` 至少包含以下章节：
  - `## 本轮输入清单`
  - `## 历史近邻继承点`
  - `## 当前缺口判断`
  - `## 新增用例与依据映射`
  - `## 收敛记录`
- 每一轮都记录 `new_top_level_scenarios`、`new_leaf_cases`、`deduped_cases`、`continue_or_stop_reason`。
- 符合硬收敛条件时立即停止，不要机械地补空轮次。
- 如果第三轮后仍满足继续条件且未触达 `max_rounds`，继续输出 `delta_step10_compatibility_4.md`、`delta_step10_compatibility_5.md`，直到硬收敛。
- Step 16 默认读取本步骤编号最大的 `delta_step10_compatibility_*.md` 作为兼容性专项 delta。

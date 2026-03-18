# Step 7：做组别 pattern 学习并生成 pattern delta

## 目录

- 7.1 输入与全文读取要求
- 7.2 生成 pattern route tags 与 summary
- 7.3 按产品标签和能力标签读取组别 pattern
- 7.4 生成 `delta/delta_step7_pattern.md`
- 7.5 review 并输出 `delta/delta_step7_pattern_reviewed.md`

## 7.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/baseline/testcase_base_reviewed.md`
- `working_dir/delta/delta_step5_jira_reviewed.md`（如果 Step 5 实际执行）
- `working_dir/delta/delta_step6_former_case_reviewed.md`（如果 Step 6 实际执行）
- `working_dir/former_case_selection.md`
- `working_dir/full_read_manifest.md`
- Step 4 到 Step 6 使用过的正文资料

执行要求：

- 先完整阅读 baseline 和已执行 delta，再读取 `working_dir/former_case_selection.md`，确认历史近邻到底来自哪里。
- 结合 `working_dir/full_read_manifest.md`，确认前序已经读过哪些用户文档、Drive 文档、产品文档和 testcase 文件。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤读取的 testcase、pattern 与其他资料。

## 7.2 生成 pattern route tags 与 summary

先生成：

- `working_dir/reports/pattern_route_summary.md`

至少记录：

- `product_tags`
- `capability_tags`
- `selected_group_patterns`
- `why_selected`
- `why_skipped`

提取标签时，至少综合以下信息：

1. Step 2 的产品信息、`core_keywords`、`expansion_keywords`
2. `working_dir/former_case_selection.md` 中命中的 suite / section / subsection
3. baseline 与已执行 delta 中反复出现的对象、动作、异常和观测手段

标签规则：

- `product_tags` 更偏向产品或系统对象，例如：`elf`、`tower`、`backup`、`sks`、`zbs`、`sre-platform`、`obs`、`inspection-center`、`sfs`、`neutree`
- `capability_tags` 更偏向能力或链路，例如：`virtualization`、`network-security`、`backup-replication`、`kubernetes-platform`、`block-storage`、`observability-ops`、`service-upgrade`

## 7.3 按产品标签和能力标签读取组别 pattern

先读取：

- `../testcase-pattern-learning/tutorial-all-groups/all-groups-common.md`

再根据 `product_tags` 和 `capability_tags`，读取一个或多个匹配的组别 pattern：

- `../testcase-pattern-learning/tutorial-all-groups/*-group.md`

执行要求：

- 不要再用“猜最接近的组”作为默认策略。
- 命中规则：
  - `network-group.md`
    - `capability_tags` 命中 `network-security`
    - 或关键词指向网络、安全、端口控制、连通性、VPC、LB、FIP、SDN、转发、策略
  - `elf-group.md`
    - `product_tags` 命中 `elf` 或 `tower`
    - 或 `capability_tags` 命中 `virtualization`
    - 或关键词指向虚拟机生命周期、迁移、v2v、VMTools、Guest 网络配置
  - `backup-group.md`
    - `product_tags` 命中 `backup`
    - 或 `capability_tags` 命中 `backup-replication`
    - 或关键词指向备份、复制、恢复点、备份计划、备份存储库、故障转移
  - `sks-group.md`
    - `product_tags` 命中 `sks`
    - 或 `capability_tags` 命中 `kubernetes-platform`
    - 或关键词指向 Kubernetes 集群、节点组、CNI、CSI、GPU、系统服务、工作负载集群
  - `zbs-group.md`
    - `product_tags` 命中 `zbs`
    - 或 `capability_tags` 命中 `block-storage`
    - 或关键词指向 ZBS、LUN、CSI、PV、PVC、storageClass、快照、克隆、加密、副本数
  - `sre-group.md`
    - `product_tags` 命中 `sre-platform`、`obs`、`inspection-center`、`sfs`、`neutree`
    - 或 `capability_tags` 命中 `observability-ops`、`service-upgrade`
    - 或关键词指向告警、静默、巡检、报表、系统服务、任务 / 事件、服务升级、管理 VIP、DRS、平台运维
- 多组并存时，不要强行只选一组；按实际命中读取多组：
  - Backup on ZBS：读 `backup-group.md` + `zbs-group.md`
  - SKS CSI on ZBS：读 `sks-group.md` + `zbs-group.md`
  - SKS 可观测性联动：读 `sks-group.md` + `sre-group.md`
  - ELF + ZBS 联动：读 `elf-group.md` + `zbs-group.md`
- 如果只有通用特征，没有任何组别标签命中：
  - 只读 `all-groups-common.md`
  - 在 `pattern_route_summary.md` 里明确写清“未命中特定组 pattern”，不要猜一个最近的组。
- 在 `working_dir/full_read_manifest.md` 中把 pattern 文档记录为 `source_type: pattern`。

## 7.4 生成 `delta/delta_step7_pattern.md`

在 baseline 与前序 delta 基础上，结合组别 pattern，只输出 pattern 带来的净新增 delta：

- `working_dir/delta/delta_step7_pattern.md`

生成要求：

- 不要复制整份 baseline 或前序 delta。
- 只补 pattern 明确提示的粒度、场景矩阵、工具、观测手段、关联产品和命名习惯，不要提前把边界 / 兼容 / 压力 / 升级 / 扩缩容 / 故障专项一股脑全塞进来。
- 如果 pattern 明确提示当前用例粒度过粗，先拆细基础功能路径。
- 此文件是 pattern delta，不是 final。

## 7.5 review 并输出 `delta/delta_step7_pattern_reviewed.md`

对 `working_dir/delta/delta_step7_pattern.md` 做一次 review，再输出：

- `working_dir/delta/delta_step7_pattern_reviewed.md`

在进入 Step 8 前，先用以下脚本做结构校验；解析失败时先修格式：

```bash
python scripts/validate_testrail_case.py --source <working_dir/delta/delta_step7_pattern.md 的绝对路径>
```

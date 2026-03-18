# Step 6：补充本地历史近邻 delta，并按置信度决定是否让用户确认

## 目录

- 6.1 输入与全文读取要求
- 6.2 生成历史样本入口路由 summary
- 6.3 强制读取本地历史 testcase 样本
- 6.3a 记录命中的近邻样本清单
- 6.3 总结当前已有测试角度并识别缺口
- 6.4 置信度分流：高置信度直接继续，低置信度再向用户确认
- 6.5 输出历史近邻 delta `delta/delta_step6_former_case.md`
- 6.6 review 历史近邻 delta 并输出 `delta/delta_step6_former_case_reviewed.md`

## 6.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/baseline/testcase_base_reviewed.md`
- `working_dir/delta/delta_step5_jira_reviewed.md`（如果 Step 5 实际执行）
- Step 2 的功能摘要、产品信息、`core_keywords`、`expansion_keywords`
- Step 4 与 Step 5 使用过的正文资料

执行要求：

- 先完整阅读 baseline 和已执行的 Jira delta，总结当前已经覆盖的对象、子模块、测试角度、异常类型和观测手段。
- 不要跳过已有 testcase 的正文细节，否则会误判历史近邻缺口。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤全文读取的资料和 testcase 文件。

## 6.2 生成历史样本入口路由 summary

先生成：

- `working_dir/reports/former_case_route_summary.md`

至少记录：

- `product_tags`
- `capability_tags`
- `selected_former_case_roots`
- `priority_suites_or_files`
- `why_selected`
- `why_skipped`

路由规则：

- `network` / `network-security`
  - 根目录：`../testcase-pattern-learning/former_cases/15_SDN`
  - 优先 suite：分布式防火墙、VPC、负载均衡、Everoute、许可拆分等网络相关 suite
- `elf` / `tower` / `virtualization`
  - 根目录：`../testcase-pattern-learning/former_cases/1_SmartX`
  - 优先文件：`121_Master.md`
  - 如涉及 ZBS 联动，再补 `300_SMTX ZBS.md`
- `backup` / `backup-replication`
  - 根目录：`../testcase-pattern-learning/former_cases/6_Backup`
  - 优先文件：`271_Master.md`
- `sks` / `kubernetes-platform`
  - 根目录：`../testcase-pattern-learning/former_cases/8_SKS`
  - 优先文件：`442_Master.md`
- `zbs` / `block-storage`
  - 根目录：`../testcase-pattern-learning/former_cases/18_ZBS CSI`
  - 优先文件：`1312_Master.md`
  - 如涉及管理面 / 跨产品联动，再补 `../testcase-pattern-learning/former_cases/1_SmartX/300_SMTX ZBS.md`
- `sre-platform` / `observability-ops` / `service-upgrade`
  - 根目录按主题选择：
    - 可观测与告警：`../testcase-pattern-learning/former_cases/10_可观测平台`
    - 巡检服务：`../testcase-pattern-learning/former_cases/16_巡检中心`
    - 文件存储平台运维：`../testcase-pattern-learning/former_cases/17_SFS`
    - 控制面 + 监控组件部署：`../testcase-pattern-learning/former_cases/22_Neutree`

要求：

- 不要默认从整个 `former_cases/` 根目录无差别扫描。
- 如果命中了多个组，就按组分别收紧到对应根目录，再在每个根目录内部挑近邻样本。
- 如果没有命中任何明确组别，再退回 `../testcase-pattern-learning/former_cases` 做有限检索，并在 route summary 里说明为什么无法先缩窄入口。

## 6.3 强制读取本地历史 testcase 样本

本步骤只使用本地历史 testcase 样本，不读取实时 TestRail，不调用远端导出。

读取入口：

- `working_dir/reports/former_case_route_summary.md` 中选中的根目录和优先文件

执行规则：

- 围绕 Step 2 的主体产品、对象、动作、症状、版本词、子模块名去检索本地历史样本。
- 优先在 route summary 已选中的根目录里检索，不要先跨组扫描。
- 优先找同组、同对象、同动作、同异常模式、同 subsection 结构的历史用例。
- 先看 suite / section / subsection 结构，再读代表性 case 正文。
- 不要只看历史标题；对被选中的近邻 subsection / case，要读到足以判断其场景矩阵、粒度和缺口。
- 只从本地历史样本中取近邻，不要引入在线 TestRail 数据。
- 在 `working_dir/full_read_manifest.md` 中把本步骤实际读过的历史样本记录为 `source_type: former_case`。

## 6.3a 记录命中的近邻样本清单

把本步骤最终命中的近邻样本整理为：

- `working_dir/former_case_selection.md`

至少记录：

- `suite`
- `section`
- `subsection`
- `path`
- `root_selected_from`
- `why_matched`
- `what_to_learn`

要求：

- 只记录真正读过并判定为“近邻”的样本，不要把只扫过标题的文件写进去。
- 后续 Step 7 到 Step 15 都把这个文件当作历史近邻入口，不要每一步重新从零回忆样本来源。

## 6.3 总结当前已有测试角度并识别缺口

结合 baseline、已执行 delta 与本地历史近邻样本，总结：

1. 当前已覆盖的测试角度
2. 历史近邻经常出现、但当前尚未覆盖的特殊场景
3. 当前 feature 与历史 subsection 相比缺少哪些场景或用例

优先检查的特殊场景包括但不限于：

- 升级
- 扩缩容
- 故障
- 稳定性
- 恢复 / 回退 / 清理
- 兼容性
- 工具 / 观测路径
- 生命周期闭环

## 6.4 置信度分流：高置信度直接继续，低置信度再向用户确认

先输出：

- `working_dir/reports/former_case_gap_summary.md`

摘要里至少包含：

1. 当前已覆盖的测试角度摘要
2. 命中的本地历史近邻 suite / section / subsection，以及 `working_dir/former_case_selection.md`
3. 历史样本入口路由结果，以及 `working_dir/reports/former_case_route_summary.md`
4. 近邻样本提示的缺口场景
5. 建议新增的用例类别
6. 本轮置信度判断：`high` 或 `needs_confirmation`

要求：

- 满足以下条件时，可判定为 `high` 并继续：
  - 近邻样本集中在同一产品线、同一对象链或同一子模块。
  - 建议新增的场景能清晰映射到当前 baseline 缺口。
  - 没有多个相互矛盾的历史写法需要用户拍板。
- 出现以下情况时，改为 `needs_confirmation` 并暂停：
  - 近邻样本来自多个相差较大的 suite / section。
  - 历史样本提示的扩展方向可能超出当前 feature 边界。
  - 需要用户选择“要不要继承某一类高成本专项场景”。

## 6.5 输出历史近邻 delta `delta/delta_step6_former_case.md`

以当前 baseline 和已执行 delta 为参考，补写历史近邻提示的缺口，输出：

- `working_dir/delta/delta_step6_former_case.md`

delta 要求：

- 不要复制整份 baseline 或 Jira delta。
- 只补当前文件尚缺、但本地历史近邻稳定出现的场景、矩阵或成对路径。
- 不要直接照抄历史业务文本；只继承粒度、场景、工具、矩阵和命名习惯。
- 如果一个新增场景能拆成多条 case，直接拆开，不要压成一条大 case。

## 6.6 review 历史近邻 delta 并输出 `delta/delta_step6_former_case_reviewed.md`

对 `working_dir/delta/delta_step6_former_case.md` 做一次 review，再输出：

- `working_dir/delta/delta_step6_former_case_reviewed.md`

在 review 开始前，先用以下脚本做格式测试：

```bash
python scripts/validate_testrail_case.py --source <working_dir/delta/delta_step6_former_case.md 的绝对路径>
```

规则：

- `--source` 必须传 testcase 文件的绝对路径。
- 如果脚本解析失败、提示结构不合法或怀疑乱码，先修 testcase 格式或编码，再继续后续 review。

review 必查项：

1. 新增内容是否与命中的本地历史近邻场景一致
2. 能拆成多条用例的地方是否都已拆开
3. 是否仍存在“把多条用例藏在一条 case 的步骤里”的情况
4. 是否只保留了历史近邻带来的净新增项，而不是重复 baseline / Jira delta
5. 是否符合 `references/testrail_default.md` 的模板结构，并能被 parser 成功解析

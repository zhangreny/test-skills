# 质量检查

最终输出前逐项确认：

- 已实际读取相关补充文档，而不只是看文件名。
- 已先完成“原始需求分析 + 用户确认”，再去搜 Drive 和 Jira。
- 已输出分析结果，并分别完成“需求分析确认”“Jira 摘要确认”“测试对象 + 工具矩阵 + 测试角度 + 历史矩阵补全结果 + coverage_expansion_plan 确认”。
- 最终 case 与需求主线一致，没有被模板示例内容带偏。
- 最终 case 兼顾主流程、异常、边界、运维联动、工具 / 观测手段、升级兼容和历史回归风险。
- 已先生成原子级 `case_seeds`，再通过补缺循环扩展到最终 testcase，而不是直接从测试角度生成大纲式终稿。
- 已执行有上限的补缺循环，并明确记录每轮 gap report 与停止条件。
- 已显式完成“原子性检查”：确认每条 case 只验证一个核心结果，且都具备对象、条件、动作、预期结果、观测方式。
- 已显式完成“覆盖密度检查”：确认没有因为“已经有原子 case”就提前停止，且对象差异、条件差异、输入差异、状态差异、结果差异、观测差异、生命周期差异等高风险拆分轴都已按需展开成独立 case。
- 如 reviewer 发现任何 case 仍停留在主题大纲层或混合多个核心结果，已回到 seeds 阶段重拆并重新渲染。
- 如 reviewer 发现任何 case 虽然原子但仍合并多个高风险差异轴，已回到 seeds 阶段继续拆细并重新渲染。
- 已在最终输出前完成 reviewer 专家复核，并已将 review 结论实际落实到 `working_dir/testcase_final.md`。
- 已完成“双源历史学习”：本地样本源 + 实时 / 近期 TestRail 源；如果其中一侧受阻，已明确说明影响。
- 已将 `coverage_expansion_plan` 中的 `must_pair_paths`、`tool_required_paths`、`must_expand_dimensions` 实际落实到最终 case 或明确标注残余风险。
- 已将 `coverage_expansion_plan` 中的 `must_split_axes` 与 `case_granularity_strategy` 实际落实到最终 case，而不是停留在分析阶段。
- 已对验收、功能、边界、可靠性、用户场景、压力、规格、兼容性、扩缩容、升级这 10 类测试维度完成覆盖判断，并落实到 `test_dimension_coverage`、最终 case 或明确说明不适用原因。
- 已检查并修正与 `references/testrail_default.md` 的格式差异，确保编号层级、名称、描述、`【Step1】`、`【Step2】`、`【Step3】` 均完整。
- 最终输出给用户的是 review 后的终稿，而不是 draft 或未修订版本。
- 标题和粒度符合 TestRail 风格，单条 case 不臃肿。

# 通用测试设计维度

在 Step 5 做测试设计收敛时，把以下维度作为显式输入，而不是靠生成 testcase 时临时脑补。

## 维度清单

1. 验收测试
   - 包括前端、后端和端到端集成验收
2. 功能测试
3. 边界测试
4. 可靠性测试
   - 包括故障测试、稳定性测试
5. 用户场景测试
   - 包括端到端应用场景测试
6. 压力测试
7. 规格测试
8. 兼容性测试
9. 集群扩缩容场景对功能进行验证
10. 集群升级场景对功能进行验证

## 使用规则

- 不要默认这 10 类都必须展开成同等数量的 testcase；先判断是否适用，再决定覆盖方式。
- 对每一类维度都必须给出以下三种判定之一：
  - `must_cover`：当前 feature 必须显式覆盖，且要在 `coverage_expansion_plan` 和最终 case 中找到落点
  - `sample_cover`：当前 feature 需要覆盖，但允许抽样，不要求把该维度下所有变体都展开
  - `not_applicable`：当前 feature 不适用，但必须写明理由
- 如果一个维度被标记为 `not_applicable`，理由必须基于当前需求、产品边界、交付目标或环境限制，不能只写“暂不考虑”。
- 如果一个维度被标记为 `sample_cover`，必须写明抽样依据，例如风险较低、已有历史覆盖、当前版本改动面有限、仅影响单一对象等。
- 如果当前需求明确涉及扩缩容、升级、兼容、性能、故障恢复、前后端联动，就不能把对应维度标记为 `not_applicable`。

## 与 Step 5 的衔接要求

- 在完成业务分析后，先用这 10 类维度检查当前 feature 的覆盖范围，再进入测试对象核对和工具矩阵设计。
- 对每个维度至少补充以下信息：
  - `dimension`
  - `decision`
  - `why`
  - `mapped_objects`
  - `mapped_test_angles`
  - `mapped_case_groups`
- 如果某个维度需要特殊环境或特殊前置条件，例如压测环境、升级路径、扩缩容资源池、兼容性矩阵，要在 Step 5 明确记录依赖，不要到 Step 6 才暴露。

## 与 `coverage_expansion_plan` 的衔接要求

在 `coverage_expansion_plan` 中额外增加：

- `test_dimension_coverage`
  - 按上述 10 类维度逐项记录 `must_cover` / `sample_cover` / `not_applicable`
  - 记录每类维度映射到的测试角度、case 分组或残余风险

如果某类维度被判定为 `must_cover`，但在后续 seeds 或最终 testcase 中没有对应落点，必须视为缺口，不能继续推进终稿。

## 建议判断口径

- 验收测试：当 feature 涉及多层联动、前后端协同、完整交付闭环时，通常至少 `sample_cover`，高风险时 `must_cover`
- 功能测试：通常为 `must_cover`
- 边界测试：只要存在参数、状态、对象差异、条件差异，通常至少 `sample_cover`
- 可靠性测试：当 feature 涉及异步任务、状态恢复、依赖链路、服务异常、重试回滚时，通常至少 `sample_cover`
- 用户场景测试：当 feature 面向真实业务路径或运维路径交付时，通常至少 `sample_cover`
- 压力测试：只有在需求、历史问题、性能风险或交付目标明确涉及容量、吞吐、并发、时延时，才提升为 `must_cover` 或 `sample_cover`
- 规格测试：当需求存在明确规格、限制、配额、数量上限、行为契约时，通常至少 `sample_cover`
- 兼容性测试：当 feature 涉及版本、平台、架构、部署形态、外部依赖差异时，通常至少 `sample_cover`
- 集群扩缩容验证：当 feature 与集群资源、节点数量、调度、部署拓扑或集群生命周期有关时，通常至少 `sample_cover`
- 集群升级验证：当 feature 有版本继承、升级前后行为一致性、配置保留、状态迁移要求时，通常至少 `sample_cover`

# Step 7：通用测试维度缺口分析

在进入最终 pattern 学习前，先围绕通用测试维度检查 `working_dir/testcase_addformercase_reviewed.md` 还缺什么。

## 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/testcase_addformercase_reviewed.md`
- Step 4 到 Step 6 使用过的正文资料

执行要求：

- 先完整阅读当前 reviewed testcase，再判断通用测试维度是否已经覆盖。
- 不要只凭模块标题猜测“应该已经覆盖”。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤全文读取的资料和 testcase 文件。

## 维度清单

1. 验收测试
   - 包括前端和后端，端到端集成
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

## 输出要求

输出：

- `working_dir/test_dimension_gap_analysis.md`

对每个维度至少记录：

- `dimension`
- `why_relevant`
- `already_covered_cases`
- `missing_scenarios`
- `suggested_additions`
- `not_applicable_reason`

规则：

- 如果当前 feature 明确涉及某个维度，不要把它轻易写成 `not_applicable`。
- 如果当前 testcase 已覆盖该维度，也要指出具体落在哪些 case，而不是只写“已覆盖”。
- 如果当前维度仍有明显缺口，要写清楚缺的是什么场景、为什么缺、后续准备在哪里补。
- Step 8 必须全文读取 `working_dir/test_dimension_gap_analysis.md`，不能只看结论摘要。

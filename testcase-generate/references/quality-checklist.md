# 质量检查

最终输出前逐项确认：

- 已完成 Step 0-2，并先做“原始需求分析 + 用户确认”。
- 已在 Step 3 确认并准备相关 Drive 补充文档。
- 从 Step 4 开始，已维护 `working_dir/full_read_manifest.md`，并记录每一步全文读取的资料、按需读取的产品文档章节与 testcase 文件。
- Step 4 已全文读取原始需求文档与 Drive 补充文档。
- Step 4 已按需读取 `smartx-docs-download/markdown_docs` 中直接相关的产品手册 / 管理指南 / 用户指南 / 技术白皮书 / 相关规格文档，且读取范围足以支撑当前 feature 理解。
- Step 4 已直接生成 `testcase_1_direct.md`，没有使用 seeds、seed plan 或 gap loop。
- Step 4 review 前已使用 `../testrail-testcase-extract-upload/scripts/parse_testrail_template.py` 对 `testcase_1_direct.md` 做格式测试；若解析失败，已先修格式再继续 review。
- Step 4 review 已检查文档场景覆盖、可拆场景拆分、“步骤里藏用例”问题与模板格式，并输出 `testcase_1_direct_reviewed.md`。
- Step 5 已全文读取 `testcase_1_direct_reviewed.md` 和前序正文资料，没有退化成只看摘要或关键词。
- Step 5 已显式向用户确认相关 Jira，再追加 Jira 补充用例；每条 Jira 派生 case 都带有 Jira 号。
- Step 5 review 前已使用 `../testrail-testcase-extract-upload/scripts/parse_testrail_template.py` 对 `testcase_jira.md` 做格式测试；若解析失败，已先修格式再继续 review。
- Step 5 review 已检查 Jira 内容对齐、可拆场景拆分、“步骤里藏用例”问题与模板格式，并输出 `testcase_jira_reviewed.md`。
- Step 6 只读取了本地历史 testcase 样本 `../testcase-pattern-learning/former_cases`，没有混入实时 TestRail 数据。
- Step 6 已全文读取 `testcase_jira_reviewed.md`，并显式向用户确认历史近邻缺口，再补写 `testcase_addformercase.md`。
- Step 6 review 前已使用 `../testrail-testcase-extract-upload/scripts/parse_testrail_template.py` 对 `testcase_addformercase.md` 做格式测试；若解析失败，已先修格式再继续 review。
- Step 6 review 已检查历史近邻内容对齐、可拆场景拆分、“步骤里藏用例”问题与模板格式，并输出 `testcase_addformercase_reviewed.md`。
- Step 7 已全文读取 `testcase_addformercase_reviewed.md`，并输出 `test_dimension_gap_analysis.md`，覆盖验收、功能、边界、可靠性、用户场景、压力、规格、兼容性、扩缩容、升级这 10 类维度。
- Step 8 已全文读取 `testcase_addformercase_reviewed.md` 与 `test_dimension_gap_analysis.md`。
- Step 8 已读取 `../testcase-pattern-learning/tutorial-all-groups/all-groups-common.md` 与对应组别的 `*-group.md`，并将 pattern 中提示的缺口落实到最终用例。
- Step 8 review 前已使用 `../testrail-testcase-extract-upload/scripts/parse_testrail_template.py` 对 `testcase_final.md` 做格式测试；若解析失败，已先修格式再继续最终 review。
- 所有下游 testcase 文件都保留了前一步的全部有效内容，没有出现“后面步骤内容比前面更少”的情况。
- 每次 review 都检查了“文档 / Jira / 历史近邻 / pattern 暴露出的场景是否全部落点”。
- 每次 review 都检查了“能拆成多条的 case 是否已经拆开”。
- 每次 review 都检查了“`【Step1】`、`【Step2】`、`【Step3】` 里是否藏了多条本应独立的用例”。
- 最终输出前，已检查并修正与 `references/testrail_default.md` 的格式差异，确保编号层级、名称、描述、`【Step1】`、`【Step2】`、`【Step3】` 均完整，并且 parser 可成功解析。
- 最终输出给用户的是 review 后的 `working_dir/testcase_final_reviewed.md` 正文，而不是 draft 或未修订版本。

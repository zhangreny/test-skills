# Step 6：补充本地历史近邻用例并让用户确认

## 目录

- 6.1 输入与全文读取要求
- 6.2 强制读取本地历史 testcase 样本
- 6.3 总结当前已有测试角度并识别缺口
- 6.4 向用户确认近邻缺口
- 6.5 追加历史近邻补充用例并输出 `testcase_addformercase.md`
- 6.6 review 历史近邻增补版并输出 `testcase_addformercase_reviewed.md`

## 6.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/testcase_jira_reviewed.md`
- Step 2 的功能摘要、产品信息、`core_keywords`、`expansion_keywords`
- Step 4 与 Step 5 使用过的正文资料

执行要求：

- 先完整阅读 `working_dir/testcase_jira_reviewed.md`，总结当前已经覆盖的对象、子模块、测试角度、异常类型和观测手段。
- 不要跳过已有 testcase 的正文细节，否则会误判历史近邻缺口。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤全文读取的资料和 testcase 文件。

## 6.2 强制读取本地历史 testcase 样本

本步骤只使用本地历史 testcase 样本，不读取实时 TestRail，不调用远端导出。

读取入口：

- `../testcase-pattern-learning/former_cases`

执行规则：

- 围绕 Step 2 的主体产品、对象、动作、症状、版本词、子模块名去检索本地历史样本。
- 优先找同组、同对象、同动作、同异常模式、同 subsection 结构的历史用例。
- 先看 suite / section / subsection 结构，再读代表性 case 正文。
- 不要只看历史标题；对被选中的近邻 subsection / case，要读到足以判断其场景矩阵、粒度和缺口。
- 只从本地历史样本中取近邻，不要引入在线 TestRail 数据。

## 6.3 总结当前已有测试角度并识别缺口

结合 `working_dir/testcase_jira_reviewed.md` 与本地历史近邻样本，总结：

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

## 6.4 向用户确认近邻缺口

在继续之前，必须向用户展示并确认：

1. 当前已覆盖的测试角度摘要
2. 命中的本地历史近邻 suite / section / subsection
3. 近邻样本提示的缺口场景
4. 建议新增的用例类别

要求：

- 必须等待用户确认或修正
- 未经用户确认，不要补写历史近邻增补用例

## 6.5 追加历史近邻补充用例并输出 `testcase_addformercase.md`

以 `working_dir/testcase_jira_reviewed.md` 为基础，补写历史近邻提示的缺口，输出：

- `working_dir/testcase_addformercase.md`

追加要求：

- 保留 `testcase_jira_reviewed.md` 的全部有效内容
- 只补当前文件尚缺、但本地历史近邻稳定出现的场景、矩阵或成对路径
- 不要直接照抄历史业务文本；只继承粒度、场景、工具、矩阵和命名习惯
- 如果一个新增场景能拆成多条 case，直接拆开，不要压成一条大 case

## 6.6 review 历史近邻增补版并输出 `testcase_addformercase_reviewed.md`

对 `working_dir/testcase_addformercase.md` 做一次 review，再输出：

- `working_dir/testcase_addformercase_reviewed.md`

在 review 开始前，先用以下脚本做格式测试：

```bash
python ../testrail-testcase-extract-upload/scripts/parse_testrail_template.py --source <working_dir/testcase_addformercase.md 的绝对路径> --pretty
```

规则：

- `--source` 必须传 testcase 文件的绝对路径。
- 如果脚本解析失败、提示结构不合法或怀疑乱码，先修 testcase 格式或编码，再继续后续 review。

review 必查项：

1. 新增内容是否与命中的本地历史近邻场景一致
2. 能拆成多条用例的地方是否都已拆开
3. 是否仍存在“把多条用例藏在一条 case 的步骤里”的情况
4. 是否保留了 `testcase_jira_reviewed.md` 的全部有效内容
5. 是否符合 `references/testrail_default.md` 的模板结构，并能被 `parse_testrail_template.py` 成功解析

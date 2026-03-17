# Step 8：做组别 pattern 学习并输出终稿

## 目录

- 8.1 输入与全文读取要求
- 8.2 强制读取组别 pattern
- 8.3 生成 `testcase_final.md`
- 8.4 review 终稿并输出 `testcase_final_reviewed.md`

## 8.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/testcase_addformercase_reviewed.md`
- `working_dir/test_dimension_gap_analysis.md`
- Step 4 到 Step 7 使用过的正文资料

执行要求：

- 先完整阅读当前 reviewed testcase 和通用测试维度缺口分析，再做 pattern 学习。
- 不要只拿 pattern 去“套模板”，必须先理解当前已有内容缺在哪里。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤全文读取的资料和 testcase 文件。

## 8.2 强制读取组别 pattern

先读取：

- `../testcase-pattern-learning/tutorial-all-groups/all-groups-common.md`

再根据 feature 所属组别，读取对应的组别 pattern：

- `../testcase-pattern-learning/tutorial-all-groups/*-group.md`

执行要求：

- 如果 feature 属于网络 / 安全 / 连通性 / 端口控制类，优先读取 `network-group.md`
- 如果 feature 属于 ELF 虚拟化、虚拟机生命周期、迁移、Guest 工具、ZBS 联动或 Tower / 管理面联动类，优先读取 `elf-group.md`
- 如果组别判断仍不明确，明确说明当前不确定点，再选择最接近的组别 pattern
- 从 pattern 中重点学习：
  - 粒度
  - 范围边界
  - 场景矩阵
  - 工具 / 观测手段
  - 关联产品
  - 命名习惯

## 8.3 生成 `testcase_final.md`

在 `working_dir/testcase_addformercase_reviewed.md` 基础上，结合组别 pattern 与 Step 7 的通用测试维度缺口分析，补齐仍缺的场景，输出：

- `working_dir/testcase_final.md`

生成要求：

- 保留 `testcase_addformercase_reviewed.md` 的全部有效内容
- 只补 pattern 和通用维度明确提示仍缺的场景，不要无依据地扩散范围
- 如果 pattern 提示当前用例粒度过粗，继续拆细
- 如果 pattern 提示缺少矩阵、工具、关联产品、升级 / 扩缩容 / 故障 / 恢复等高频场景，显式补写
- 不要直接照抄 pattern 文档内容；只继承结构化经验

## 8.4 review 终稿并输出 `testcase_final_reviewed.md`

对 `working_dir/testcase_final.md` 做最终 review，再输出：

- `working_dir/testcase_final_reviewed.md`

review 必查项：

1. 是否保留了 `testcase_addformercase_reviewed.md` 的全部有效内容
2. 是否补齐了 Step 7 与组别 pattern 暴露出的缺口
3. 是否仍存在能拆却未拆的 case
4. 是否仍存在“在步骤里藏多条用例”的情况
5. 是否符合 `references/testrail_default.md` 的模板结构

最终返回给用户的必须是 review 后的 `working_dir/testcase_final_reviewed.md` 正文。

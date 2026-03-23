# Step 16：结构化合并基础稿与各专项 delta

## 目录

- 16.1 输入与全文读取要求
- 16.2 合并规则
- 16.3 输出 `merged/testcase_final.md`

## 16.1 输入与全文读取要求

本步骤至少全文读取以下内容：

- `working_dir/merged/testcase_basic_final.md`
- Step 9 到 Step 15 实际执行步骤中，编号最大的 delta 文件
- `working_dir/full_read_manifest.md`

执行要求：

- 逐份全文读取各专项 delta 文件，不要只凭文件名猜测“这个专项应该补了什么”。
- 在 `working_dir/full_read_manifest.md` 中追加记录本步骤读取的 testcase 文件。
- 如果某个专项没有执行，明确说明跳过原因；不要在 merge 阶段假装它已经覆盖。

## 16.2 合并规则

使用 merge 脚本做结构化拼装：

```bash
python scripts/merge_testcase_variants.py --base <working_dir/merged/testcase_basic_final.md 的绝对路径> --delta <已执行专项 delta 文件的绝对路径> --output <working_dir/merged/testcase_final.md 的绝对路径> --map-output <working_dir/reports/final_merge_map.md 的绝对路径>
```

合并要求：

- 保留 `testcase_basic_final.md` 的全部有效内容。
- 把各专项新增的 case、矩阵和观测路径合并进来，但不要因为“标题相似”就粗暴去重。
- merge 脚本只做“完全相同 case”的精确去重；如果两个来源标题相似但描述、前置、步骤或预期不同，默认保留为独立 case。
- `working_dir/reports/final_merge_map.md` 必须记录：`source_file`、`source_path`、`merged_section`、`kept_as_is`、`deduplicated_with`、`split_further_reason`、`action`。

## 16.3 输出 `merged/testcase_final.md`

输出：

- `working_dir/merged/testcase_final.md`

要求：

- 这是合并后的未 review 终稿。
- 输出后先跑一次 parser；解析失败先修格式，再进入 Step 17。
- 如果 merge 脚本保留了明显重复但不完全相同的 case，把这些问题留给 Step 17 去收敛，不要在 Step 16 静默丢内容。

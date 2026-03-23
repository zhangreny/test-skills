# Step 4：初始化 working_dir、强制全文读取资料并生成 baseline

## 目录

- 4.1 初始化 `working_dir`
- 4.2 强制全文读取用户输入与 Drive 补充资料
- 4.3 强制按需读取 SmartX 产品手册与白皮书
- 4.4 直接生成 baseline `baseline/testcase_base.md`
- 4.5 review baseline 并输出 `baseline/testcase_base_reviewed.md`

## 4.1 初始化 `working_dir`

进入 Step 4 前，先初始化统一工作目录。默认复用 Step 0 已创建的 intake working_dir：

```bash
python scripts/init_working_dir.py --existing-workdir <Step 0 创建的 working_dir 绝对路径>
```

初始化后，后续步骤统一使用：

- `working_dir/input-manifest.json`
- `working_dir/baseline`
- `working_dir/delta`
- `working_dir/merged`
- `working_dir/reports`
- `working_dir/full_read_manifest.md`
- `working_dir/workflow_state.json`

要求：

- 优先复用 Step 0 创建的 working_dir，不要再新开第二个并行产物目录。
- 如果确实没有可复用的 intake working_dir，才改用 `--output-dir` 或让脚本自行新建。
- 如果既没传 `--existing-workdir` 也没传 `--output-dir`，脚本默认把 `working_dir` 创建在系统 `Downloads` 下。
- 不要把默认工作目录放到 `/tmp`、系统临时目录或其他容易被系统清理的位置。
- 所有 baseline、delta、merged 和 report 文件都放在这个 `working_dir` 下。
- 不要删除 Step 0 留下的 `input-manifest.json`。
- 后续多轮步骤的默认轮次和最大轮次，以 `working_dir/workflow_state.json` 为准。

## 4.2 强制全文读取用户输入与 Drive 补充资料

本步骤至少完整读取以下输入：

- 用户原始需求文档
- 如果 Step 3 用户选择补充，则再读取下载到本地的相关 Drive 补充文档

执行要求：

- 不要只看文件名、标题或首段摘要。
- 不要只抽取关键词后停止。
- 对 `.md` 直接全文读取。
- 对 `.pdf`、`.docx` 使用当前环境可行的本地方式抽取全文，并确保全文被读完。
- 如果某份关键文件体积较大，按分段方式继续读到全文结束。
- 在 `working_dir/full_read_manifest.md` 中记录每份已全文读取的文件。

优先使用：

```bash
python scripts/append_full_read_manifest.py --manifest <working_dir/full_read_manifest.md 的绝对路径> --step 4 --round base --source-type <user_upload|drive_doc> --path <绝对路径> --scope fulltext --why-read "Step 4 baseline generation"
```

如果 Step 3 用户明确表示不补充 Drive 文档，不要因为缺少 `drive_doc` 就阻塞 Step 4。

## 4.3 强制按需读取 SmartX 产品手册与白皮书

围绕 Step 2 已确认的主体产品与功能，先在 `../smartx-docs-download/markdown_docs` 中定位产品文档，再强制读取与当前 feature 直接相关的文档内容。

最低要求：

- 必须读取直接相关的产品手册类文档：
  - 管理指南
  - 用户指南
  - 特性说明
- 必须读取直接相关的技术白皮书类文档

按需追加读取：

- 升级指南
- 兼容性指南
- 配置和管理规格
- 安装与运维指南
- 故障场景说明 / 故障处理指南

规则：

- 不要只读命中的关键词所在段落。
- 不要用“手册里已有关键词命中”替代产品理解。
- 对产品文档采用“按需但充分”的读取方式，至少覆盖：
  - 当前 feature 所属模块或对象定义
  - 主流程与关键操作路径
  - 关键限制、前置条件、规格约束
  - 与当前 feature 直接相关的异常、恢复、兼容、升级、运维或故障章节
- 在 `working_dir/full_read_manifest.md` 中记录每份产品文档读了哪些章节，以及为什么这些内容足以支撑当前 feature 理解。

## 4.4 直接生成 baseline `baseline/testcase_base.md`

在完成“用户与 Drive 文档全文读取”以及“产品文档按需充分读取”后，直接按 `references/testrail_default.md` 的结构生成首版 testcase 正文，不使用 seed 理论。

输出文件：

- `working_dir/baseline/testcase_base.md`

生成要求：

- 直接基于全文材料生成 testcase 正文。
- 默认倾向“尽可能多、尽可能细、尽可能展开条数”。
- 目录层级不要被固定成三层；按 feature 复杂度允许使用 `##` 到 `######`。
- 对对象差异、前置条件差异、边界值差异、状态切换差异、异常类型差异、恢复或回退差异、入口差异、结果信号差异、观测方式差异、生命周期阶段差异，优先拆成独立 case。
- 每条 case 的步骤数按执行闭环需要使用 `【Step1】` 到 `【StepN】`。
- 不要把多个可独立验证的结果藏在一条 case 的多个步骤里。
- 这一版只吸收文档体系中的信息，不在本步骤提前混入 Jira 或历史 testcase 样本。

## 4.5 review baseline 并输出 `baseline/testcase_base_reviewed.md`

生成 `working_dir/baseline/testcase_base.md` 后，立刻做一次 review，再输出：

- `working_dir/baseline/testcase_base_reviewed.md`

在 review 开始前，先用以下脚本做格式测试：

```bash
python scripts/validate_testrail_case.py --source <working_dir/baseline/testcase_base.md 的绝对路径>
```

review 必查项：

1. 文档中的所有场景是否都有落点
2. 能拆成多条用例的地方是否已经拆开
3. 是否存在“一条 case 实际上藏了多条 case”的情况
4. 是否存在正文与已全文读取材料不一致的情况
5. 是否符合 `references/testrail_default.md` 的模板结构，且能被 parser 成功解析

如果发现缺场景、缺分支、缺观测、粒度过粗、模板不齐或 parser 失败，先回修，再输出 reviewed 版本。

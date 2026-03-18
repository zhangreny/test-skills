# Step 4：强制全量读取用户与 Drive 文档、按需读取 SmartX 产品文档并直接生成首版用例

## 目录

- 4.1 建立 `working_dir`
- 4.2 强制全量读取用户输入与 Drive 补充资料
- 4.3 强制按需读取 SmartX 产品手册与白皮书
- 4.4 直接生成 `testcase_1_direct.md`
- 4.5 review 首版并输出 `testcase_1_direct_reviewed.md`

## 4.1 建立 `working_dir`

如果这是本轮流程中第一次生成 testcase 文件，先创建统一工作目录：

- 如果调用方或用户明确给了 `output_dir`，则在该目录下创建独立子目录：`.codex-testcase-generate`
- 如果没有提供 `output_dir`，则自动创建系统临时目录下的时间戳工作目录：
  - Windows：`%TEMP%\\codex-testcase-generate-YYYYMMDD-HHMMSS`
  - macOS / Linux：`/tmp/codex-testcase-generate-YYYYMMDD-HHMMSS`

从 Step 4 开始，把所有中间产物和终稿都放在这个 `working_dir` 下。

同时创建并维护：

- `working_dir/full_read_manifest.md`

## 4.2 强制全量读取用户输入与 Drive 补充资料

本步骤至少完整读取以下输入：

- 用户原始需求文档
- Step 3 下载到本地的相关 Drive 补充文档

执行要求：

- 不要只看文件名、标题或首段摘要。
- 不要只抽取关键词后停止。
- 对 `.md` 直接全文读取。
- 对 `.pdf`、`.docx` 使用当前环境可行的本地方式抽取全文，并确保全文被读完，而不是只取第一页或局部段落。
- 如果某份关键文件体积较大，按分段方式继续读到全文结束，不要因为单次输出过长就提前停止。
- 在 `working_dir/full_read_manifest.md` 中记录每份已全文读取的文件。

## 4.3 强制按需读取 SmartX 产品手册与白皮书

围绕 Step 2 已确认的主体产品与功能，先在 `../smartx-docs-download/markdown_docs` 中定位产品文档，再强制读取与当前 feature 直接相关的文档内容。

最低要求：

- 必须读取直接相关的产品手册类文档
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
  - 当前 feature 所属模块 / 对象定义
  - 主流程与关键操作路径
  - 关键限制、前置条件、规格约束
  - 异常、恢复、兼容、升级、运维或故障相关章节中与当前 feature 直接相关的部分
- 如果某份产品文档与当前 feature 高度直接相关且篇幅可控，可以全文读取；但默认不要求整本文档全文通读。
- 在 `working_dir/full_read_manifest.md` 中记录每份产品文档读取了哪些章节、主题或段落范围，以及为什么这些内容足以支撑当前 feature 理解。
- 如果没有找到直接相关的产品手册或白皮书，明确说明缺口，不能假装已理解产品。

## 4.4 直接生成 `testcase_1_direct.md`

在完成“用户与 Drive 文档全文读取”以及“产品文档按需充分读取”后，直接按 `references/testrail_default.md` 的结构生成首版 testcase，不使用 seed 理论。

输出文件：

- `working_dir/testcase_1_direct.md`

生成要求：

- 直接基于全文材料生成 testcase 正文，不要先生成 seed 表。
- 默认倾向“尽可能多、尽可能细、尽可能展开条数”。
- 目录层级不要被固定成三层；按 feature 复杂度、对象分组、子场景和子路径需要，允许使用 `##` 到 `######` 形成更深的模块 / 子模块 / subsection / case 树。
- 对以下差异优先拆成独立 case：
  - 对象差异
  - 前置条件差异
  - 输入值 / 边界值差异
  - 状态切换前后差异
  - 异常类型差异
  - 恢复 / 清理 / 回退差异
  - 入口差异
  - 结果信号差异
  - 观测方式差异
  - 生命周期阶段差异
- 每条 case 的步骤数不设上限；按执行闭环需要使用 `【Step1】` 到 `【StepN】`。
- 不要把多个可独立验证的结果藏在一条 case 的多个步骤里。
- 如果关键验证依赖日志、告警、任务状态、CLI、API、抓包、trace、报表等观测手段，在 `描述：` 或 `【Step3】` 中显式写出来。
- 这一版只吸收文档体系中的信息，不在本步骤提前混入 Jira 或历史 testcase 样本。

## 4.5 review 首版并输出 `testcase_1_direct_reviewed.md`

生成 `working_dir/testcase_1_direct.md` 后，立刻做一次 review，再输出：

- `working_dir/testcase_1_direct_reviewed.md`

在 review 开始前，先用以下脚本做格式测试：

```bash
python ../testrail-testcase-extract-upload/scripts/parse_testrail_template.py --source <working_dir/testcase_1_direct.md 的绝对路径> --pretty
```

规则：

- `--source` 必须传 testcase 文件的绝对路径。
- 按 UTF-8 读取 testcase 文件。
- 如果脚本解析失败、提示结构不合法或怀疑乱码，先修 testcase 格式或编码，再继续后续 review。

review 必查项：

1. 文档中的所有场景是否都有落点
2. 能拆成多条用例的地方是否已经拆开
3. 是否存在“表面上一条 case，实际上步骤里藏了多条 case”的情况
4. 是否存在正文与“已全文读取的用户 / Drive 材料”及“已按需读取的产品文档章节”不一致的情况
5. 是否符合 `references/testrail_default.md` 的模板结构：层级深度按内容需要展开，步骤数量按执行需要展开，并能被 `parse_testrail_template.py` 成功解析

回修规则：

- 如果发现缺场景、缺分支、缺观测、粒度过粗、模板不齐或 parser 解析失败，先回修，再输出 reviewed 版本。
- reviewed 版本必须保留并扩展 direct 版本内容，不要减少已写出的有效用例。

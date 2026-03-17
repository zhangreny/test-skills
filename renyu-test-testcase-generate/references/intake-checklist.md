# Intake Checklist

## 目录模式下的候选文档判断

优先推荐以下名称或扩展名的文件作为测试用例生成输入：

- 扩展名：`.doc`、`.docx`、`.pdf`、`.md`、`.txt`、`.ppt`、`.pptx`
- 文件名关键词：`需求`、`设计`、`方案`、`说明`、`规格`、`prd`、`spec`、`design`、`api`、`story`、`userstory`、`原型`、`流程`、`架构`

降低优先级但仍然列出：

- 图片、压缩包、二进制安装包、日志、缓存、构建产物
- 文件名包含 `log`、`cache`、`tmp`、`debug`、`dist`、`build`

## 推荐的用户确认话术

目录模式：

```text
我已经列出了该目录下的文件，并标出了更像需求/设计文档的候选项。请直接告诉我这次要用哪些文件生成测试用例；即使只有一个文件，也请你确认一下。
```

整理完 `temp_inputs` 之后：

```text
当前 `temp_inputs` 中的这些文件会作为本轮测试用例生成输入。若没有问题，请回复“继续”或“开始生成”；如果要增删替换文件，直接告诉我。
```

Google 文档下载失败之后：

```text
至少有一个 Google 文档下载失败了，这一轮先不继续。请你自行导出对应文件后重新上传；如果浏览器里只打开了当前文档，请选择 Current tab，如果同时打开了多个相关文档并且都要导出，请选择 All tabs。
```

## 临时目录约定

```text
<Downloads>/testcase-generate-YYYYMMDD-HHMMSS/
  temp_inputs/
  google-drive-file-download/   # 仅在 Google 文档模式下由下游子技能创建
```

`temp_inputs` 始终代表“已经被本轮确认会参与测试用例生成的输入文件”。

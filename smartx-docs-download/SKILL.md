---
name: smartx-docs-download
description: 爬取 SmartX 内部文档站（internal-docs.smartx.com）的文档索引，并用 Playwright 打开文档页面，递归展开左侧导航、逐项点击目录、抓取右侧正文和表格并导出为 Markdown。适用于需要批量获取 SmartX 内部文档链接、离线保存文档正文、或把站点内容转换为可搜索的 md 文件时使用。
---

# SmartX Docs Download

## 概述

这个 skill 提供两个脚本：

1. `scripts/crawl_doc_index.py`
用于访问文档站首页，解析所有产品/版本文档入口，生成 `doc_index.json`。

2. `scripts/download_docs.py`
用于读取 `doc_index.json`，打开每个文档页面，展开左侧目录树，逐节抓取右侧正文，导出为 Markdown。

## 环境要求

- Python `3.9`
- 本机已安装 Google Chrome
- 可访问 `https://internal-docs.smartx.com`

## 安装依赖

```bash
pip install -r scripts/requirements.txt
playwright install chrome
```

## 使用流程

### 1. 构建文档索引

```bash
python scripts/crawl_doc_index.py
```

脚本默认在自身目录生成 `doc_index.json`。

### 2. 抓取文档并导出 Markdown

```bash
python scripts/download_docs.py
```

默认行为：

- 从同目录 `doc_index.json` 读取文档链接
- 将抓取结果输出到同目录下的 `markdown_docs/`
- 一个文档生成一个 `.md` 文件

常用参数：

```bash
python scripts/download_docs.py -i doc_index.json -o markdown_docs
python scripts/download_docs.py --match "配置和管理规格" --limit 1
```

## 关键实现

### 左侧导航抓取

脚本不会点击“下载 PDF”，而是：

- 定位左侧导航 `nav._1iv8wwv2`
- 对带子分类的目录项先点击展开按钮 `div._1iv8wwv6`
- 展开后重新扫描目录，避免因为 DOM 重渲染漏抓子项
- 只对实际链接 `a._1iv8wwvb[href]` 执行点击

### 正文提取

右侧正文从 `data-docs-content="true"` 容器读取，保留：

- 标题
- 段落
- 列表
- 表格

HTML 会通过 `markdownify` 转为 Markdown。

## 输出和仓库约定

- `doc_index.json` 和 `markdown_docs/` 都是运行产物
- 默认只在本地使用，不应提交到 skill 仓库
- 提交 skill 仓库时，只同步脚本和必要元数据

## 常见问题

| 问题 | 原因 | 处理方式 |
|------|------|----------|
| 左侧子分类漏抓 | 展开后导航重渲染 | 重新扫描导航树后继续遍历 |
| 正文没有变化 | 页面切换较慢 | 适当增加等待时间 |
| Chrome 未找到 | 本机未安装 Chrome | 执行 `playwright install chrome` |
| 依赖缺失 | 未安装 `markdownify` / `playwright` | 重新执行 `pip install -r scripts/requirements.txt` |

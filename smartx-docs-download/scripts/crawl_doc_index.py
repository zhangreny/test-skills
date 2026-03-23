#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只访问首页一次，从 https://internal-docs.smartx.com/ 解析所有产品索引链接，输出 JSON。
格式示例: "SMTXOS/6.3.0/SMTXOS 发布说明": "https://internal-docs.smartx.com/smtxos/6.3.0/release_notes/release-notes"
需安装: pip install requests beautifulsoup4
"""

import json
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://internal-docs.smartx.com"
OUTPUT_JSON = "doc_index.json"
# 只保留路径为 /产品名/版本号/ 的链接（版本号 x.x 或 x.x.x）
VERSION_PATH_RE = re.compile(r"^/([^/]+)/(\d+\.\d+(?:\.\d+)?)/")
REQUEST_TIMEOUT = 30
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def normalize_product_key(path_segment: str) -> str:
    """路径里的产品名转成 key 用显示名，如 smtxos -> SMTXOS"""
    s = path_segment.strip()
    if not s:
        return s
    upper = s.upper().replace("-", "_")
    if "SMTX" in upper or "CLOUD" in upper or "ELF" in upper:
        return upper.replace("-", "_")
    return s


def build_index_from_one_page(session: requests.Session) -> dict:
    """只请求首页一次，解析所有 产品/版本 链接，用链接文字做标题，生成 key -> url"""
    print(f"正在请求首页（仅此一次）: {BASE_URL}")
    r = session.get(BASE_URL + "/", headers=HEADERS, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    r.encoding = r.apparent_encoding or "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    result = {}
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        full = urljoin(BASE_URL + "/", href).split("#")[0].rstrip("/")
        if not full.startswith(BASE_URL):
            continue
        path = urlparse(full).path
        m = VERSION_PATH_RE.search(path)
        if not m:
            continue
        product_slug, version = m.group(1), m.group(2)
        product_key = normalize_product_key(product_slug)
        title = a.get_text(strip=True) or path.split("/")[-1] or "untitled"
        key = f"{product_key}/{version}/{title}"
        result[key] = full

    return result


def main():
    session = requests.Session()
    index = build_index_from_one_page(session)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"已写入 {OUTPUT_JSON}，共 {len(index)} 条。")


if __name__ == "__main__":
    main()

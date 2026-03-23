#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 doc_index.json 读取所有文档 URL，用 Playwright 打开每个页面，
依次点击左侧导航中的所有条目，抓取右侧正文区域，并将整篇文档保存为 Markdown。

用法:
    python download_docs.py
    python download_docs.py -i doc_index.json -o markdown_docs
    python download_docs.py --match "配置和管理规格" --limit 1

依赖:
    pip install playwright markdownify beautifulsoup4
    playwright install chrome
"""

import argparse
import json
import re
import sys
from pathlib import Path

from markdownify import markdownify as html_to_md
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

DOC_INDEX = Path(__file__).parent / "doc_index.json"
OUTPUT_DIR = Path(__file__).parent / "markdown_docs"

NAV_TIMEOUT = 30_000
NETWORKIDLE_TIMEOUT = 15_000
RENDER_WAIT_MS = 800
EXPAND_WAIT_MS = 800
WAIT_SELECTOR_TIMEOUT = 10_000

NAV_SELECTOR = "nav._1iv8wwv2"
CONTENT_SELECTOR = '[data-docs-content="true"]'


def sanitize_filename(name: str, suffix: str = ".md") -> str:
    """将 key（含 / 和空格）转为合法文件名。"""
    safe = re.sub(r'[\\/:*?"<>|\r\n]', "_", name)
    return safe + suffix


def normalize_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", (text or "").strip())


def wait_page_ready(page) -> None:
    page.wait_for_selector(NAV_SELECTOR, timeout=WAIT_SELECTOR_TIMEOUT)
    page.wait_for_selector(CONTENT_SELECTOR, timeout=WAIT_SELECTOR_TIMEOUT)
    try:
        page.wait_for_load_state("networkidle", timeout=NETWORKIDLE_TIMEOUT)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(RENDER_WAIT_MS)


def get_content_signature(page) -> str:
    try:
        text = page.locator(CONTENT_SELECTOR).first.inner_text(timeout=WAIT_SELECTOR_TIMEOUT)
    except Exception:
        return ""
    return normalize_text(text)[:500]


def html_to_markdown(html: str) -> str:
    markdown = html_to_md(
        html,
        heading_style="ATX",
        bullets="-",
        strong_em_symbol="*",
        table_infer_header=True,
    )
    markdown = markdown.replace("\r\n", "\n").replace("\xa0", " ")
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def extract_content_markdown(page) -> str:
    html = page.locator(CONTENT_SELECTOR).first.inner_html(timeout=WAIT_SELECTOR_TIMEOUT)
    return html_to_markdown(html)


def get_nav_items(page):
    return page.evaluate(
        """
() => {
  const nav = document.querySelector('nav._1iv8wwv2');
  if (!nav) return [];

  const normalize = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const visible = (el) => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };

  const getLabel = (li) => {
    const anchor = li.querySelector(':scope > a._1iv8wwvb');
    const label = li.querySelector(':scope > a._1iv8wwvb > div._1iv8wwv6');
    const direct = label || anchor || li.querySelector(':scope > div, :scope > button, :scope > span');
    return normalize(direct ? direct.innerText : li.innerText);
  };

  const getPath = (li) => {
    const parts = [];
    let current = li;
    while (current && current.matches && current.matches('li._1iv8wwv5')) {
      const label = getLabel(current);
      if (label) parts.unshift(label);
      current = current.parentElement ? current.parentElement.closest('li._1iv8wwv5') : null;
    }
    return parts.join(' > ');
  };

  return Array.from(nav.querySelectorAll('li._1iv8wwv5'))
    .filter((li) => visible(li))
    .map((li) => {
      const anchor = li.querySelector(':scope > a._1iv8wwvb');
      const link = li.querySelector(':scope > a._1iv8wwvb[href]');
      const submenu = li.querySelector(':scope > ul._1iv8wwv7');
      const isDropdown = li.classList.contains('dropdown');
      const toggle = isDropdown ? (li.querySelector(':scope > a._1iv8wwvb > div._1iv8wwv6') || anchor) : null;
      const levelMatch = li.className.match(/level-(\\d+)/);
      return {
        text: getLabel(li),
        path: getPath(li),
        href: link ? (link.getAttribute('href') || '') : '',
        has_link: !!link,
        has_toggle: !!toggle,
        is_dropdown: isDropdown || !!submenu,
        expanded: !!(submenu && visible(submenu)),
        level: levelMatch ? Number(levelMatch[1]) : 0,
      };
    })
    .filter((item) => item.text && item.path);
}
"""
    )


def click_nav_item(page, item_path: str) -> bool:
    return bool(
        page.evaluate(
            """
(targetPath) => {
  const nav = document.querySelector('nav._1iv8wwv2');
  if (!nav) return false;

  const normalize = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const visible = (el) => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };

  const getLabel = (li) => {
    const anchor = li.querySelector(':scope > a._1iv8wwvb');
    const label = li.querySelector(':scope > a._1iv8wwvb > div._1iv8wwv6');
    const direct = label || anchor || li.querySelector(':scope > div, :scope > button, :scope > span');
    return normalize(direct ? direct.innerText : li.innerText);
  };

  const getPath = (li) => {
    const parts = [];
    let current = li;
    while (current && current.matches && current.matches('li._1iv8wwv5')) {
      const label = getLabel(current);
      if (label) parts.unshift(label);
      current = current.parentElement ? current.parentElement.closest('li._1iv8wwv5') : null;
    }
    return parts.join(' > ');
  };

  const li = Array.from(nav.querySelectorAll('li._1iv8wwv5'))
    .filter((node) => visible(node))
    .find((node) => getPath(node) === targetPath);

  if (!li) return false;

  const link = li.querySelector(':scope > a._1iv8wwvb[href]');
  if (!link || !visible(link)) return false;

  link.scrollIntoView({block: 'center'});
  link.click();
  return true;
}
""",
            item_path,
        )
    )


def expand_nav_item(page, item_path: str) -> bool:
    return bool(
        page.evaluate(
            """
(targetPath) => {
  const nav = document.querySelector('nav._1iv8wwv2');
  if (!nav) return false;

  const normalize = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const visible = (el) => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };

  const getLabel = (li) => {
    const anchor = li.querySelector(':scope > a._1iv8wwvb');
    const label = li.querySelector(':scope > a._1iv8wwvb > div._1iv8wwv6');
    const direct = label || anchor || li.querySelector(':scope > div, :scope > button, :scope > span');
    return normalize(direct ? direct.innerText : li.innerText);
  };

  const getPath = (li) => {
    const parts = [];
    let current = li;
    while (current && current.matches && current.matches('li._1iv8wwv5')) {
      const label = getLabel(current);
      if (label) parts.unshift(label);
      current = current.parentElement ? current.parentElement.closest('li._1iv8wwv5') : null;
    }
    return parts.join(' > ');
  };

  const li = Array.from(nav.querySelectorAll('li._1iv8wwv5'))
    .filter((node) => visible(node))
    .find((node) => getPath(node) === targetPath);

  if (!li) return false;

  const submenu = li.querySelector(':scope > ul._1iv8wwv7');
  if (submenu && visible(submenu)) return true;

  const toggle = li.querySelector(':scope > a._1iv8wwvb > div._1iv8wwv6') || li.querySelector(':scope > a._1iv8wwvb');
  if (!toggle || !visible(toggle)) return false;

  toggle.scrollIntoView({block: 'center'});
  toggle.click();
  return true;
}
""",
            item_path,
        )
    )


def expand_all_dropdowns(page) -> int:
    return int(
        page.evaluate(
            """
() => {
  const nav = document.querySelector('nav._1iv8wwv2');
  if (!nav) return 0;

  const visible = (el) => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };

  let expandedCount = 0;
  const dropdowns = Array.from(nav.querySelectorAll('li._1iv8wwv5.dropdown'));

  for (const li of dropdowns) {
    if (!visible(li)) continue;

    const submenu = li.querySelector(':scope > ul._1iv8wwv7');
    if (submenu && visible(submenu)) continue;

    const toggle =
      li.querySelector(':scope > a._1iv8wwvb > div._1iv8wwv6') ||
      li.querySelector(':scope > a._1iv8wwvb') ||
      li.querySelector(':scope > span') ||
      li.querySelector(':scope > div._1iv8wwv6');

    if (!toggle || !visible(toggle)) continue;

    toggle.scrollIntoView({ block: 'center' });
    toggle.click();
    expandedCount += 1;
  }

  return expandedCount;
}
""",
        )
    )


def dump_document_markdown(page, name: str, url: str) -> str:
    visited = set()
    sections = []

    # 先把当前文档左侧所有可见 dropdown 递归展开，避免遗漏子分类。
    for _ in range(20):
        expanded_count = expand_all_dropdowns(page)
        if expanded_count <= 0:
            break
        page.wait_for_timeout(EXPAND_WAIT_MS)

    while True:
        # 某些目录会在点击正文后重新收起，进入下一轮前再兜底展开一次。
        expanded_count = expand_all_dropdowns(page)
        if expanded_count > 0:
            page.wait_for_timeout(EXPAND_WAIT_MS)

        items = get_nav_items(page)

        next_item = next(
            (item for item in items if item["path"] not in visited and item["has_link"]),
            None,
        )
        if not next_item:
            break

        path = next_item["path"]
        visited.add(path)
        previous_signature = get_content_signature(page)

        if not click_nav_item(page, path):
            continue

        page.wait_for_timeout(RENDER_WAIT_MS)
        try:
            page.wait_for_function(
                """
                ([selector, previous]) => {
                    const el = document.querySelector(selector);
                    if (!el) return false;
                    const current = (el.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 500);
                    return current !== previous;
                }
                """,
                arg=[CONTENT_SELECTOR, previous_signature],
                timeout=3_000,
            )
        except PlaywrightTimeoutError:
            pass

        refreshed = next((item for item in get_nav_items(page) if item["path"] == path), None)
        if refreshed and refreshed["is_dropdown"] and not refreshed["has_link"]:
            if get_content_signature(page) == previous_signature:
                continue

        body = extract_content_markdown(page)
        if not body:
            continue

        sections.append(f"## {path}\n\n{body}")

    if not sections:
        body = extract_content_markdown(page)
        if body:
            sections.append(f"## 正文\n\n{body}")

    header = [
        "---",
        f'title: "{name.replace(chr(34), chr(39))}"',
        f'source_url: "{url}"',
        f"sections: {len(sections)}",
        "---",
        "",
        f"# {name}",
        "",
    ]
    return "\n".join(header) + "\n\n---\n\n".join(sections) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="抓取 SmartX 文档站并导出 Markdown")
    parser.add_argument("-i", "--index", default=str(DOC_INDEX), help="doc_index.json 路径")
    parser.add_argument("-o", "--output", default=str(OUTPUT_DIR), help="Markdown 输出目录")
    parser.add_argument("--match", default="", help="仅处理名称包含该字符串的文档")
    parser.add_argument("--limit", type=int, default=0, help="最多处理 N 个文档，0 表示不限")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(args.index, encoding="utf-8") as f:
        doc_index = json.load(f)

    if args.match:
        doc_index = {k: v for k, v in doc_index.items() if args.match.lower() in k.lower()}
    if args.limit > 0:
        doc_index = dict(list(doc_index.items())[: args.limit])

    total = len(doc_index)
    print(f"共 {total} 个文档，输出目录: {output_dir}\n")
    if total == 0:
        print("[warn] 没有匹配到任何文档")
        return 1

    success_list = []
    skip_list = []
    failed_list = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--start-maximized"],
        )
        context = browser.new_context(viewport={"width": 1600, "height": 900})
        page = context.new_page()

        for idx, (name, url) in enumerate(doc_index.items(), 1):
            filename = sanitize_filename(name)
            output_path = output_dir / filename
            prefix = f"[{idx:>3}/{total}]"

            if output_path.exists():
                print(f"{prefix} [skip] {name}")
                skip_list.append(name)
                continue

            print(f"{prefix} [open] {url}")
            try:
                page.goto(url, timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
                wait_page_ready(page)
                markdown = dump_document_markdown(page, name, url)
                output_path.write_text(markdown, encoding="utf-8")
                size_kb = output_path.stat().st_size // 1024
                print(f"{prefix} [ok] {output_path.name}  ({size_kb} KB)")
                success_list.append(name)
            except PlaywrightTimeoutError as e:
                msg = f"timeout: {e}"
                print(f"{prefix} [fail] {msg}")
                failed_list.append((name, url, msg))
            except Exception as e:
                msg = str(e)[:200]
                print(f"{prefix} [fail] {msg}")
                failed_list.append((name, url, msg))

        context.close()
        browser.close()

    print("\n" + "=" * 60)
    print(f"完成  成功: {len(success_list)}  已存在跳过: {len(skip_list)}  失败: {len(failed_list)}")

    if failed_list:
        print("\n失败列表:")
        for name, url, err in failed_list:
            print(f"  [x] {name}")
            print(f"      {url}")
            print(f"      原因: {err}")

        failed_json = output_dir.parent / "download_failed.json"
        with open(failed_json, "w", encoding="utf-8") as f:
            json.dump(
                [{"name": n, "url": u, "error": e} for n, u, e in failed_list],
                f,
                ensure_ascii=False,
                indent=2,
            )
        print(f"\n失败记录已写入: {failed_json}")

    return 0 if not failed_list else 1


if __name__ == "__main__":
    sys.exit(main())

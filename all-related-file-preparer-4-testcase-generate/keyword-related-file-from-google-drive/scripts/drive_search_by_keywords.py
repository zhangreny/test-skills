#!/usr/bin/env python3
"""
对每个关键词执行 gog drive search，合并并按 file id 去重，输出 JSON。

gog 会两次提示 "Enter passphrase to unlock keyring"，脚本通过 PTY 自动发送两次回车，
无需手动输入（若已解锁过 keyring，直接回车即可通过）。

用法:
  python drive_search_by_keywords.py 关键词1 关键词2 ...
  echo -e "关键词1\n关键词2" | python drive_search_by_keywords.py

输出: 标准输出为 JSON 数组 [{ "name", "webViewLink" }, ...]，按 file id 去重。
"""

import argparse
import json
import os
import select
import subprocess
import sys
import pty
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List


def escape_drive_query_value(keyword: str) -> str:
    """转义关键词以安全放入 fullText contains '...'：反斜杠与单引号需转义。"""
    if not keyword:
        return ""
    return keyword.replace("\\", "\\\\").replace("'", "\\'")


def _run_gog_with_pty(cmd: List[str], timeout: int, send_enters: bytes = b"\n\n") -> str:
    """在伪终端中执行 cmd，先发送 send_enters（两次回车），再读取全部输出。"""
    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            close_fds=True,
        )
        os.close(slave)
        slave = None

        # 先发两次回车，满足 gog 的 "Enter passphrase" 提示（空密码或已解锁时直接过）
        time.sleep(0.1)
        os.write(master, send_enters)

        out_chunks: List[bytes] = []
        deadline = time.monotonic() + timeout
        while True:
            remaining = max(0.01, deadline - time.monotonic())
            r, _, _ = select.select([master], [], [], remaining)
            if not r:
                proc.kill()
                proc.wait()
                return ""
            try:
                buf = os.read(master, 4096)
            except OSError:
                break
            if not buf:
                break
            out_chunks.append(buf)
            if proc.poll() is not None:
                # 进程已退出，再读一次清空 PTY 缓冲
                try:
                    while True:
                        buf = os.read(master, 4096)
                        if not buf:
                            break
                        out_chunks.append(buf)
                except (OSError, BlockingIOError):
                    pass
                break
        proc.wait()
        return (b"".join(out_chunks)).decode("utf-8", errors="replace")
    finally:
        if slave is not None:
            try:
                os.close(slave)
            except OSError:
                pass
        try:
            os.close(master)
        except OSError:
            pass


def run_search(
    keyword: str,
    max_results: int = 15,
    timeout: int = 60,
    verbose: bool = False,
) -> List[dict]:
    """执行单次 gog drive search（PTY 内自动两次回车），返回解析后的记录列表。"""
    safe = escape_drive_query_value(keyword)
    query = f"fullText contains '{safe}'"
    cmd = [
        "gog", "drive", "search",
        query,
        "--max", str(max_results),
        "--json",
    ]
    try:
        out = _run_gog_with_pty(cmd, timeout=timeout).strip()
        if verbose and out:
            print(out, file=sys.stderr)
        if not out:
            return []
        # 从 PTY 输出中提取 JSON（前面可能有 "Enter passphrase" 等 prompt）
        def parse_json_and_return(data: object) -> List[dict]:
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "files" in data:
                return data["files"]
            if isinstance(data, dict):
                return [data]
            return []

        try:
            return parse_json_and_return(json.loads(out))
        except json.JSONDecodeError:
            pass
        # 找 JSON 起始位置（gog 输出最后是 {"files": ...}）
        for start in (out.find('{"files"'), out.find("{\n  \"files\""), out.rfind("\n{")):
            if start == -1:
                continue
            if start >= 0 and out[start] == "\n":
                start += 1
            try:
                return parse_json_and_return(json.loads(out[start:]))
            except json.JSONDecodeError:
                continue
        return []
    except FileNotFoundError:
        return []
    except OSError:
        return []


def dedupe_and_trim(records: List[dict]) -> List[dict]:
    """按 id 去重（保留首次出现顺序），只保留 id、name、webViewLink。"""
    """筛选 "mimeType": "application/vnd.google-apps.document" """
    seen: Dict[str, dict] = {}
    for r in records:
        if not isinstance(r, dict):
            continue
        if r.get("mimeType") != "application/vnd.google-apps.document":
            continue
        fid = r.get("id")
        if not fid or fid in seen:
            continue
        seen[fid] = {
            "id": fid,
            "name": r.get("name") or "",
            "webViewLink": r.get("webViewLink") or "",
        }
    return list(seen.values())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="按关键词在 Google Drive 全文搜索，合并去重后输出 JSON。",
    )
    parser.add_argument(
        "keywords",
        nargs="*",
        help="关键词列表；若不提供则从 stdin 读取（每行一个）。",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=15,
        metavar="N",
        help="每个关键词最多返回条数（默认 15）。",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        metavar="SEC",
        help="单次搜索超时秒数（默认 60）。",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=0,
        metavar="J",
        help="并发搜索数，0 表示与关键词数一致（默认 0）。",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="将搜索进度等信息输出到 stderr。",
    )
    args = parser.parse_args()

    if args.keywords:
        keywords = [k.strip() for k in args.keywords if k.strip()]
    else:
        keywords = [line.strip() for line in sys.stdin if line.strip()]

    if not keywords:
        print("[]")
        return

    max_per_kw = max(1, args.max)
    timeout_sec = max(1, args.timeout)
    n_jobs = args.jobs if args.jobs > 0 else len(keywords)
    n_jobs = min(n_jobs, len(keywords))

    all_records: List[dict] = []
    if n_jobs <= 1:
        for kw in keywords:
            if not kw:
                continue
            if args.verbose:
                print(f"[drive_search] 搜索: {kw!r}", file=sys.stderr)
            all_records.extend(run_search(kw, max_results=max_per_kw, timeout=timeout_sec, verbose=args.verbose))
    else:
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            future_to_kw = {
                executor.submit(run_search, kw, max_per_kw, timeout_sec, args.verbose): kw
                for kw in keywords if kw
            }
            for future in as_completed(future_to_kw):
                kw = future_to_kw[future]
                try:
                    items = future.result()
                    all_records.extend(items)
                    if args.verbose:
                        print(f"[drive_search] 完成: {kw!r} -> {len(items)} 条", file=sys.stderr)
                except Exception as e:
                    if args.verbose:
                        print(f"[drive_search] 失败: {kw!r} -> {e}", file=sys.stderr)

    result = dedupe_and_trim(all_records)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

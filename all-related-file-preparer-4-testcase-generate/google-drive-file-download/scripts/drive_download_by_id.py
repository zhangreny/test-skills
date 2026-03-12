#!/usr/bin/env python3
"""
对单个 Google Drive 文件 ID 执行 gog drive download，将文件下载到指定目录。

gog 可能提示 "Enter passphrase to unlock keyring"，脚本通过 PTY 自动发送两次回车。
批量下载时由调用方循环，每次传入一个 --id，便于定位失败并重试。

用法:
  python drive_download_by_ids.py --output /path/to/dir --id <文件ID>

退出码: 0 表示成功，非 0 表示失败（错误详情在 stderr）。
"""

import argparse
import os
import select
import subprocess
import sys
import pty
import time
from typing import List, Tuple


def _run_gog_with_pty(cmd: List[str], timeout: int, send_enters: bytes = b"\n\n") -> Tuple[int, str, str]:
    """在伪终端中执行 cmd，先发送 send_enters，再读取全部输出。返回 (returncode, stdout, stderr 合并后的输出)。"""
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
                return (proc.returncode or -1, "", "timeout")
            try:
                buf = os.read(master, 4096)
            except OSError:
                break
            if not buf:
                break
            out_chunks.append(buf)
            if proc.poll() is not None:
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
        out = (b"".join(out_chunks)).decode("utf-8", errors="replace")
        return (proc.returncode or 0, out, out)
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


def download_one(file_id: str, output_dir: str, timeout: int = 120) -> Tuple[bool, str]:
    """执行 gog drive download <id> --output <dir>，返回 (成功, 错误信息)。"""
    if not file_id or not output_dir:
        return False, "file_id 或 output_dir 为空"
    cmd = [
        "gog", "drive", "download", file_id.strip(),
        "--output", output_dir,
    ]
    try:
        code, out, _ = _run_gog_with_pty(cmd, timeout=timeout)
        if code == 0:
            return True, ""
        return False, out.strip() or f"退出码 {code}"
    except FileNotFoundError:
        return False, "未找到 gog 命令，请先安装 gog CLI"
    except Exception as e:
        return False, str(e)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="按 Google Drive 文件 ID 下载单个文件到指定目录。",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        metavar="DIR",
        help="下载目标目录。",
    )
    parser.add_argument(
        "--id",
        required=True,
        metavar="ID",
        help="要下载的文件 ID。",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        metavar="SEC",
        help="下载超时秒数（默认 120）。",
    )
    args = parser.parse_args()

    output_dir = os.path.expanduser(args.output)
    if not os.path.isdir(output_dir):
        print(f"错误：输出目录不存在或不是目录: {output_dir}", file=sys.stderr)
        sys.exit(2)

    fid = (args.id or "").strip()
    if not fid:
        print("未提供文件 ID。", file=sys.stderr)
        sys.exit(2)

    ok, err = download_one(fid, output_dir, timeout=args.timeout)
    if ok:
        print(f"{fid} 下载成功", file=sys.stderr)
        sys.exit(0)
    print(f"{fid} 失败: {err}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

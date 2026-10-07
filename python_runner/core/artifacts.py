from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional


_DEBUG_DIR_RE = re.compile(
    r"====\s*Debug output.*?====\s*\n\s*([^\r\n]+)",
    re.IGNORECASE | re.DOTALL,
)


def parse_debug_dir_from_output(text: str) -> Optional[Path]:
    """从 maestro stdout/stderr 解析 debug 目录。"""
    if not text:
        return None
    m = _DEBUG_DIR_RE.search(text)
    if not m:
        # 兜底：单独一行 Windows/Unix 路径且包含 .maestro\tests 或 /tests/
        for line in text.splitlines():
            s = line.strip().strip('"')
            if not s:
                continue
            lower = s.lower()
            if ".maestro" in lower and "tests" in lower:
                p = Path(s)
                if p.exists():
                    return p
        return None
    p = Path(m.group(1).strip().strip('"'))
    return p if p.exists() else p


def latest_debug_dir(debug_root: Path, after: datetime) -> Optional[Path]:
    """若输出未带路径，则取 debug_root 下 after 之后最新的一次运行目录。"""
    if not debug_root.exists():
        return None
    candidates = []
    for child in debug_root.iterdir():
        if not child.is_dir():
            continue
        try:
            mtime = datetime.fromtimestamp(child.stat().st_mtime)
        except OSError:
            continue
        if mtime >= after:
            candidates.append((mtime, child))
    if not candidates:
        # 放宽：取最新一个
        all_dirs = [c for c in debug_root.iterdir() if c.is_dir()]
        if not all_dirs:
            return None
        return max(all_dirs, key=lambda p: p.stat().st_mtime)
    return max(candidates, key=lambda x: x[0])[1]


def find_screenshot(
    artifacts_dir: Optional[Path],
    workspace: Path,
    name: str,
) -> Optional[Path]:
    """按截图名查找（允许无扩展名）。"""
    stems = {name, Path(name).stem}
    search_roots = []
    if artifacts_dir and artifacts_dir.exists():
        search_roots.append(artifacts_dir)
    search_roots.append(workspace / ".maestro" / "screenshots")
    search_roots.append(workspace)

    for root in search_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.stem in stems or path.name in stems:
                return path
    return None


def read_text_if_exists(path: Path, limit: int = 2_000_000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    data = path.read_bytes()[:limit]
    return data.decode("utf-8", errors="replace")


def collect_log_text(artifacts_dir: Optional[Path]) -> str:
    if not artifacts_dir or not artifacts_dir.exists():
        return ""
    chunks: list[str] = []
    for pattern in ("**/maestro.log", "**/commands.json", "**/*.log"):
        for path in artifacts_dir.glob(pattern):
            if path.is_file():
                chunks.append(read_text_if_exists(path))
    return "\n".join(chunks)

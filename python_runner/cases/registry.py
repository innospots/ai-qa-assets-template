from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from .base import TestCase
from .discover import discover_cases, list_domains, select_discovered

_DEFAULT_WORKSPACE = Path(__file__).resolve().parents[2]


def list_suites(workspace: Optional[Path] = None) -> List[str]:
    return list_domains(workspace or _DEFAULT_WORKSPACE)


def load_suite(suite: str, workspace: Optional[Path] = None) -> List[TestCase]:
    root = workspace or _DEFAULT_WORKSPACE
    cases = select_discovered(root, suite=suite)
    if not cases:
        raise KeyError(f"未知套件: {suite}，可选: {', '.join(list_suites(root))}")
    return cases


def load_all_cases(workspace: Optional[Path] = None) -> List[TestCase]:
    return discover_cases(workspace or _DEFAULT_WORKSPACE)


def select_cases(
    suite: Optional[str] = None,
    case_id: Optional[str] = None,
    tags: Optional[Sequence[str]] = None,
    flow_path: Optional[str] = None,
    workspace: Optional[Path] = None,
) -> List[TestCase]:
    """按 Flow 文件 / Case ID / 领域目录 / tags 筛选。"""
    root = workspace or _DEFAULT_WORKSPACE
    tag_list = list(tags) if tags else None
    return select_discovered(
        workspace=root,
        suite=suite,
        case_id=case_id,
        tags=tag_list,
        flow_path=flow_path,
    )


def format_case_table(cases: Iterable[TestCase]) -> str:
    lines = [
        f"{'case_id':<24} {'module':<12} {'locale':<8} {'tags':<32} flow",
        "-" * 110,
    ]
    for c in cases:
        lines.append(
            f"{c.case_id:<24} {c.module:<12} {c.locale:<8} "
            f"{','.join(c.tags):<32} {c.flow_path}"
        )
    return "\n".join(lines)

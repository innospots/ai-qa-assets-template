from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

import yaml

from .base import Expectation, TestCase

_SCREENSHOT_RE = re.compile(
    r"takeScreenshot:\s*['\"]?([^'\"\s$\n]+)",
    re.IGNORECASE,
)


def _parse_header(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    header = text.split("---", 1)[0]
    data = yaml.safe_load(header) or {}
    if not isinstance(data, dict):
        return {}
    return data


def _screenshot_names(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8")
    names: List[str] = []
    for match in _SCREENSHOT_RE.finditer(text):
        name = match.group(1).strip()
        if name and "${" not in name:
            names.append(Path(name).stem)
    return names


def flow_to_case(workspace: Path, path: Path) -> TestCase:
    rel = path.resolve().relative_to(workspace.resolve()).as_posix()
    header = _parse_header(path)
    tags = header.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.strip("[]").split(",") if t.strip()]
    tags = [str(t) for t in tags]
    name = str(header.get("name") or path.stem)
    parts = Path(rel).parts
    if parts and parts[0] == "journeys":
        module = "journeys"
    else:
        module = parts[1] if len(parts) > 1 else ""
    locale = ""
    for token in ("zh", "en", "ja"):
        if token in tags or f"_{token}" in path.stem.lower():
            locale = token
            break
    return TestCase(
        case_id=path.stem,
        module=module,
        flow_path=rel,
        locale=locale,
        tags=tags,
        description=name,
        expect=Expectation(screenshot_names=_screenshot_names(path)),
    )


def discover_cases(workspace: Path) -> List[TestCase]:
    """从 flows/ 与 journeys/ 发现可执行入口，不扫描 modules/。"""
    cases: List[TestCase] = []
    for folder in ("flows", "journeys"):
        root = workspace / folder
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.yaml")):
            if path.name.startswith("."):
                continue
            header = _parse_header(path)
            executor = str(header.get("executor") or "").lower()
            if executor in {"api", "web"}:
                continue
            cases.append(flow_to_case(workspace, path))
    return cases


def select_discovered(
    workspace: Path,
    suite: Optional[str] = None,
    case_id: Optional[str] = None,
    tags: Optional[List[str]] = None,
    flow_path: Optional[str] = None,
) -> List[TestCase]:
    cases = discover_cases(workspace)
    if flow_path:
        raw = Path(flow_path)
        if raw.is_absolute():
            try:
                rel = raw.resolve().relative_to(workspace.resolve()).as_posix()
            except ValueError:
                rel = raw.as_posix()
        else:
            rel = raw.as_posix()
        matched = [
            c
            for c in cases
            if c.flow_path == rel or c.flow_path.endswith(rel) or rel.endswith(c.flow_path)
        ]
        if not matched and raw.exists():
            return [flow_to_case(workspace, raw.resolve())]
        if not matched:
            raise FileNotFoundError(f"未找到 Flow: {flow_path}")
        return matched

    if case_id:
        matched = [c for c in cases if c.case_id == case_id]
        if not matched:
            known = ", ".join(c.case_id for c in cases)
            raise KeyError(f"未知用例: {case_id}，已知: {known}")
        return matched

    if suite:
        key = suite.strip().lower()
        cases = [
            c
            for c in cases
            if c.module.lower() == key or c.flow_path.lower().startswith(f"flows/{key}/")
        ]

    if tags:
        tag_set = {t.strip().lower() for t in tags if t.strip()}
        cases = [
            c
            for c in cases
            if tag_set.intersection({t.lower() for t in c.tags})
        ]
    return cases


def list_domains(workspace: Path) -> List[str]:
    domains = {c.module for c in discover_cases(workspace) if c.module}
    return sorted(domains)

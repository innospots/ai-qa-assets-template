#!/usr/bin/env python3
# 用途：检查 Flow YAML 中 runFlow/runScript 引用的相对路径是否存在。
# 用法：python3 skills/test-flow/scripts/check-references.py flows/mobile/demo/TC-MOBILE-DEMO-001.yaml
# 输出：缺失路径列表；失败时 exit 1。

from __future__ import annotations

import re
import sys
from pathlib import Path

RUN_FLOW_FILE = re.compile(
    r"^\s*(?:-\s*)?runFlow:\s*$|^\s*file:\s*(.+)$|^\s*-\s*runFlow:\s*(.+)$",
    re.MULTILINE,
)
RUN_SCRIPT = re.compile(r"runScript:\s*(.+)$", re.MULTILINE)


def extract_refs(text: str) -> list[str]:
    refs: list[str] = []
    for m in RUN_SCRIPT.finditer(text):
        refs.append(m.group(1).strip())
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("- runFlow:") and not line.strip().endswith(".yaml"):
            val = line.split(":", 1)[1].strip()
            if val and not val.startswith("{"):
                refs.append(val)
        if line.strip().startswith("file:"):
            refs.append(line.split(":", 1)[1].strip())
        if line.strip().startswith("- runFlow:") and ".yaml" in line:
            part = line.split(":", 1)[1].strip()
            refs.append(part)
        i += 1
    return refs


def check_flow(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    base = path.parent
    for ref in extract_refs(text):
        ref = ref.strip("'\"")
        if ref.startswith("${"):
            continue
        target = (base / ref).resolve()
        if not target.is_file():
            errors.append(f"missing reference: {ref} (from {path})")
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check-references.py <flow.yaml> [flow2.yaml ...]", file=sys.stderr)
        return 2

    failed = False
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"ERROR: not a file: {path}")
            failed = True
            continue
        print(f"Checking references: {path}")
        errs = check_flow(path)
        if errs:
            failed = True
            for e in errs:
                print(f"  ERROR: {e}")
        else:
            print("  OK")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

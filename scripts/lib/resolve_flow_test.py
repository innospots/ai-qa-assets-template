#!/usr/bin/env python3
"""解析单条 API/Web Flow 清单的 pytest 节点；供正式脚本调用。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a formal API/Web Flow to its pytest node")
    parser.add_argument("executor", choices=["api", "web"])
    parser.add_argument("flow", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    flow = (args.flow if args.flow.is_absolute() else root / args.flow).resolve()
    if not flow.is_relative_to(root / "flows") or not flow.is_file():
        print(f"ERROR: Flow must be an existing formal asset under flows/: {flow}", file=sys.stderr)
        return 1
    try:
        with flow.open(encoding="utf-8") as handle:
            manifest = next(yaml.safe_load_all(handle), None)
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot read Flow: {exc}", file=sys.stderr)
        return 1
    if not isinstance(manifest, dict) or manifest.get("executor") != args.executor:
        print(f"ERROR: Flow executor must be {args.executor}: {flow}", file=sys.stderr)
        return 1
    node = manifest.get("test")
    pattern = rf"executors/{args.executor}/tests/[A-Za-z0-9_/-]+\.py::test_[A-Za-z0-9_]+"
    if not isinstance(node, str) or not re.fullmatch(pattern, node):
        print(f"ERROR: invalid pytest node in Flow: {flow}", file=sys.stderr)
        return 1
    test_file = (root / node.split("::", 1)[0]).resolve()
    if not test_file.is_relative_to(root / "executors" / args.executor / "tests") or not test_file.is_file():
        print(f"ERROR: pytest file does not exist: {test_file}", file=sys.stderr)
        return 1
    print(node)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

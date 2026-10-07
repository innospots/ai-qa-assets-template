#!/usr/bin/env python3
"""跨业务域扫描 Flow，按 executor 和 tags 发现 pytest 节点。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Discover pytest nodes from flow manifests")
    parser.add_argument("executor", choices=["api", "web"])
    parser.add_argument("scope", help="smoke, regression, e2e, special, or all")
    parser.add_argument("--root", default=".", help="repository root")
    return parser.parse_args()


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return next(yaml.safe_load_all(handle), None) or {}


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    flow_root = root / "flows"
    if not flow_root.is_dir():
        print(f"ERROR: missing flow directory: {flow_root}", file=sys.stderr)
        return 1

    nodes: list[str] = []
    for path in sorted(flow_root.rglob("TC-*.yaml")):
        manifest = load_manifest(path)
        if manifest.get("executor") != args.executor:
            continue
        tags = [str(tag).lower() for tag in (manifest.get("tags") or [])]
        scope = args.scope.lower()
        if scope != "all" and scope not in tags:
            continue
        test_node = manifest.get("test")
        if not test_node:
            print(f"ERROR: missing test node in {path}", file=sys.stderr)
            return 1
        nodes.append(str(test_node))

    if not nodes:
        print(f"No tests matched executor={args.executor} scope={args.scope}", file=sys.stderr)
        return 1

    for node in nodes:
        print(node)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# 用途：按 API/Web 清单或 Mobile Maestro YAML 校验单个 Flow 的基础结构。
# 用法：python3 skills/test-flow/scripts/validate-flow.py flows/auth/login/TC-AUTH-LOGIN-001.yaml
# 输出：stdout 问题列表；失败时 exit 1。

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

CASE_ID_IN_NAME = re.compile(r"^TC-[A-Z0-9]+-[A-Z0-9-]+-\d{3}\b")
ASSERT_COMMANDS = (
    "assertVisible",
    "assertNotVisible",
    "assertTrue",
    "assertWithAI",
    "assertScreenshot",
    "assertDarkMode",
    "assertLightMode",
)


def validate_flow(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        documents = list(yaml.safe_load_all(text))
    except yaml.YAMLError as exc:
        return [f"invalid YAML: {exc}"]
    manifest = documents[0] if documents else None
    if isinstance(manifest, dict) and manifest.get("executor") in {"api", "web"}:
        if len(documents) != 1:
            return ["API/Web manifest must contain exactly one YAML document"]
        return validate_manifest(path, manifest)
    if "---" not in text:
        errors.append("missing '---' separator between header and commands")
        return errors
    if len(documents) != 2 or not isinstance(documents[0], dict) or not isinstance(documents[1], list):
        errors.append("Mobile Flow must contain a header and command list")
        return errors

    header, commands = text.split("---", 1)
    header_lines = header.strip().splitlines()

    if not any(line.startswith("appId:") or line.startswith("url:") for line in header_lines):
        errors.append("header must contain appId: or url:")

    name_line = next((l for l in header_lines if l.startswith("name:")), None)
    if not name_line:
        errors.append("header must contain name:")
    else:
        name_val = name_line.split(":", 1)[1].strip()
        if not CASE_ID_IN_NAME.match(name_val):
            errors.append(f"name should start with Case ID (TC-...-NNN): {name_val!r}")

    stem = path.stem
    if not CASE_ID_IN_NAME.match(stem):
        errors.append(f"filename should match Case ID pattern: {path.name}")

    if name_line and not name_val.startswith(stem):
        errors.append(f"name should start with filename stem {stem}")

    if "tags:" not in header and "tags:" not in header.replace(" ", ""):
        if not any(line.startswith("tags:") for line in header_lines):
            errors.append("header should contain tags:")

    if not any(cmd in commands for cmd in ASSERT_COMMANDS):
        errors.append("commands section should contain at least one assertion")

    if re.search(r'inputText:\s*["\'][^"\']{8,}["\']', commands):
        errors.append("possible hardcoded inputText; prefer ${output...} or env variables")

    return errors


def validate_manifest(path: Path, manifest: dict) -> list[str]:
    """API/Web 的 Flow 是 pytest 节点清单，不要求 Maestro 分隔符。"""
    errors: list[str] = []
    if not CASE_ID_IN_NAME.fullmatch(path.stem):
        errors.append(f"filename should match Case ID pattern: {path.name}")
    name = manifest.get("name")
    if not isinstance(name, str) or not name.startswith(path.stem + " "):
        errors.append("name should start with Case ID and a space")
    tags = manifest.get("tags")
    if not isinstance(tags, list) or not tags:
        errors.append("tags must be a non-empty list")
    test = manifest.get("test")
    if not isinstance(test, str) or not re.fullmatch(r"executors/(?:api|web)/tests/[A-Za-z0-9_/-]+\.py::test_[A-Za-z0-9_]+", test) or not test.startswith(f"executors/{manifest['executor']}/"):
        errors.append("test must be an executor pytest node")
    elif not (Path(__file__).resolve().parents[3] / test.split("::", 1)[0]).is_file():
        errors.append(f"test file does not exist: {test}")
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate-flow.py <flow.yaml> [flow2.yaml ...]", file=sys.stderr)
        return 2

    failed = False
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"ERROR: not a file: {path}")
            failed = True
            continue
        print(f"Checking: {path}")
        errs = validate_flow(path)
        if errs:
            failed = True
            for e in errs:
                print(f"  ERROR: {e}")
        else:
            print("  OK")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

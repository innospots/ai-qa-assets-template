"""Case/Flow 映射的关键失败路径。"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_missing_flow_directory_is_reported(tmp_path: Path) -> None:
    cases = tmp_path / "cases" / "catalog"
    cases.mkdir(parents=True)
    (cases / "read.case.md").write_text(
        """---
id: CATALOG-READ
name: Read
module: catalog
priority: P1
tags: [catalog]
platform: [api]
---
## 正向测试
### TC-CATALOG-READ-001 Read
## 反向测试
""",
        encoding="utf-8",
    )
    flow_root = tmp_path / "flows"
    flow_root.mkdir()
    result = subprocess.run(
        ["bash", str(ROOT / "scripts" / "validate-cases.sh")],
        env={**os.environ, "CASE_DIR": str(tmp_path / "cases"), "FLOW_DIR": str(flow_root)},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert "missing Flow" in result.stdout


def test_flow_validator_accepts_all_formal_platforms() -> None:
    validator = ROOT / "skills" / "test-flow" / "scripts" / "validate-flow.py"
    flow_paths = [
        ROOT / "flows" / "api" / "health" / "TC-API-HEALTH-001.yaml",
        ROOT / "flows" / "web" / "home" / "TC-WEB-HOME-001.yaml",
        ROOT / "flows" / "mobile" / "demo" / "TC-MOBILE-DEMO-001.yaml",
    ]
    result = subprocess.run(
        [os.sys.executable, str(validator), *(str(p) for p in flow_paths)],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_api_discovery_uses_executor_not_domain_directory(tmp_path: Path) -> None:
    flow = tmp_path / "flows" / "catalog" / "read" / "TC-CATALOG-READ-001.yaml"
    flow.parent.mkdir(parents=True)
    flow.write_text(
        "executor: api\nname: TC-CATALOG-READ-001 Read\ntags: [catalog, smoke, positive, p1]\n"
        "test: executors/api/tests/test_read.py::test_tc_catalog_read_001\n",
        encoding="utf-8",
    )
    test_file = tmp_path / "executors" / "api" / "tests" / "test_read.py"
    test_file.parent.mkdir(parents=True)
    test_file.write_text("def test_tc_catalog_read_001():\n    assert True\n", encoding="utf-8")
    discovery = ROOT / "scripts" / "lib" / "discover_flow_tests.py"
    result = subprocess.run(
        [os.sys.executable, str(discovery), "api", "smoke", "--root", str(tmp_path)],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "test_tc_catalog_read_001" in result.stdout

    resolver = ROOT / "scripts" / "lib" / "resolve_flow_test.py"
    resolved = subprocess.run(
        [os.sys.executable, str(resolver), "api", str(flow), "--root", str(tmp_path)],
        text=True, capture_output=True, check=False,
    )
    assert resolved.returncode == 0, resolved.stderr
    assert resolved.stdout.strip() == "executors/api/tests/test_read.py::test_tc_catalog_read_001"

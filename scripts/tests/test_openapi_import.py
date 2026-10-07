"""OpenAPI 草稿导入的离线契约测试。"""

from __future__ import annotations

import json
import ast
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "scripts" / "openapi" / "import.py"


def run_import(tmp_path: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    spec = tmp_path / "api.yaml"
    spec.write_text(
        """openapi: 3.0.3
info:
  title: Catalog API
  version: '1.0'
paths:
  /items/{itemId}:
    parameters:
      - name: itemId
        in: path
        required: true
        schema: {type: string}
    get:
      operationId: getItem
      responses:
        '200':
          description: Found
          content:
            application/json:
              schema:
                type: object
                properties:
                  id: {type: string}
    delete:
      responses:
        '204': {description: Deleted}
""",
        encoding="utf-8",
    )
    return subprocess.run(
        [sys.executable, str(COMMAND), "--spec", str(spec), "--domain", "catalog", "--output", str(tmp_path / "drafts"), *extra],
        text=True,
        capture_output=True,
        check=False,
    )


def test_selected_operation_creates_review_bundle(tmp_path: Path) -> None:
    result = run_import(tmp_path, "--operation", "GET /items/{itemId}")
    assert result.returncode == 0, result.stderr
    bundles = list((tmp_path / "drafts" / "catalog").iterdir())
    assert len(bundles) == 1
    bundle = bundles[0]
    assert (bundle / "designs" / "catalog" / "index.md").is_file()
    assert len(list((bundle / "cases" / "catalog").glob("*.case.md"))) == 1
    flow = next((bundle / "flows" / "catalog").rglob("*.yaml"))
    assert "executor: api" in flow.read_text()
    assert "test:" in flow.read_text()
    assert "待确认" in next((bundle / "cases" / "catalog").glob("*.case.md")).read_text()
    contract = json.loads((bundle / "resources" / "operation.json").read_text())
    assert contract["method"] == "GET"
    assert contract["path"] == "/items/{itemId}"
    assert "200" in contract["operation"]["responses"]
    assert "pytest.skip" in next((bundle / "executors" / "api" / "tests").glob("*.py")).read_text()
    ast.parse(next((bundle / "executors" / "api" / "tests").glob("*.py")).read_text())


def test_all_is_explicit_and_existing_bundle_is_preserved(tmp_path: Path) -> None:
    first = run_import(tmp_path, "--all")
    assert first.returncode == 0, first.stderr
    assert len(list((tmp_path / "drafts" / "catalog").iterdir())) == 2
    second = run_import(tmp_path, "--all")
    assert second.returncode != 0
    assert "已存在" in second.stderr


def test_requires_explicit_selection(tmp_path: Path) -> None:
    result = run_import(tmp_path)
    assert result.returncode != 0
    assert "--operation" in result.stderr or "--all" in result.stderr


def test_rejects_unknown_operation(tmp_path: Path) -> None:
    result = run_import(tmp_path, "--operation", "PATCH /missing")
    assert result.returncode != 0
    assert "不存在" in result.stderr


def test_lists_json_openapi_31_without_creating_assets(tmp_path: Path) -> None:
    spec = tmp_path / "api.json"
    spec.write_text(json.dumps({
        "openapi": "3.1.0", "info": {"title": "Catalog", "version": "1"},
        "paths": {"/items": {"get": {"responses": {"200": {"description": "OK"}}}}},
    }), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(COMMAND), "--spec", str(spec), "--list", "--output", str(tmp_path / "drafts")],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "GET /items"
    assert not (tmp_path / "drafts").exists()

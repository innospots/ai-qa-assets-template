# Scripts：校验与执行入口

| 文件 | 用途 |
| --- | --- |
| `validate-cases.sh` | Case 元数据、章节、ID 与 Flow 映射 |
| `openapi/import.py` | 本地 OpenAPI 3.x → 按接口生成待审查 API 资产包 |
| `run-smoke.sh` | 默认 **API + Web** Smoke |
| `run-smoke-mobile.sh` | Maestro Mobile Smoke |
| `run-regression.sh` / `run-all.sh` | Maestro 套件（移动端） |
| `api/run-suite.sh` | pytest API 套件 |
| `api/run-flow.sh` | API 单 Flow |
| `web/run-suite.sh` | Playwright Web 套件 |
| `web/run-flow.sh` | Web 单 Flow |
| `maestro/*` | 移动端 Flow 执行 |
| `tests/test-executor-scripts.sh` | API/Web 发现脚本契约 |
| `tests/test-maestro-scripts.sh` | Maestro 脚本契约（伪 CLI） |
| `tests/test_openapi_import.py`、`tests/test_asset_validation.py` | 离线导入与追溯校验 |

## 日常检查

```bash
source .venv/bin/activate
./scripts/validate-cases.sh
bash -n scripts/*.sh scripts/api/*.sh scripts/web/*.sh scripts/lib/*.sh scripts/maestro/*.sh scripts/tests/*.sh
bash scripts/tests/test-executor-scripts.sh
bash scripts/tests/test-maestro-scripts.sh
python3 -m pytest -q scripts/tests/test_openapi_import.py scripts/tests/test_asset_validation.py
```

## OpenAPI 草稿导入

```bash
python3 scripts/openapi/import.py --spec skills/test-openapi-import/examples/catalog.openapi.yaml --list
python3 scripts/openapi/import.py --spec skills/test-openapi-import/examples/catalog.openapi.yaml --domain catalog --operation 'GET /items/{itemId}'
```

输出到 `generated/openapi-drafts/`；详细审核门槛见 [`test:openapi-import`](../skills/test-openapi-import/SKILL.md)。

## Smoke

```bash
./scripts/run-smoke.sh
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke-mobile.sh
```

生成 Case/Flow 请使用 `skills/` 中的 `test:design`、`test:case`、`test:flow`，不要用一次性生成脚本。

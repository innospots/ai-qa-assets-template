# 自动化测试资产模板

中性、可复制的测试资产工程：**Case 为唯一事实源**；执行实现可替换。默认以 **API（pytest + httpx）** 与 **Web（pytest-playwright）** 为主，**Android/iOS（Maestro）** 为辅。

## 1. 主链路

```text
需求 / 验收标准
      ↓
   Design（TDS）
      ↓
    Case ──→ Flow ──→ 执行层 ──→ Artifact
  │              ↑
  └─→ 文档    data + env
```

| 层级 | 示范目录 | 执行器 |
| --- | --- | --- |
| API | `flows/api/` + `executors/api/` | pytest |
| Web | `flows/web/` + `executors/web/` | Playwright |
| Mobile | `flows/mobile/` + `modules/` | Maestro |

Flow 文件职责因平台而异：API/Web 的 YAML 为 **清单**（`executor`、`tags`、`test` 节点）；Mobile 的 YAML 为 **Maestro DSL**。
目录名表示业务域；示范目录暂以平台命名。产品工程可使用 `catalog` 等业务目录，API/Web 执行器按清单中的 `executor` 字段发现 Flow。

## 2. 目录结构

```text
ai-qa-assets-template/
├── AGENTS.md
├── README.md
├── docs/FORK-CHECKLIST.md    从模板创建产品仓的检查清单
├── config.yaml               域、Tag、执行器入口
├── cases/                    Case 源定义（示范：api / web / mobile）
├── designs/                  TDS
├── flows/                    与 Case ID 1:1 的执行映射
├── executors/                API/Web pytest 实现
├── modules/                  Mobile 可复用 Maestro 步骤
├── data/                     业务数据与选择器（JS Object）
├── env/                      环境与敏感值模板（*.env.example）
├── skills/                   test:design / case / flow / execution …
├── scripts/                  校验与套件入口
├── python_runner/            Maestro 编排与汇总报告
├── artifacts/                运行产物（不提交）
└── generated/                派生文档（不提交）
```

## 3. 快速开始：从接口规范到可运行测试

### 3.1 依赖

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
playwright install chromium   # Web 测试需要
```

### 3.2 选择接口并生成待审查草稿（无需网络）

```bash
python3 scripts/openapi/import.py --spec skills/test-openapi-import/examples/catalog.openapi.yaml --list
python3 scripts/openapi/import.py --spec skills/test-openapi-import/examples/catalog.openapi.yaml --domain catalog --operation 'GET /items/{itemId}'
```

命令在 `generated/openapi-drafts/catalog/` 创建 TDS、Case、API Flow 清单、data、env 模板、接口契约快照和 pytest 骨架。使用 `--all` 才会批量处理全部接口；已有草稿不会被覆盖。OpenAPI 只提供接口契约，**生成的 Case 预期须按需求确认，pytest 骨架默认跳过**。详见 [`test:openapi-import`](skills/test-openapi-import/SKILL.md)。

审核后按 `test:design` → `test:case` → `test:flow` 将资产写入正式目录，完成断言并去掉跳过标记。若没有 OpenAPI 文件，可直接从需求开始同一链路。API/Web 的 Flow 是 pytest 节点清单；Mobile Flow 是 Maestro YAML。

### 3.3 结构校验（无需外网）

```bash
./scripts/validate-cases.sh
bash -n scripts/*.sh scripts/api/*.sh scripts/web/*.sh scripts/lib/*.sh scripts/maestro/*.sh scripts/tests/*.sh
bash scripts/tests/test-executor-scripts.sh
bash scripts/tests/test-maestro-scripts.sh
.venv/bin/python -m pytest -q scripts/tests/test_openapi_import.py scripts/tests/test_asset_validation.py
find data -name '*.js' -type f -exec node --check {} \;
```

### 3.4 Smoke（API + Web，需网络）

```bash
cp env/api.env.example env/api.env    # 按需修改 API_BASE_URL
cp env/web.env.example env/web.env
./scripts/run-smoke.sh
```

### 3.5 Mobile Smoke（可选）

```bash
cp env/android.env.example env/android.env
./scripts/maestro/preflight.sh android env/android.env
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke-mobile.sh
```

## 4. 从模板创建产品工程

见 [`docs/FORK-CHECKLIST.md`](docs/FORK-CHECKLIST.md)：重命名、替换 `config.yaml` 域列表、审核并替换示范资产、配置 CI Secret 与 env 文件。`journeys/`、`fixtures/` 可按业务需要启用；`generated/`、`artifacts/` 是派生目录。

## 5. AI Agent

修改资产前阅读 [`AGENTS.md`](AGENTS.md) 与 [`skills/README.md`](skills/README.md)。设计 → Case → Flow 的顺序不可跳过。

## 6. 常用命令

| 目标 | 命令 |
| --- | --- |
| 校验 Case/Flow | `./scripts/validate-cases.sh` |
| API 单 Flow | `./scripts/api/run-flow.sh flows/api/health/TC-API-HEALTH-001.yaml env/api.env` |
| API 套件 | `./scripts/api/run-suite.sh regression env/api.env` |
| Web 单 Flow | `./scripts/web/run-flow.sh flows/web/home/TC-WEB-HOME-001.yaml env/web.env` |
| Web 套件 | `./scripts/web/run-suite.sh regression env/web.env` |
| 默认 Smoke | `./scripts/run-smoke.sh` |
| Mobile Smoke | `MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke-mobile.sh` |
| 单条 Maestro Flow | `./scripts/maestro/run-flow.sh android flows/mobile/demo/TC-MOBILE-DEMO-001.yaml env/android.env` |

规范索引：[`docs/README.md`](docs/README.md)。

# 本仓库 Flow 约定

## 路径与追溯

`cases/{domain}/{scene}.case.md` 中每个 `TC-` 对应 `flows/{domain}/{scene}/{case-id}.yaml`。业务变化先更新 TDS 和 Case；仅执行实现变化可只改 Flow、Module、data 或 executor。

`{domain}` 是业务域，不是执行器名称。示范目录恰好使用 `api`、`web`、`mobile`；产品工程可使用 `catalog` 等真实业务域。API/Web 套件跨 `flows/` 扫描，并按清单的 `executor` 字段选择节点。

| 平台 | Flow 内容 | 执行位置 | 可运行例子 |
| --- | --- | --- | --- |
| API | `executor: api`、`name`、`tags`、`test` 清单 | `executors/api/tests/` pytest + httpx | `flows/api/health/TC-API-HEALTH-001.yaml` |
| Web | `executor: web`、`name`、`tags`、`test` 清单 | `executors/web/tests/` pytest-playwright | `flows/web/home/TC-WEB-HOME-001.yaml` |
| Mobile | Maestro YAML，配置区 + `---` + 命令 | `flows/mobile/` + `modules/` | `flows/mobile/demo/TC-MOBILE-DEMO-001.yaml` |

API/Web 清单的 `test` 应是仓库内可发现的 `path.py::test_name`，不能把 pytest 语法写进 Case。Mobile 的 `runScript` 从 Flow 相对路径加载 `data/{domain}/*.js`，`${output.<domain>...}` 层级须与脚本写入一致。环境地址和敏感值从 env/CI 提供。

## 共享资产

修改 `modules/` 或 `data/` 前，用 `rg` 查全部引用者；修改后至少验证直接引用的 Flow。`journeys/` 仅用于跨功能目标，不代替单 Case 的 Flow。

## 草稿边界

`generated/openapi-drafts/` 中的 API Flow 是待审查清单，pytest 骨架会跳过。只有 TDS/Case 业务预期确认、执行器断言完成且正式资产校验通过后，才可移入 `flows/`。

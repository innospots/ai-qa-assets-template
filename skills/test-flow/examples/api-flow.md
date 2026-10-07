# API Flow：健康检查

正式资产链路：`designs/api/health.design.md` 的 `DS-API-HEALTH-001` → `cases/api/health.case.md` 的 `TC-API-HEALTH-001` → `flows/api/health/TC-API-HEALTH-001.yaml` → `executors/api/tests/test_health.py::test_tc_api_health_001`。

Flow 清单只做映射，状态与响应体判断在 pytest 节点。单 Flow 执行：

```bash
source .venv/bin/activate
./scripts/api/run-flow.sh flows/api/health/TC-API-HEALTH-001.yaml env/api.env
```

需先设置 `API_BASE_URL`；未配置时该示范节点会跳过。

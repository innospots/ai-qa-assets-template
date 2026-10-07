# API 资产审查示例

审查范围：`designs/api/health.design.md`、`cases/api/health.case.md`、`flows/api/health/`、`executors/api/tests/test_health.py`。

| 检查项 | 证据 | 结论 |
| --- | --- | --- |
| DS → TC | TDS 中 `DS-API-HEALTH-001`；Case 中 `TC-API-HEALTH-001` 的追溯字段 | 已建立 |
| TC → Flow | `flows/api/health/TC-API-HEALTH-001.yaml` | 已建立 |
| Flow → 执行节点 | 清单 `test:` 指向 `test_health.py::test_tc_api_health_001` | 已建立 |
| 环境路径 | Case 声明 `probePath`；env 模板声明 `API_PROBE_PATH`；pytest 读取该变量 | 已对齐 |

问题记录应写明严重程度、影响与建议。例如：P2，若产品工程复制模板后仍沿用公共 echo 服务地址，则测试无法验证该产品接口；建议先替换 `API_BASE_URL` 与路径，再运行两条 Health Flow。此结论是静态审查，不代表已运行接口测试。

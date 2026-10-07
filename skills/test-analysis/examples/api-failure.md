# API 失败分析示例

以下是报告格式示例，数值为假设，不代表仓库实际运行结果。

| 字段 | 内容 |
| --- | --- |
| Case/Flow | `TC-API-HEALTH-001` / `flows/api/health/TC-API-HEALTH-001.yaml` |
| 预期 | Case 要求 2xx 且响应体非空 |
| 观察 | 假设 JUnit 显示连接超时，未收到 HTTP 响应 |
| 证据 | 对应运行的 JUnit 与 pytest 日志路径，需在真实分析中填写 |
| 分类 | 暂定环境/网络问题；证据不足时写 Unknown |
| 推断 | 可能是测试环境不可达；这是推断，不是产品缺陷结论 |
| 下一步 | 核对 `API_BASE_URL` 配置和网络连通性，再运行该单条 pytest 节点 |

先记录实际事实，再归因；不能因为超时而修改 Case 的 2xx 预期。

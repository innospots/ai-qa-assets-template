# 执行摘要示例

| 项目 | 值 |
| --- | --- |
| Case | `TC-API-HEALTH-001` |
| Flow | `flows/api/health/TC-API-HEALTH-001.yaml` |
| 命令 | `./scripts/api/run-flow.sh flows/api/health/TC-API-HEALTH-001.yaml env/api.env` |
| 环境 | `env/api.env`，仅记录文件名 |
| 结果 | 按实际运行填写通过/失败/跳过和退出码 |
| 证据 | 相应 `artifacts/api/` 下的 JUnit 与 pytest 日志路径 |

Web 与 Mobile 使用同一摘要字段；不能运行时在“结果”写未执行及具体原因，不填“通过”。

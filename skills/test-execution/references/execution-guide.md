# 测试执行指南

执行前确认 Flow 属于正式 `flows/`、对应 env 文件已准备、运行目标可访问。草稿目录 `generated/openapi-drafts/` 不参加正式套件。

| 平台 | 单 Flow | 套件 |
| --- | --- | --- |
| API | `./scripts/api/run-flow.sh flows/api/health/TC-API-HEALTH-001.yaml env/api.env` | `./scripts/api/run-suite.sh smoke env/api.env` |
| Web | `./scripts/web/run-flow.sh flows/web/home/TC-WEB-HOME-001.yaml env/web.env` | `./scripts/web/run-suite.sh smoke env/web.env` |
| Mobile | `./scripts/maestro/run-flow.sh android flows/mobile/demo/TC-MOBILE-DEMO-001.yaml env/android.env` | `./scripts/maestro/run-suite.sh android smoke env/android.env` |

API/Web 先安装 `requirements-dev.txt`；Web 还需 `playwright install chromium`。Mobile 先运行 `./scripts/maestro/preflight.sh android env/android.env` 并确认设备与 Maestro CLI。跨 API/Web 的默认 Smoke 为 `./scripts/run-smoke.sh`。

记录命令、目标、环境文件名、退出码、通过/失败/跳过数及 Artifact 路径。缺设备、CLI 或真实环境时，不得称测试通过；报告未执行原因和用户可运行的准确命令。日志、报告不得含密码、Token 或真实个人数据。

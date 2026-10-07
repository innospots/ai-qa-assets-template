# Maestro Python Runner

由 `scripts/maestro/*.sh` 调用的编排层：跨 `flows/`、`journeys/` 发现 Mobile Maestro 用例，跳过 API/Web 清单 → 执行 Maestro → 校验 → 写入 `artifacts/maestro/` 汇总报告。

API/Web 测试不经过本目录，见 `executors/` 与 `scripts/api`、`scripts/web`。

## 安装

```bash
cd python_runner
pip install -r requirements.txt
```

## 配置

编辑 `python_runner/config.yaml` 中的 `app_id` 与工具路径；敏感值仍只来自 `env/*.env`。

## 日常入口

```bash
./scripts/maestro/run-flow.sh android flows/mobile/demo/TC-MOBILE-DEMO-001.yaml env/android.env HTML
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke-mobile.sh
```

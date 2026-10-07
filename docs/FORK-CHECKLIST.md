# 从模板创建产品测试工程

复制本仓库（或 GitHub Template）后，按顺序完成下列项。模板与任何具体产品仓库无绑定关系。

## 仓库与命名

- [ ] 修改 README 标题与产品说明
- [ ] 在 `config.yaml` 的 `tags.domains` 中写入业务域（可删除示范域 `api`/`web`/`mobile` 或保留作参考）
- [ ] 确认 Case ID 规则仍为 `TC-{DOMAIN}-{FEATURE}-{NUMBER}`，与 CI 及缺陷系统一致

## 环境与密钥

- [ ] 复制 `env/*.env.example` 为本地 `env/*.env`（已 gitignore）
- [ ] 在 CI 中注入 `API_BASE_URL`、`WEB_BASE_URL`、`APP_ID` 等，勿提交真实密码/Token
- [ ] Web：在 CI 镜像中执行 `playwright install --with-deps chromium`

## 资产

- [ ] 如有 OpenAPI 文档，使用 `python3 scripts/openapi/import.py --spec <file> --list` 选择接口，再用 `--domain <domain> --operation 'METHOD /path'` 生成草稿；对照需求审核后才落正式资产
- [ ] 删除或替换 `cases/{api,web,mobile}/` 示范 Case
- [ ] 同步删除/替换 `designs/`、`flows/`、`executors/`、`data/` 中对应示范文件
- [ ] 新建业务域目录，例如 `cases/billing/`、`cases/auth/`
- [ ] 为每个 Case ID 维护唯一 Flow 映射文件
- [ ] 草稿进入正式目录前确认业务断言，并移除 pytest 骨架中的跳过标记

## 执行器

- [ ] API：在 `executors/api/tests/` 增加 pytest，并在 Flow 清单中填写 `test:` 节点
- [ ] Web：在 `executors/web/tests/` 增加 Playwright 用例
- [ ] Mobile：在 `flows/` + `modules/` 编写 Maestro YAML；按需调整 `python_runner/config.yaml`

## 验证

- [ ] `./scripts/validate-cases.sh`
- [ ] `bash scripts/tests/test-executor-scripts.sh`
- [ ] `.venv/bin/python -m pytest -q scripts/tests/test_openapi_import.py scripts/tests/test_asset_validation.py`
- [ ] `./scripts/run-smoke.sh`（或 CI 等价步骤）
- [ ] 按需运行 Mobile 预检与 Smoke

## 文档与 Agent

- [ ] 更新 `docs/` 中与产品相关的示例路径
- [ ] 确认 `AGENTS.md` 与团队 Review 规则一致

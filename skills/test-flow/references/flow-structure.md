# Flow 结构

## API 与 Web

Flow 是执行清单，不写操作步骤或断言 DSL：

```yaml
executor: api
name: TC-API-HEALTH-001 GET 探测返回 2xx
tags: [api, smoke, regression, positive, p0]
test: executors/api/tests/test_health.py::test_tc_api_health_001
```

`executor` 与清单所在平台一致，`name` 以 Case ID 开头，`test` 指向唯一 pytest 节点。实际请求、页面动作、断言、清理写在 executor 测试中。测试节点应可独立运行并在失败时留下 Case ID 与诊断信息。

## Mobile

Mobile Flow 是 Maestro YAML：`appId`、`name`、`tags` 配置区，`---` 后为命令。每个关键 Case 预期需要等价 `assertVisible`、`assertNotVisible` 等判断；数据通过 `runScript` 和 `${output...}` 加载。具体命令、控制流与选择器见本目录的 Maestro 专项指南。

```yaml
appId: ${APP_ID}
name: TC-MOBILE-DEMO-001 启动应用后首页可见
tags: [mobile, smoke, regression, positive, p0]
---
- launchApp
- assertVisible: "首页"
```

以上是结构示意；实际文案和选择器须来自已确认 Case 与当前应用 data。

## 共同约束

- 一 Case ID 对应一正式 Flow，文件名和 ID 完全一致。
- Tag 与 Case 执行范围一致；`smoke` 只给稳定的关键路径。
- 不依赖其他 Case 的运行副作用；准备、断言和必要清理可独立完成。
- 不提交真实环境地址、凭据和个人信息。

# Data Binding Guide

## 1. 目的

规范 Test Data、运行参数、Flow 常量、Subflow 参数与 JavaScript 运行数据的职责边界。

## 2. 官方依据

- Parameters and constants  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/parameters-and-constants
- Nested flows  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/nested-flows
- Manage data and states  
  https://docs.maestro.dev/maestro-flows/javascript/manage-data-and-states
- Run and debug JavaScript  
  https://docs.maestro.dev/maestro-flows/javascript/run-and-debug-javascript

## 3. 数据分层

```text
Test Data File
    │
    │ 业务输入 / Expected Data
    ▼
Execution Parameters
    │
    │ 注入
    ▼
Flow Variables
    │
    ├── Subflow env
    │
    └── JavaScript
           │
           ▼
        output.*
```

## 4. 数据职责

| 数据类型 | 应放位置 |
|---|---|
| 用户名、商品号、案件号等业务测试数据 | 独立 Test Data |
| 密码、Token、API Secret | 外部安全环境变量/Secret |
| 环境 URL、租户、运行环境 | 执行参数 |
| Flow 内稳定常量 | Header `env` |
| Subflow 调用参数 | `runFlow.env` |
| Script 计算结果 | `output.<namespace>` |
| UI 捕获文字 | `maestro.copiedText` |

## 5. 变量引用

Maestro 使用：

```yaml
${VARIABLE_NAME}
```

变量名称大小写敏感。

CLI 参数传入时通常是字符串；数字/布尔类型如需要业务计算，应在 JavaScript 中显式转换。

## 6. Flow 中禁止硬编码业务测试数据

错误：

```yaml
- inputText: "user001"
- inputText: "Password123!"
```

推荐：

```yaml
- inputText: ${USERNAME}
- inputText: ${PASSWORD}
```

固定 UI 文案不是“测试数据”，可以直接写：

```yaml
- tapOn: "Login"
```

## 7. `env` 使用

适合 Flow 内固定常量：

```yaml
appId: com.example.app
env:
  DEFAULT_ROLE: "customer"
---
```

不要把生产密码或真实用户信息写入 `env` 并提交 Git。

## 8. Subflow 参数

```yaml
- runFlow:
    file: common/login.yaml
    env:
      USERNAME: ${LOGIN_USERNAME}
      PASSWORD: ${LOGIN_PASSWORD}
```

Subflow：

```yaml
- tapOn: "Username"
- inputText: ${USERNAME}
- tapOn: "Password"
- inputText: ${PASSWORD}
```

Subflow 应声明清楚所需参数；不要隐式依赖父 Flow 中大量全局变量。

## 9. `output` 规范

`output` 是 Flow 执行过程中的全局 JavaScript 状态。

禁止直接堆积：

```javascript
output.id = ...
output.value = ...
output.result = ...
```

推荐 namespace：

```javascript
output.order = {
  id: data.id,
  status: data.status
};
```

Flow 中：

```yaml
- assertVisible: ${output.order.id}
```

建议 namespace 按功能/脚本命名：

```text
output.auth.*
output.order.*
output.profile.*
output.fixture.*
```

## 10. UI → Script 数据

使用 `copyTextFrom` 获取 UI 文本后，可通过：

```text
maestro.copiedText
```

访问。

适合：

- 动态订单号；
- 页面生成 ID；
- 需要后续 API 校验的 UI 值。

如果需要保存多个值，应立即复制到自己的 `output` namespace，避免后续 `copyTextFrom` 覆盖。

## 11. 默认值

Subflow 可对可选参数设置合理默认值：

```yaml
env:
  USER_ROLE: ${USER_ROLE || "customer"}
```

但对测试结论有影响的关键输入，不应静默降级成默认值；缺失时应该尽早失败。

## 12. 与本仓库 `data/` 的关系

本仓库业务数据在 `data/{domain}/*.js`（**非**独立 JSON 文件），由 Flow 通过 `runScript` 加载：

```yaml
- runScript: ../../../data/web/locales.js
- runScript: ../../../data/auth/users.js
```

```javascript
output.auth = output.auth || {};
output.auth.users = {
  normal: { username: '...', password: TEST_ADMIN_PASSWORD }
};
```

Flow 引用：

```yaml
${output.auth.users.normal.username}
${output.customer.customers.validFull.code}
```

由 `test:case` / `test-data` 维护 data 脚本；`test:flow` **只引用**，不重新定义业务值。

敏感值经 env/CI Secret 注入 data 脚本，禁止写入 Flow YAML 或提交 Git。

详见 [repo-conventions.md](repo-conventions.md) 与 [`../../../data/README.md`](../../../data/README.md)。

## 13. Review Checklist

- [ ] 业务数据和 Flow 分离
- [ ] Secret 未进入 Git
- [ ] 参数名称明确
- [ ] Subflow 参数显式
- [ ] `output` 使用 namespace
- [ ] 没有依赖未定义变量
- [ ] 关键输入缺失不会被不合理默认值掩盖

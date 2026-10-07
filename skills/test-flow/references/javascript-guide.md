# JavaScript Guide

## 1. 目的

定义 Flow 中 JavaScript 的使用边界，防止声明式测试被演变为难维护的脚本程序。

## 2. 官方依据

- JavaScript overview  
  https://docs.maestro.dev/maestro-flows/javascript/javascript-overview
- Run and debug JavaScript  
  https://docs.maestro.dev/maestro-flows/javascript/run-and-debug-javascript
- Manage data and states  
  https://docs.maestro.dev/maestro-flows/javascript/manage-data-and-states
- Make HTTP requests  
  https://docs.maestro.dev/maestro-flows/javascript/make-http-requests
- Generate synthetic data  
  https://docs.maestro.dev/maestro-flows/javascript/generate-synthetic-data
- `runScript`  
  https://docs.maestro.dev/reference/commands-available/runscript

## 3. 总原则

```text
能用 YAML 清晰表达
    ↓ 是
使用 YAML
    ↓ 否
简单表达式？
    ↓ 是
${...} / evalScript
    ↓ 否
独立 runScript
```

JavaScript 是扩展机制，不是默认 Flow 编写方式。

## 4. 可使用 JavaScript 的场景

推荐：

- 日期/时间计算；
- 字符串转换；
- 数字计算；
- 唯一随机测试值；
- JSON 处理；
- HTTP API setup / verify；
- 复杂但必要的条件表达式；
- UI 捕获值后的二次加工。

不推荐：

- 用 JS 编写主要 UI 点击流程；
- 把大量业务步骤写进 `.js`；
- 仅为了避免 YAML Selector；
- 用 JS 吞掉异常或把失败改成成功。

## 5. 三种执行方式

### Inline expression

```yaml
- inputText: ${'user_' + faker.name().firstName()}
```

适合简单表达式。

### `evalScript`

```yaml
- evalScript: ${output.order = {}}
```

适合单步状态设置或简单计算。

### `runScript`

```yaml
- runScript:
    file: ../../scripts/create-order.js
    env:
      API_BASE_URL: ${API_BASE_URL}
```

适合复杂、可复用逻辑。

Cloud 场景优先相对路径。

## 6. Sandbox 约束

JavaScript 在受限 Sandbox 中执行，不应假设：

- 可以访问任意本地文件；
- 可以 `npm install` 并使用 Node.js 包；
- 可以依赖本机私有运行环境。

脚本必须具有可移植性。

## 7. `output` 使用

推荐：

```javascript
output.fixture = {
  userId: user.id,
  email: user.email
};
```

避免：

```javascript
output.id = ...
output.name = ...
output.result = ...
```

namespace 可防止不同 Script 相互覆盖。

## 8. HTTP

适用于：

- 创建测试前置数据；
- 删除测试数据；
- 获取测试专用 Token；
- UI 操作后验证后端状态。

推荐模式：

```text
API setup
   ↓
UI action
   ↓
UI assertion
   ↓
必要时 API verify
```

HTTP 不应绕开 Test Case 原本明确要求验证的 UI 行为。

## 9. Synthetic Data

Faker 适合：

- 唯一用户名；
- 临时邮箱；
- 随机名称；
- 唯一字段冲突规避。

但回归用例需要可重放时，应把关键随机结果保存到 `output` 并进入日志/证据。

例如：

```yaml
- evalScript: ${output.user = {name: faker.name().firstName()}}
- inputText: ${output.user.name}
```

## 10. 日志

外部 `.js` 可使用 `console.log`。

日志不得输出：

- 密码；
- Access Token；
- 完整敏感个人数据。

即使 Flow 使用 label，仍不要假设底层 debug log 完全隐藏原始数据。

## 11. Script 文件规范

推荐：

```text
scripts/
├── fixtures/
│   ├── create-user.js
│   └── delete-user.js
├── assertions/
│   └── verify-order.js
└── utils/
    └── date-utils.js
```

脚本名表达能力，不表达步骤编号。

## 12. Review Checklist

- [ ] YAML 无法合理表达才使用 JS
- [ ] 复杂逻辑使用外部 Script
- [ ] `output` 已 namespace
- [ ] 不依赖 Node/npm 本地包
- [ ] HTTP 不绕过核心 UI 验证
- [ ] 随机数据可追踪
- [ ] 日志无 Secret

# Test Flow Best Practices

## 1. 目的

汇总 `test-flow` Skill 在生成和审查 Flow 时必须遵循的工程最佳实践。

## 2. 官方依据

- Maestro Flows overview  
  https://docs.maestro.dev/maestro-flows
- Flow control and logic  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/flow-control-and-logic-overview
- Selectors  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/how-to-use-selectors
- Nested flows  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/nested-flows
- Wait commands  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/wait-commands
- Conditions  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/conditions
- Workspace management  
  https://docs.maestro.dev/maestro-flows/workspace-management/workspace-management-overview
- Official suite structuring article  
  https://maestro.dev/blog/maestro-best-practices-structuring-your-test-suite

## 3. 一 Case 一 Main Flow

一个 Flow 应表达一个明确测试意图。

不要把：

```text
注册
登录
修改资料
下单
支付
退款
```

全部放进同一个超长 Flow，除非 Test Case 本身就是这一条完整 E2E 用户旅程。

在本项目中默认：

```text
1 Test Case = 1 Main Flow
```

## 4. Flow 可独立执行

每个 Main Flow 尽量可以：

```text
Reset Environment
     ↓
Setup Preconditions
     ↓
Execute Case
     ↓
Assert
     ↓
Cleanup
```

不要依赖另一个 Flow 的执行副作用。

## 5. Expected Result 必须可验证

每个关键 Expected Result 转换成明确 Assertion。

如果无法自动验证，应：

1. 明确原因；
2. 标记为当前自动化缺口；
3. 不得假装已经验证。

## 6. Selector 稳定优先

通常：

```text
stable text / id
   ↓
state + selector
   ↓
relational
   ↓
index
   ↓
coordinate
```

坐标是最后手段。

## 7. 数据与逻辑分离

业务数据：

```text
Test Data
```

Flow：

```text
行为逻辑 + 变量引用
```

Secret：

```text
Environment / Secret Store
```

## 8. DRY，但不要过度抽象

应该提取：

```text
login
logout
setup-user
navigate-to-order
```

不应该提取：

```text
click-button
input-text
step-1
```

## 9. 优先智能等待

正常页面变化：

```yaml
- assertVisible: "Success"
```

而不是人为大 Timeout。

只有确实长耗时才使用 `extendedWaitUntil`。

## 10. Condition 克制

Condition 是业务/平台分支，不是“容错器”。

关键步骤缺失应该失败。

## 11. Retry 克制

Retry 用于局部偶发问题，不应用于掩盖系统不稳定。

如果 `retry` 成为 Flow 的必要条件，应调查：

- Selector；
- 页面等待；
- 产品问题；
- 测试环境。

## 12. JavaScript 最小化

```text
YAML First
JS When Necessary
```

JS 负责数据、计算、API 和复杂逻辑，不负责主要 UI 流程。

## 13. Hook 快速且安全

Hook 每个 Flow 都会运行，因此：

- 不做大规模慢操作；
- 不递归；
- cleanup 应可重复执行；
- setup 必须失败可见。

## 14. 测试报告可追踪

至少写：

```yaml
properties:
  testCaseId: TC-XXX-001
```

CI 建议加稳定 JUnit ID。

## 15. 典型反模式

### Anti-pattern A：万能 Optional

```yaml
optional: true
```

到处出现，导致失败被忽略。

### Anti-pattern B：万能 Retry

每个按钮都重试，导致产品真实不稳定不可见。

### Anti-pattern C：坐标脚本

大量 `point`，一换设备/布局就失败。

### Anti-pattern D：超长 Flow

一个 Flow 同时验证多个 Test Case。

### Anti-pattern E：没有 Assertion

脚本只点击，不验证。

### Anti-pattern F：数据硬编码

账号、订单号直接写入 YAML。

### Anti-pattern G：JS 化

YAML 只剩多个 `runScript`。

### Anti-pattern H：顺序依赖

Flow B 必须等 Flow A 跑完才能运行。

## 16. Agent 生成完成检查

### Structure

- [ ] 一个 Main Flow 对应一个 Case
- [ ] Header 完整
- [ ] Case ID 可追踪

### Behavior

- [ ] Step 顺序符合 Test Case
- [ ] Expected Result 已转换成 Assertion

### Selector

- [ ] Selector 稳定
- [ ] 未滥用 index / point

### Data

- [ ] 业务数据外置
- [ ] Secret 未硬编码
- [ ] `output` 有 namespace

### Reuse

- [ ] 重复业务操作已合理提取
- [ ] Subflow 保持原子性

### Reliability

- [ ] 正常等待使用 Assertion
- [ ] Condition 不隐藏错误
- [ ] Retry 范围小
- [ ] Loop 有安全退出

### Maintainability

- [ ] Label 清楚
- [ ] JS 使用最小化
- [ ] Flow 可独立运行

# Control Flow Guide

## 1. 目的

规范 Condition、Loop、Wait、Retry、Optional 和 Hook 的使用，防止 Agent 为“提高通过率”而隐藏真实失败。

## 2. 官方依据

- Flow control and logic overview  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/flow-control-and-logic-overview
- Conditions  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/conditions
- Loops  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/loops
- Wait commands  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/wait-commands
- Hooks  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/hooks
- Labeling and error handling  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/labeling-and-error-handling
- `retry`  
  https://docs.maestro.dev/reference/commands-available/retry

## 3. Condition

支持典型条件：

```text
visible
notVisible
platform
true (JavaScript expression)
```

多个条件组合为 AND。

允许场景：

- Android / iOS / Web 差异；
- 合法 A/B 状态；
- 非关键、真实可选弹层；
- 已知的业务状态分支；
- 特性开关。

禁止：

- 用 `when.visible` 避免关键控件不存在时失败；
- 把关键业务步骤变成“有就执行，没有就算了”；
- 大量 Condition 把一个 Case 变成多个不同 Case。

如果两个路径的业务意图明显不同，应拆成不同 Test Case / Flow。

## 4. `optional`

适用于真正非关键步骤：

```yaml
- tapOn:
    text: "Dismiss"
    optional: true
    label: "Dismiss non-critical promotion if shown"
```

禁止对以下内容使用 `optional: true`：

- Case 核心业务动作；
- Expected Result Assertion；
- 数据保存/提交；
- 权限或认证必须成功的步骤。

## 5. Wait

### 首选 Assertions

目标出现：

```yaml
- assertVisible: "Success"
```

目标消失：

```yaml
- assertNotVisible:
    id: loading
```

标准 Assertion 自带自动等待能力，因此不要先人为等待再断言。

### 长耗时

确实超过普通 Assertion 等待窗口时：

```yaml
- extendedWaitUntil:
    visible: "Report ready"
    timeout: 30000
```

Timeout 应匹配产品合理 SLA，不应全部设置为极大值。

### 动画

```yaml
- waitForAnimationToEnd:
    timeout: 5000
```

仅在“元素已经存在但仍运动”的情况使用。

## 6. Loop

固定次数：

```yaml
- repeat:
    times: 3
    commands:
      - tapOn: "Add"
```

条件循环：

```yaml
- repeat:
    while:
      visible: "Load more"
    commands:
      - tapOn: "Load more"
```

推荐“安全循环”：

```yaml
- repeat:
    times: 10
    while:
      visible: "Load more"
    commands:
      - tapOn: "Load more"
```

所有动态循环必须有可证明的终止条件；优先同时使用最大次数作为安全边界。

## 7. Retry

Retry 用于局部、短暂且可恢复行为。

```yaml
- retry:
    maxRetries: 2
    commands:
      - tapOn:
          id: refresh_button
```

不得：

- Retry 整个 Flow；
- 用 Retry 掩盖 Selector 错误；
- 用 Retry 把 50% 成功率的产品行为变成测试“通过”。

## 8. Hooks

```yaml
onFlowStart:
  - runFlow: common/setup.yaml

onFlowComplete:
  - runFlow: common/cleanup.yaml
```

规则：

- Hook 必须短；
- Hook 失败应视为环境/测试失败；
- 防止 Hook → Flow → Hook 递归；
- `onFlowComplete` 用于恢复中性状态或清理测试数据。

## 9. 决策表

| 问题 | 首选 |
|---|---|
| 等待正常页面出现 | `assertVisible` |
| 等待 Loader 消失 | `assertNotVisible` |
| 长业务处理 | `extendedWaitUntil` |
| UI 仍在动画 | `waitForAnimationToEnd` |
| 可选弹层 | `when` / `optional` |
| 平台差异 | `when.platform` |
| 重复固定次数 | `repeat.times` |
| 重复直到状态变化 | `repeat.while` + 安全次数 |
| 短暂偶发失败 | 小范围 `retry` |
| 每个 Flow 都要准备 | Hook |

## 10. Review Checklist

- [ ] Condition 没有隐藏关键失败
- [ ] Optional 仅用于非关键步骤
- [ ] Loop 有停止条件
- [ ] Wait 没有替代正常 Assertion
- [ ] Timeout 合理
- [ ] Retry 范围足够小
- [ ] Hook 不递归

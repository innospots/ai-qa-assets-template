# Command Selection Guide

## 1. 目的

指导 `test-flow` Skill 根据 Test Case 的语义选择正确的 Maestro Command，并限制容易造成脆弱测试的用法。

## 2. 官方依据

- Commands available  
  https://docs.maestro.dev/reference/commands-available
- `tapOn`  
  https://docs.maestro.dev/reference/commands-available/tapon
- `launchApp`  
  https://docs.maestro.dev/reference/commands-available/launchapp
- `runFlow`  
  https://docs.maestro.dev/reference/commands-available/runflow
- `repeat`  
  https://docs.maestro.dev/reference/commands-available/repeat
- `retry`  
  https://docs.maestro.dev/reference/commands-available/retry
- `assertVisible`  
  https://docs.maestro.dev/reference/commands-available/assertvisible
- `assertNotVisible`  
  https://docs.maestro.dev/reference/commands-available/assertnotvisible
- `extendedWaitUntil`  
  https://docs.maestro.dev/reference/commands-available/extendedwaituntil

## 3. Command 分类

### 3.1 应用生命周期

```text
launchApp
stopApp
killApp
clearState
clearKeychain
```

生成规则：

- 普通启动：`launchApp`
- 测试要求全新安装态/首次进入：`launchApp.clearState: true`
- 仅恢复后台 App：根据测试意图使用 `stopApp: false`
- 不要默认清理状态；状态策略必须来自 Case 前置条件。

### 3.2 UI 操作

```text
tapOn
doubleTapOn
longPressOn
inputText
eraseText
pasteText
pressKey
hideKeyboard
back
openLink
swipe
scroll
scrollUntilVisible
```

优先使用元素 Selector，而不是坐标。

错误：

```yaml
- tapOn:
    point: "50%,72%"
```

推荐：

```yaml
- tapOn:
    id: login_button
    enabled: true
```

### 3.3 Assertions

```text
assertVisible
assertNotVisible
assertTrue
assertDarkMode
assertLightMode
assertScreenshot
assertWithAI
assertNoDefectsWithAI
```

规则：

1. Expected Result 可以通过 Accessibility Tree 明确验证时，优先普通 Assertion；
2. 状态型验证可以组合 `enabled`、`checked`、`focused`、`selected`；
3. AI Assertion 属于概率性能力，不应替换可以确定性验证的关键业务结果；
4. Main Flow 至少应验证 Test Case 的关键结果。

### 3.4 Flow 与控制逻辑

```text
runFlow
repeat
retry
evalScript
runScript
```

规则：

- 公共步骤 → `runFlow`
- 有明确重复语义 → `repeat`
- 短暂、不可预测但业务允许重试的动作 → `retry`
- 简单计算 → `evalScript`
- 复杂可复用逻辑 → `runScript`

### 3.5 等待

```text
assertVisible
assertNotVisible
extendedWaitUntil
waitForAnimationToEnd
```

选择顺序：

```text
预期元素出现/消失
    ↓
assertVisible / assertNotVisible
    ↓
确实超过默认等待窗口
    ↓
extendedWaitUntil
    ↓
纯动画稳定问题
    ↓
waitForAnimationToEnd
```

不要默认在步骤之间添加固定 Sleep 思维。

### 3.6 Device / Environment

```text
setPermissions
setAirplaneMode
toggleAirplaneMode
setDarkMode
toggleDarkMode
setLocation
setOrientation
travel
addMedia
setClipboard
```

这些命令只应在 Test Case 明确测试设备、权限、网络、时间、媒体或环境行为时使用。

### 3.7 获取与证据

```text
copyTextFrom
takeScreenshot
startRecording
stopRecording
extractTextWithAI
```

截图主要作为测试证据或调试辅助，不应替代 Assertion。

## 4. `tapOn` 生成规范

官方支持 text / id / selector map / point，并提供 `retryTapIfNoChange`。

推荐：

```yaml
- tapOn:
    id: submit_button
    enabled: true
```

只有 UI 已确认存在“早点击未响应”的特殊情况，才使用：

```yaml
- tapOn:
    id: submit_button
    retryTapIfNoChange: true
```

不要全局添加 `retryTapIfNoChange`。

## 5. `launchApp` 生成规范

可控制：

- `appId`
- `clearState`
- `clearKeychain`
- `stopApp`
- `permissions`
- `arguments`

测试隔离不等于每条用例都强制 `clearState: true`。应依据测试前置状态决定。

## 6. `retry` 使用规范

`retry` 只用于局部、可解释的短暂不稳定行为。

禁止：

```yaml
- retry:
    commands:
      # 几十个业务步骤
```

更禁止用它包裹整个 Flow。

使用 `retry` 前先判断：

1. 是否应该使用 Assertion 自动等待；
2. 是否 Selector 不稳定；
3. 是否产品本身存在真实故障；
4. 是否该行为在业务上真的允许重试。

## 7. 完整 Command 官方链接

### Assertions

- https://docs.maestro.dev/reference/commands-available/assertdarkmode
- https://docs.maestro.dev/reference/commands-available/assertlightmode
- https://docs.maestro.dev/reference/commands-available/assertnodefectswithai
- https://docs.maestro.dev/reference/commands-available/assertnotvisible
- https://docs.maestro.dev/reference/commands-available/assertscreenshot
- https://docs.maestro.dev/reference/commands-available/asserttrue
- https://docs.maestro.dev/reference/commands-available/assertvisible
- https://docs.maestro.dev/reference/commands-available/assertwithai

### App / UI

- https://docs.maestro.dev/reference/commands-available/back
- https://docs.maestro.dev/reference/commands-available/clearkeychain
- https://docs.maestro.dev/reference/commands-available/clearstate
- https://docs.maestro.dev/reference/commands-available/copytextfrom
- https://docs.maestro.dev/reference/commands-available/doubletapon
- https://docs.maestro.dev/reference/commands-available/erasetext
- https://docs.maestro.dev/reference/commands-available/hidekeyboard
- https://docs.maestro.dev/reference/commands-available/inputtext
- https://docs.maestro.dev/reference/commands-available/killapp
- https://docs.maestro.dev/reference/commands-available/launchapp
- https://docs.maestro.dev/reference/commands-available/longpresson
- https://docs.maestro.dev/reference/commands-available/openlink
- https://docs.maestro.dev/reference/commands-available/pastetext
- https://docs.maestro.dev/reference/commands-available/presskey
- https://docs.maestro.dev/reference/commands-available/scroll
- https://docs.maestro.dev/reference/commands-available/scrolluntilvisible
- https://docs.maestro.dev/reference/commands-available/swipe
- https://docs.maestro.dev/reference/commands-available/tapon

### Flow / Script / Timing

- https://docs.maestro.dev/reference/commands-available/evalscript
- https://docs.maestro.dev/reference/commands-available/extendedwaituntil
- https://docs.maestro.dev/reference/commands-available/repeat
- https://docs.maestro.dev/reference/commands-available/retry
- https://docs.maestro.dev/reference/commands-available/runflow
- https://docs.maestro.dev/reference/commands-available/runscript
- https://docs.maestro.dev/reference/commands-available/waitforanimationtoend

### Device / Environment / Artifacts

- https://docs.maestro.dev/reference/commands-available/addmedia
- https://docs.maestro.dev/reference/commands-available/setairplanemode
- https://docs.maestro.dev/reference/commands-available/setclipboard
- https://docs.maestro.dev/reference/commands-available/setdarkmode
- https://docs.maestro.dev/reference/commands-available/setlocation
- https://docs.maestro.dev/reference/commands-available/setorientation
- https://docs.maestro.dev/reference/commands-available/setpermissions
- https://docs.maestro.dev/reference/commands-available/startrecording
- https://docs.maestro.dev/reference/commands-available/stopapp
- https://docs.maestro.dev/reference/commands-available/stoprecording
- https://docs.maestro.dev/reference/commands-available/takeScreenshot
- https://docs.maestro.dev/reference/commands-available/toggleairplanemode
- https://docs.maestro.dev/reference/commands-available/toggledarkmode
- https://docs.maestro.dev/reference/commands-available/travel
- https://docs.maestro.dev/reference/commands-available/extracttextwithai

## 8. Command 选择检查

- [ ] Command 与 Test Case 语义一致
- [ ] 没有把 Screenshot 当 Assertion
- [ ] 没有滥用 Retry
- [ ] 没有不必要的 coordinate
- [ ] 没有不必要的 JavaScript
- [ ] 等待优先使用 Assertions

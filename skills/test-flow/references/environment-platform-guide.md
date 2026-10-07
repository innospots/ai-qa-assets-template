# Environment and Platform Guide

## 1. 目的

规范 Flow 在 Android、iOS、Web、权限、Locale、设备和测试状态方面的处理方式。

## 2. 官方依据

- Permissions  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/permissions
- Test in different locales  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/test-in-different-locales
- Locales supported by Maestro  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/test-in-different-locales/locales-supported-by-maestro
- Specify and start devices  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/specify-and-start-devices
- Detect Maestro  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/detect-maestro
- `launchApp`  
  https://docs.maestro.dev/reference/commands-available/launchapp

## 3. 平台分支

只有平台行为确实不同才生成：

```yaml
- runFlow:
    when:
      platform: Android
    file: common/android-permissions.yaml
```

不要因为 Selector 不稳定而建立 Android/iOS 两套完全相同的 Flow。

## 4. App 初始状态

状态来自 Test Case 前置条件。

### 干净状态

```yaml
- launchApp:
    clearState: true
```

### 保留登录状态

不要清状态；明确 setup 方式。

### 首次安装行为

需要同时考虑：

- state；
- permission；
- onboarding；
- keychain（iOS）。

## 5. Permissions

可以在 `launchApp` 时设置：

```yaml
- launchApp:
    permissions:
      all: deny
      camera: allow
```

也可以运行中修改：

```yaml
- setPermissions:
    permissions:
      notifications: allow
```

规则：

- 权限状态必须来自测试意图；
- 测试“用户拒绝权限”时不要默认 `all: allow`；
- Web 浏览器权限能力与 Mobile 不同，不可假设一致；
- 系统权限弹框属于测试目标时，不应通过 setup 隐藏。

## 6. Locale

Locale 属于设备级运行配置，不应由 Flow 自己通过 `launchApp` 或 `config.yaml` 伪造。

因此 Test Case 若指定 Locale：

```text
Case metadata
   ↓
Execution configuration
   ↓
device locale
   ↓
Flow
```

Flow 可以使用 Tag 标识：

```yaml
tags:
  - locale-fr
```

国际化 Flow 的 Selector 应优先采用稳定 ID，或明确使用当前 Locale 文案。

## 7. Device / Sharding

Flow 本身不要依赖某个固定设备 ID。

并行运行时：

- Flow 必须避免依赖其他 Flow 留下的状态；
- Screenshot 名称避免冲突；
- 可以使用内置 shard/device 变量区分输出。

## 8. Detect Test Runtime

官方推荐使用 `launchApp.arguments` 等显式方式传递测试标识，而不是依赖已废弃的端口检测方式。

测试标识可用于：

- 禁用 analytics；
- 指向测试环境；
- 使用测试型 2FA；
- 关闭不稳定自定义动画。

禁止利用 test mode 改变被测试核心业务结果。

## 9. Review Checklist

- [ ] 状态与 Case 前置条件一致
- [ ] Permission 没有被默认配置破坏测试意图
- [ ] Locale 交给执行环境
- [ ] 平台分支有真实必要性
- [ ] Test mode 没有绕过核心业务
- [ ] Flow 不绑定固定设备

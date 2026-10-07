# Subflow Guide

## 1. 目的

规范公共 Flow 的拆分、复用、参数传递和调用边界。

## 2. 官方依据

- Nested flows  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/nested-flows
- `runFlow`  
  https://docs.maestro.dev/reference/commands-available/runflow
- Hooks  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/hooks
- Sequential execution  
  https://docs.maestro.dev/maestro-flows/workspace-management/sequential-execution

## 3. 定义

### Main Flow

一个 Main Flow 表示一个独立 Test Case。

### Subflow

Subflow 是可复用的业务操作或环境准备能力，不代表独立测试结论。

示例：

```text
common/
├── login.yaml
├── logout.yaml
├── reset-session.yaml
├── navigate-to-orders.yaml
└── dismiss-permissions.yaml
```

## 4. 什么情况下提取 Subflow

同时满足较多以下条件时提取：

- 在多个 Main Flow 重复；
- 具有明确业务语义；
- 职责单一；
- 输入可以参数化；
- 修改时希望集中维护；
- 可以独立理解。

推荐：

```text
login
logout
create-test-user
navigate-to-profile
select-product
```

不推荐：

```text
tap-button
step-1
input-field
click-next
```

Subflow 不应退化成对单条 Command 的无意义包装。

## 5. 原子性

一个 Subflow 只完成一个明确任务。

推荐：

```text
login.yaml
logout.yaml
onboarding.yaml
```

不推荐：

```text
login-and-create-order-and-open-profile.yaml
```

## 6. 参数化

Main Flow：

```yaml
- runFlow:
    file: ../../common/login.yaml
    env:
      USERNAME: ${USERNAME}
      PASSWORD: ${PASSWORD}
```

Subflow：

```yaml
- tapOn: "Username"
- inputText: ${USERNAME}
- tapOn: "Password"
- inputText: ${PASSWORD}
- tapOn: "Login"
- assertVisible:
    id: home_screen
```

公共 Flow 自己应验证“自身动作完成的必要状态”，但 Main Flow 仍负责 Case 的最终 Expected Result。

## 7. Inline Subflow

少量条件动作可以使用：

```yaml
- runFlow:
    label: "Dismiss optional welcome dialog"
    when:
      visible: "Welcome"
    commands:
      - tapOn: "Continue"
```

如果逻辑被多处复用或超过少量步骤，应提取文件。

## 8. Setup / Teardown

可使用 Subflow 作为 setup/cleanup：

```yaml
onFlowStart:
  - runFlow: ../../common/setup-session.yaml

onFlowComplete:
  - runFlow: ../../common/cleanup-session.yaml
```

Hooks 每个 Flow 都会执行，因此公共 Hook 必须足够快，并避免递归调用自身。

## 9. Flow 独立性

禁止：

```text
TC-A 创建数据
 ↓
TC-B 默认依赖 TC-A 留下的数据
```

推荐：

```text
TC-B
 ├── setup/API/Subflow 创建前置数据
 ├── 执行 Case
 └── cleanup
```

即使使用 sequential execution，也应尽量保持每个 Flow 可以从干净设备运行。

## 10. 目录规范

### 本仓库（推荐）

```text
flows/
├── auth/
│   └── login/
│       ├── TC-AUTH-LOGIN-001.yaml
│       └── TC-AUTH-LOGIN-101.yaml
├── mobile/
│   └── demo/
│       └── TC-MOBILE-DEMO-001.yaml
modules/
├── auth/
│   └── login.yaml
├── app/
│   └── launch-foreground.yaml
└── customer/
    └── create.yaml
```

Main Flow 在 `flows/{domain}/{scene}/`；可复用 Subflow 在 `modules/`（见 [repo-conventions.md](repo-conventions.md)）。

### 通用 Maestro 布局（其他项目）

```text
flows/
├── auth/
│   ├── TC-AUTH-001.yaml
│   └── TC-AUTH-002.yaml
└── common/
    └── auth/
        └── login.yaml
```

`common/` 不应被当成独立测试集执行。

## 11. Review Checklist

- [ ] Subflow 单一职责
- [ ] 没有一条命令一个 Subflow
- [ ] 参数显式
- [ ] 没有隐式依赖父 Flow 状态
- [ ] 公共 Flow 未被作为独立 Test Case 发现执行
- [ ] Main Flow 保留最终业务 Assertion

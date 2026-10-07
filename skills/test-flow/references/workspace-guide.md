# Workspace Guide

## 1. 目的

规定测试 Flow 在工程中的组织、发现、Tag 与公共文件隔离方式。

## 2. 官方依据

- Workspace management overview  
  https://docs.maestro.dev/maestro-flows/workspace-management/workspace-management-overview
- Project configuration  
  https://docs.maestro.dev/maestro-flows/workspace-management/project-configuration
- Repository configuration  
  https://docs.maestro.dev/maestro-flows/workspace-management/design-your-test-architecture/repository-configuration
- Test discovery and tags  
  https://docs.maestro.dev/maestro-flows/workspace-management/test-discovery-and-tags
- Sequential execution  
  https://docs.maestro.dev/maestro-flows/workspace-management/sequential-execution
- Workspace configuration reference  
  https://docs.maestro.dev/reference/workspace-configuration
- Official best-practices article  
  https://maestro.dev/blog/maestro-best-practices-structuring-your-test-suite

## 3. 推荐工程结构

结合本项目“一 Case 一 Main Flow”的要求：

```text
test-assets/
├── cases/
├── data/
├── flows/
│   ├── config.yaml
│   ├── auth/
│   │   ├── TC-AUTH-001.yaml
│   │   └── TC-AUTH-002.yaml
│   ├── order/
│   │   └── TC-ORDER-001.yaml
│   └── common/
│       ├── auth/
│       │   └── login.yaml
│       └── order/
│           └── create-order.yaml
└── scripts/
```

## 4. Main Flow 与 Common 隔离

官方推荐把可复用 Flow 单独组织；公共 Utility Flow 不应被当成独立 Test Case 发现执行。

示例：

```yaml
flows:
  - "auth/**"
  - "order/**"
  - "!common/**"
```

或者依据实际根目录调整 pattern。

`flows` 必须至少有一个正向匹配规则。

## 5. `config.yaml`

适合管理：

- Flow discovery；
- include/exclude tags；
- execution order；
- test output directory；
- platform settings；
- Cloud settings。

不要把单条 Case 的业务数据写进 `config.yaml`。

## 6. Tags

推荐 Tag 用于：

- smoke；
- regression；
- critical；
- platform；
- locale；
- 临时状态（wip/flaky）。

注意同一个 include tag 列表通常按 OR 语义筛选，不要误认为自动是 AND。

## 7. Sequential Execution

默认不应依赖执行顺序。

如果确实需要顺序：

```yaml
executionOrder:
  continueOnFailure: false
  flowsOrder:
    - signup
    - verify
```

但仍要求 Flow 尽量可以在重置设备上独立运行。

逻辑依赖优先：

```text
Main Flow
  ↓
runFlow(setup)
```

而不是：

```text
Flow A 的副作用
  ↓
Flow B 偷偷依赖
```

## 8. User Journey vs Feature

官方给出两类常见组织模型：

- Goal-driven / User Journey；
- Feature-based。

本项目已经通过 Test Design 按“模块 → 场景功能 → Case”组织，因此 Flow 层建议继续 Feature/Module 对齐，并由 Main Flow 对应 Case。

## 9. Review Checklist

- [ ] `common/` 不被独立执行
- [ ] `config.yaml` discovery 与目录一致
- [ ] Tag 字典统一
- [ ] 无跨 Flow 隐式状态依赖
- [ ] Sequential execution 仅在确有需要时使用
- [ ] Flow 目录与测试设计模块可对应

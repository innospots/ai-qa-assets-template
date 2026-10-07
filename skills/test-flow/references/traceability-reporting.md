# Traceability and Reporting Guide

## 1. 目的

建立：

```text
TDS Scenario
   ↓
Test Case
   ↓
Main Flow
   ↓
Execution
   ↓
JUnit / HTML / Artifacts
```

完整追踪链。

## 2. 官方依据

- Test reports and artifacts  
  https://docs.maestro.dev/maestro-flows/workspace-management/test-reports-and-artifacts
- Labeling and error handling  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/labeling-and-error-handling
- Workspace configuration  
  https://docs.maestro.dev/reference/workspace-configuration

## 3. Case → Flow

强制映射：

```text
TC-AUTH-001
    ↓
flows/auth/TC-AUTH-001.yaml
```

Flow Header：

```yaml
name: TC-AUTH-001 - Login successfully
properties:
  testCaseId: TC-AUTH-001
  junitId: TC-AUTH-001
  junitClassname: auth.login
```

## 4. `properties`

Maestro 报告可以携带自定义 Flow properties。

推荐标准字段：

```yaml
properties:
  testCaseId: TC-AUTH-001
  priority: P1
  module: auth
  scenario: login
  junitId: TC-AUTH-001
  junitClassname: auth.login
```

不要写过多重复元数据。

## 5. Stable JUnit ID

Case ID 应作为稳定 ID：

```yaml
properties:
  junitId: TC-AUTH-001
```

即使 Flow 的展示名称发生变化：

```yaml
name: TC-AUTH-001 - Customer login with valid password
```

报告仍可按稳定 Case ID 聚合。

## 6. Step Label

对于技术 ID 不容易理解的步骤：

```yaml
- tapOn:
    id: submit_btn_v3
    label: "Submit customer login"
```

Label 的目标是：

- 报告可读；
- 表达业务意图；
- 降低实现细节噪声。

## 7. Screenshot / Artifact

截图是证据，不是测试结论。

推荐只在以下情况显式截图：

- 业务要求保存证据；
- 关键复杂页面；
- 调试已知问题；
- 报告系统需要补充附件。

图片名可带 Case ID：

```yaml
- takeScreenshot: "TC-AUTH-001-login-success.png"
```

并行/分片时，应加入 shard/device 唯一信息，防止覆盖。

## 8. Failure 原则

不得通过：

- `optional: true`
- 大范围 `retry`
- 删除 Assertion
- 把 Assertion 改成 Screenshot

来提高统计通过率。

测试报告的“失败”本身是有效结果。

## 9. 最小追踪字段

Main Flow 最少：

```yaml
name: TC-XXX-001 - ...
properties:
  testCaseId: TC-XXX-001
```

CI/JUnit 场景推荐：

```yaml
properties:
  testCaseId: TC-XXX-001
  junitId: TC-XXX-001
  junitClassname: module.scenario
```

## 10. Review Checklist

- [ ] Case ID 与文件名一致
- [ ] Flow Header 有 `testCaseId`
- [ ] JUnit ID 稳定
- [ ] Label 表达业务含义
- [ ] Screenshot 未替代 Assertion
- [ ] Failure 未被容错机制隐藏

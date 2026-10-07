# Naming Conventions

## 1. 目的

为 Main Flow、Subflow、Script、Tag、变量和元数据建立统一命名，保证 Agent 生成结果可读、可检索、可追踪。

## 2. 原则

命名应：

- 稳定；
- 有业务语义；
- 避免工具实现细节；
- 不包含敏感数据；
- 不依赖步骤编号表达含义。

## 3. Main Flow 文件

本仓库路径：

```text
flows/{domain}/{scene}/TC-{DOMAIN}-{SCENE}-{NNN}.yaml
```

示例：

```text
flows/api/health/TC-API-HEALTH-001.yaml
flows/web/home/TC-WEB-HOME-001.yaml
```

文件名 **必须** 与 Case 测试 ID 完全一致；Case 标题变化不要求重命名文件。

## 4. Flow `name`

推荐：

```yaml
name: TC-API-HEALTH-001 GET 探测返回 2xx
```

结构：

```text
Case ID + 简短业务目的
```

## 5. Subflow

使用小写 `kebab-case`：

```text
login.yaml
logout.yaml
create-test-user.yaml
navigate-to-orders.yaml
dismiss-system-dialog.yaml
```

不要：

```text
common1.yaml
step2.yaml
click-login.yaml
run-login-flow.yaml
```

## 6. Script

```text
create-test-user.js
delete-test-user.js
verify-order-state.js
generate-business-date.js
```

目录再表达分类：

```text
scripts/fixtures/
scripts/assertions/
scripts/utils/
```

## 7. Variables

外部输入/环境参数推荐大写：

```text
USERNAME
PASSWORD
API_BASE_URL
TENANT_ID
EXPECTED_STATUS
```

Subflow 参数同样使用清晰大写名称。

## 8. `output`

使用小写 namespace：

```text
output.auth.token
output.order.id
output.fixture.userId
```

## 9. Tags

Tag 表达测试属性，不表达随机实现细节。

推荐维度：

```text
smoke
regression
critical
auth
order
web
android
ios
locale-fr
wip
flaky
```

项目应限制 Tag 字典，避免：

```text
smoke-test
smokeTest
Smoke
smoke_case
```

同时存在。

## 10. Properties

统一：

```yaml
properties:
  testCaseId: TC-AUTH-001
  priority: P1
  junitId: TC-AUTH-001
  junitClassname: auth.login
```

不要在不同 Flow 中发明：

```text
case_id
caseId
testId
tcId
```

多个同义字段。

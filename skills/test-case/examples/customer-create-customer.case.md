---
id: CUSTOMER-CREATE
name: 创建客户
module: customer
scene: create-customer
priority: P0
source:
  tds: CUSTOMER-CREATE-DESIGN
platform:
  - android
  - ios
  - web
tags:
  - customer
  - regression
  - smoke
---

# 创建客户

> 本文件基于 `CUSTOMER-CREATE-DESIGN` 生成。数据脚本参照 [`sample-customer-customers.js`](sample-customer-customers.js)；正式资产写入 `data/customer/`。

## 测试用例清单

| Case ID | TDS 场景 | 测试用例 | 类型 | 优先级 |
| --- | --- | --- | --- | --- |
| TC-CUSTOMER-CREATE-001-001 | DS-CUSTOMER-CREATE-001 | 使用完整合法信息创建客户 | 正向 | P0 |
| TC-CUSTOMER-CREATE-002-001 | DS-CUSTOMER-CREATE-002 | 仅填写必填字段创建客户 | 正向 | P0 |
| TC-CUSTOMER-CREATE-101-001 | DS-CUSTOMER-CREATE-101 | 客户名称为空时创建客户 | 反向 | P1 |
| TC-CUSTOMER-CREATE-102-001 | DS-CUSTOMER-CREATE-102 | 客户编号为空时创建客户 | 反向 | P1 |
| TC-CUSTOMER-CREATE-103-001 | DS-CUSTOMER-CREATE-103 | 使用已存在客户编号创建客户 | 反向 | P0 |
| TC-CUSTOMER-CREATE-104-001 | DS-CUSTOMER-CREATE-104 | 手机号格式非法时创建客户 | 反向 | P1 |
| TC-CUSTOMER-CREATE-105-001 | DS-CUSTOMER-CREATE-105 | 查看人员尝试创建客户 | 权限 | P0 |
| TC-CUSTOMER-CREATE-105-002 | DS-CUSTOMER-CREATE-105 | 其他租户用户向当前租户创建客户 | 权限 | P0 |
| TC-CUSTOMER-CREATE-106-001 | DS-CUSTOMER-CREATE-106 | 短时间内连续提交相同合法资料 | 幂等 | P0 |
| TC-CUSTOMER-CREATE-106-002 | DS-CUSTOMER-CREATE-106 | 首次请求超时后使用相同编号再次提交 | 幂等 | P0 |
| TC-CUSTOMER-CREATE-201-001 | DS-CUSTOMER-CREATE-201 | 客户名称为 1 个字符时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-201-002 | DS-CUSTOMER-CREATE-201 | 客户名称为 100 个字符时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-201-003 | DS-CUSTOMER-CREATE-201 | 客户名称为 101 个字符时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-202-001 | DS-CUSTOMER-CREATE-202 | 客户编号为 1 个字符时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-202-002 | DS-CUSTOMER-CREATE-202 | 客户编号为 32 个字符时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-202-003 | DS-CUSTOMER-CREATE-202 | 客户编号为 33 个字符时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-203-001 | DS-CUSTOMER-CREATE-203 | 客户名称为纯空格时创建客户 | 边界 | P1 |
| TC-CUSTOMER-CREATE-301-001 | DS-CUSTOMER-CREATE-301 | 保存失败时创建客户 | 异常 | P1 |

## 测试数据

| 数据 | 说明 |
| --- | --- |
| users.operator | 有创建权限的运营人员 |
| users.viewer | 仅查看人员 |
| users.otherTenantOperator | 其他租户运营人员 |
| tenants.current | 当前租户 |
| tenants.other | 其他租户 |
| customers.validFull | 全部合法字段 |
| customers.requiredOnly | 仅必填字段 |
| customers.emptyName | 名称为空 |
| customers.emptyCode | 编号为空 |
| customers.existing | 已存在客户（编号占用） |
| customers.duplicateCode | 与 existing 同编号 |
| customers.invalidPhone | 非法手机号 |
| customers.validPermission | 权限场景合法资料 |
| customers.idempotent | 重复提交资料 |
| customers.timeoutRetry | 超时重试资料 |
| customers.nameLength1 / nameLength100 / nameLength101 | 名称长度边界 |
| customers.codeLength1 / codeLength32 / codeLength33 | 编号长度边界 |
| customers.blankName | 纯空格名称 |
| customers.validForFailure | 保存失败专项 |

Flow 加载 `examples/sample-customer-*.js`（或 `data/customer/*.js`）后引用 `${output.customer.customers.validFull}` 等。

## 正向测试

纳入 smoke 与 regression 默认套件。

### TC-CUSTOMER-CREATE-001-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-001-001
title: 使用完整合法信息创建客户
source: DS-CUSTOMER-CREATE-001
priority: P0
type: positive
data:
  user: users.operator
  customer: customers.validFull
  tenant: tenants.current
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 在当前平台内尚不存在
- 当前租户为 `tenant`

### 测试步骤

1. 进入客户管理并发起新增客户
2. 使用 `customer` 填写客户名称、客户编号和手机号
3. 提交创建请求
4. 在客户列表中按 `customer.code` 查询
5. 打开该客户详情页
6. 通过接口或持久化层查询该客户记录
7. 查询该客户的操作日志

### 预期结果

1. 创建成功，返回成功提示或等价成功状态
2. 新客户初始状态为「正常」
3. 客户列表中存在该客户，且名称、编号、手机号与提交一致
4. 详情页字段与提交一致（名称已去除前后空格）
5. 接口或持久化记录与提交字段一致
6. 记录归属当前租户 `tenant.code`
7. 创建人、创建时间字段有值且创建人为当前 `user`
8. 存在与创建操作对应的操作日志记录

### TC-CUSTOMER-CREATE-002-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-002-001
title: 仅填写必填字段创建客户
source: DS-CUSTOMER-CREATE-002
priority: P0
type: positive
data:
  user: users.operator
  customer: customers.requiredOnly
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 在当前平台内尚不存在
- `customer.phone` 为空

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name` 与 `customer.code`，不填写手机号
3. 提交创建请求
4. 在客户列表中按 `customer.code` 查询该客户

### 预期结果

1. 创建成功
2. 新客户初始状态为「正常」
3. 列表与详情中名称、编号与提交一致
4. 手机号为空或符合产品定义的默认值/空值展示规则
5. 不存在因缺少手机号而产生的残缺记录

## 反向测试

界面可构造，纳入 regression，不纳入 smoke。

### TC-CUSTOMER-CREATE-101-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-101-001
title: 客户名称为空时创建客户
source: DS-CUSTOMER-CREATE-101
priority: P1
type: negative
data:
  user: users.operator
  customer: customers.emptyName
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.name` 为空字符串
- `customer.code` 合法且尚未占用

### 测试步骤

1. 进入客户管理并发起新增客户
2. 将客户名称留空，填写 `customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 系统拒绝创建
2. 返回可识别的名称必填或名称无效错误
3. 不存在以 `customer.code` 为编号的新客户记录

### TC-CUSTOMER-CREATE-102-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-102-001
title: 客户编号为空时创建客户
source: DS-CUSTOMER-CREATE-102
priority: P1
type: negative
data:
  user: users.operator
  customer: customers.emptyCode
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 为空字符串
- `customer.name` 合法

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name` 与 `customer.phone`，客户编号留空
3. 提交创建请求
4. 按 `customer.name` 查询是否新增客户

### 预期结果

1. 系统拒绝创建
2. 返回可识别的编号必填或编号无效错误
3. 未新增与本次提交匹配的客户记录

### TC-CUSTOMER-CREATE-103-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-103-001
title: 使用已存在客户编号创建客户
source: DS-CUSTOMER-CREATE-103
priority: P0
type: negative
data:
  user: users.operator
  existing_customer: customers.existing
  customer: customers.duplicateCode
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `existing_customer` 已存在于当前平台
- `customer.code` 与 `existing_customer.code` 相同

### 测试步骤

1. 确认 `existing_customer` 已存在并记录其名称与状态
2. 进入客户管理并发起新增客户
3. 使用 `customer` 填写资料并提交
4. 按 `customer.code` 查询所有匹配记录

### 预期结果

1. 系统拒绝创建
2. 返回可识别的编号重复错误
3. 相同编号仍只有一条客户记录
4. 原 `existing_customer` 的名称、手机号、状态未被修改

### TC-CUSTOMER-CREATE-104-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-104-001
title: 手机号格式非法时创建客户
source: DS-CUSTOMER-CREATE-104
priority: P1
type: negative
data:
  user: users.operator
  customer: customers.invalidPhone
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.name` 与 `customer.code` 合法且编号未占用
- `customer.phone` 不符合手机号格式规则

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 系统拒绝创建
2. 返回可识别的手机号格式错误
3. 不存在以 `customer.code` 为编号的新客户记录

## 权限测试

### TC-CUSTOMER-CREATE-105-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-105-001
title: 查看人员尝试创建客户
source: DS-CUSTOMER-CREATE-105
priority: P0
type: permission
data:
  user: users.viewer
  customer: customers.validPermission
```

### 前置条件

- 以 `user`（查看人员角色）身份登录
- `user` 不具备客户创建权限
- `customer.code` 尚未占用

### 测试步骤

1. 进入客户管理，确认新增客户入口不可用或不可见
2. 通过界面尝试发起创建（若入口被隐藏则改由等价受限路径验证不可创建）
3. 通过创建客户接口使用 `customer` 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 界面层无法完成创建操作
2. 接口返回权限不足或等价拒绝响应
3. 不存在以 `customer.code` 为编号的新客户记录

### TC-CUSTOMER-CREATE-105-002

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-105-002
title: 其他租户用户向当前租户创建客户
source: DS-CUSTOMER-CREATE-105
priority: P0
type: permission
data:
  user: users.otherTenantOperator
  tenant: tenants.other
  current_tenant: tenants.current
  customer: customers.validPermission
```

### 前置条件

- 以 `user` 身份登录，`user.tenant` 为 `tenant.code`
- 目标写入租户为 `current_tenant`，与 `user` 所属租户不同
- `customer.code` 在目标租户内尚未占用

### 测试步骤

1. 以 `user` 身份尝试向 `current_tenant` 发起客户创建
2. 通过界面或接口使用 `customer` 提交创建请求
3. 在 `current_tenant` 下按 `customer.code` 查询客户记录

### 预期结果

1. 界面层无法完成跨租户创建
2. 接口返回权限不足或租户隔离拒绝响应
3. `current_tenant` 下不存在以 `customer.code` 为编号的新客户记录

## 幂等与重复操作

### TC-CUSTOMER-CREATE-106-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-106-001
title: 短时间内连续提交相同合法资料
source: DS-CUSTOMER-CREATE-106
priority: P0
type: idempotency
data:
  user: users.operator
  customer: customers.idempotent
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 尚未占用
- 两次提交使用完全相同的 `customer` 资料

### 测试步骤

1. 进入客户管理并填写 `customer` 全部字段
2. 在极短时间内连续提交两次创建请求
3. 按 `customer.code` 查询客户记录数量
4. 查看第二次请求的响应或错误提示

### 预期结果

1. 最终至多存在一条以 `customer.code` 为编号的有效客户记录
2. 若第二次被拒绝，错误可识别（如重复提交或编号已占用）
3. 已创建记录的名称、手机号与 `customer` 一致且状态为「正常」

### TC-CUSTOMER-CREATE-106-002

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-106-002
title: 首次请求超时后使用相同编号再次提交
source: DS-CUSTOMER-CREATE-106
priority: P0
type: idempotency
data:
  user: users.operator
  customer: customers.timeoutRetry
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 尚未占用
- 首次提交可模拟为超时或结果未知

### 测试步骤

1. 使用 `customer` 提交创建请求，并模拟首次请求超时或结果未确认
2. 在不更换 `customer.code` 的前提下再次提交相同资料
3. 按 `customer.code` 查询客户记录数量与详情
4. 确认两次请求的最终业务状态

### 预期结果

1. 最终至多存在一条以 `customer.code` 为编号的有效客户记录
2. 若首次实际已成功，第二次应返回可识别的重复或幂等拒绝，且不产生第二条记录
3. 若首次未成功，第二次成功创建后记录字段与 `customer` 一致
4. 无论哪条路径，编号占用状态可判定且无重复有效记录

## 边界测试

### TC-CUSTOMER-CREATE-201-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-201-001
title: 客户名称为 1 个字符时创建客户
source: DS-CUSTOMER-CREATE-201
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.nameLength1
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.name` 长度恰好为 1 个字符
- `customer.code` 合法且尚未占用

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 创建成功
2. 列表与详情中名称为 1 个字符且与 `customer.name` 一致
3. 客户初始状态为「正常」

### TC-CUSTOMER-CREATE-201-002

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-201-002
title: 客户名称为 100 个字符时创建客户
source: DS-CUSTOMER-CREATE-201
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.nameLength100
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.name` 长度恰好为 100 个字符
- `customer.code` 合法且尚未占用

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 创建成功
2. 列表与详情中名称长度为 100 且与 `customer.name` 一致
3. 客户初始状态为「正常」

### TC-CUSTOMER-CREATE-201-003

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-201-003
title: 客户名称为 101 个字符时创建客户
source: DS-CUSTOMER-CREATE-201
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.nameLength101
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.name` 长度恰好为 101 个字符
- `customer.code` 合法且尚未占用

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 系统拒绝创建
2. 返回可识别的名称长度超限错误
3. 不存在以 `customer.code` 为编号的新客户记录

### TC-CUSTOMER-CREATE-202-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-202-001
title: 客户编号为 1 个字符时创建客户
source: DS-CUSTOMER-CREATE-202
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.codeLength1
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 长度恰好为 1 个字符且尚未占用
- `customer.name` 合法

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 创建成功
2. 列表与详情中编号长度为 1 且与 `customer.code` 一致
3. 客户初始状态为「正常」

### TC-CUSTOMER-CREATE-202-002

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-202-002
title: 客户编号为 32 个字符时创建客户
source: DS-CUSTOMER-CREATE-202
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.codeLength32
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 长度恰好为 32 个字符且尚未占用
- `customer.name` 合法

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 创建成功
2. 列表与详情中编号长度为 32 且与 `customer.code` 一致
3. 客户初始状态为「正常」

### TC-CUSTOMER-CREATE-202-003

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-202-003
title: 客户编号为 33 个字符时创建客户
source: DS-CUSTOMER-CREATE-202
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.codeLength33
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 长度恰好为 33 个字符
- `customer.name` 合法

### 测试步骤

1. 进入客户管理并发起新增客户
2. 填写 `customer.name`、`customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 系统拒绝创建
2. 返回可识别的编号长度超限错误
3. 不存在以 `customer.code` 为编号的新客户记录

### TC-CUSTOMER-CREATE-203-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-203-001
title: 客户名称为纯空格时创建客户
source: DS-CUSTOMER-CREATE-203
priority: P1
type: boundary
data:
  user: users.operator
  customer: customers.blankName
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.name` 仅包含空格字符
- `customer.code` 合法且尚未占用

### 测试步骤

1. 进入客户管理并发起新增客户
2. 在客户名称输入 `customer.name`，填写 `customer.code` 与 `customer.phone`
3. 提交创建请求
4. 按 `customer.code` 查询客户记录

### 预期结果

1. 系统拒绝创建
2. 返回可识别的名称无效或名称必填错误（去空格后为空）
3. 不存在以 `customer.code` 为编号的新客户记录

## 异常测试

专项场景，不纳入 smoke 与 regression 默认套件。

### TC-CUSTOMER-CREATE-301-001

### 基本信息

```yaml
id: TC-CUSTOMER-CREATE-301-001
title: 保存失败时创建客户
source: DS-CUSTOMER-CREATE-301
priority: P1
type: exception
execution: deferred
data:
  user: users.operator
  customer: customers.validForFailure
```

### 前置条件

- 以 `user` 身份登录，且具有客户创建权限
- `customer.code` 尚未占用
- 测试环境可注入保存失败或依赖服务不可用（专项环境）

### 测试步骤

1. 在专项环境中配置客户保存失败条件
2. 使用 `customer` 提交创建请求
3. 检查是否存在残缺客户记录
4. 确认 `customer.code` 占用状态
5. 在失败条件解除后，使用相同 `customer` 再次提交

### 预期结果

1. 创建失败并返回明确的系统错误或保存失败提示
2. 不存在字段不完整的客户记录
3. 编号占用状态明确，不产生重复编号占用不明的数据
4. 失败条件解除后，允许重新提交且结果可判定（成功创建或再次明确失败）

## TDS 覆盖关系

| TDS 场景 | Test Case | 状态 |
| --- | --- | --- |
| DS-CUSTOMER-CREATE-001 | TC-CUSTOMER-CREATE-001-001 | Covered |
| DS-CUSTOMER-CREATE-002 | TC-CUSTOMER-CREATE-002-001 | Covered |
| DS-CUSTOMER-CREATE-101 | TC-CUSTOMER-CREATE-101-001 | Covered |
| DS-CUSTOMER-CREATE-102 | TC-CUSTOMER-CREATE-102-001 | Covered |
| DS-CUSTOMER-CREATE-103 | TC-CUSTOMER-CREATE-103-001 | Covered |
| DS-CUSTOMER-CREATE-104 | TC-CUSTOMER-CREATE-104-001 | Covered |
| DS-CUSTOMER-CREATE-105 | TC-CUSTOMER-CREATE-105-001, TC-CUSTOMER-CREATE-105-002 | Covered |
| DS-CUSTOMER-CREATE-106 | TC-CUSTOMER-CREATE-106-001, TC-CUSTOMER-CREATE-106-002 | Covered |
| DS-CUSTOMER-CREATE-201 | TC-CUSTOMER-CREATE-201-001, TC-CUSTOMER-CREATE-201-002, TC-CUSTOMER-CREATE-201-003 | Covered |
| DS-CUSTOMER-CREATE-202 | TC-CUSTOMER-CREATE-202-001, TC-CUSTOMER-CREATE-202-002, TC-CUSTOMER-CREATE-202-003 | Covered |
| DS-CUSTOMER-CREATE-203 | TC-CUSTOMER-CREATE-203-001 | Covered |
| DS-CUSTOMER-CREATE-301 | TC-CUSTOMER-CREATE-301-001 | Deferred |

## 数据引用说明

与 [`sample-customer-customers.js`](sample-customer-customers.js) 及 [`sample-customer-batch-records.js`](sample-customer-batch-records.js) 的结构一致：

| 规则 | 说明 |
| --- | --- |
| 数据脚本 | `data/customer/users.js`、`customers.js`、`tenants.js`（Skill 示例：`examples/sample-customer-*.js`） |
| 写入方式 | `output.customer = output.customer || {}` |
| Case 引用 | `## 测试数据` 表 + 步骤中的数据集名（如 `customers.validFull`） |
| Flow 引用 | `${output.customer.customers.validFull.code}` 等，层级与 JS Object 一致 |

禁止在 Case 写 JSONPath `$.…` 或内联具体业务值。

# 数组批量数据 · 单条 Case 示例

> 片段示例，非独立 Case 文件。完整规范见 [`test-case-spec.md`](../references/test-case-spec.md) §9.3；数据见 [`sample-customer-batch-records.js`](sample-customer-batch-records.js)。

## 何时用数组

| 情况 | 做法 |
| --- | --- |
| 步骤相同、仅输入/预期逐行不同 | **一条 TC** + `records[]` 循环 |
| 步骤或预期逻辑不同 | **多条 TC**（见 `../examples/customer-create-customer.case.md` 201-001/002/003） |

## 测试数据（Case 文件内）

| 数据 | 说明 |
| --- | --- |
| users.operator | 有创建权限 `users.operator` |
| nameLengthBatch | 边界批量集 `nameLengthBatch.records`（含每行 `expect`） |

## 边界测试

### TC-CUSTOMER-CREATE-201-001 按批量表循环验证名称长度边界

**目的**

一条 Case 覆盖 DS-CUSTOMER-CREATE-201 中 1 / 100 / 101 字符三种边界，避免拆三条同构 TC。

**前置条件**

- 以 `users.operator` 登录且有创建权限
- 每行使用的 `code` 在提交前均未被占用

**步骤**

1. 进入客户创建功能
2. 对 `nameLengthBatch.records` **每一行**依次执行：
   1. 使用该行的 `name`、`code`、`phone` 填写资料
   2. 提交创建
   3. 根据该行 `expect` 判定结果：
      - `success`：创建成功，名称按规则保存
      - `reject`：拒绝创建，返回与 `errorHint` 一致的可识别校验错误，无新记录
   4. 清理或换号，确保下一行 `code` 仍可用（由 Flow 准备环境）

**预期结果**

- 三行全部执行完毕
- 每行结果与数据中 `expect` 一致
- `len1`、`len100` 成功；`len101` 拒绝且无新记录

**Flow 引用（实现层，不写进 Case 正文）**

```text
${output.customer.nameLengthBatch.records}
${output.customer.nameLengthBatch.records[0].name}
```

循环逻辑由 `test:flow` 在 Flow 中实现（Maestro `repeat` / 脚本遍历等）。

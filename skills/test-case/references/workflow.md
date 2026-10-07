# Case 生成工作流

## 1. 输入盘点（T0）

| 输入 | 路径 |
| --- | --- |
| 场景 TDS | `designs/{domain}/{scene}.design.md` |
| 已有 Case | `cases/{domain}/{scene}.case.md` |
| 已有 data | `data/{domain}/`（参照 [`../examples/sample-customer-customers.js`](../examples/sample-customer-customers.js)） |

产出：DS→TC 映射、待增 data 节点清单。

## 2. 任务拆解

| 任务 | 产出 |
| --- | --- |
| T1 | `data/{domain}/*.js`（按业务对象拆分，参照 customer 示例） |
| T2 | `cases/{domain}/{scene}.case.md` |
| T_review | checklist 审查 |

## 3. 编写 data（T1）

参照 [`../examples/sample-customer-customers.js`](../examples/sample-customer-customers.js) 与 [`../examples/sample-customer-batch-records.js`](../examples/sample-customer-batch-records.js)：

1. `output.<domain> = output.<domain> || {}`
2. 语义化数据集名 + `description`
3. fixtures 用 `path: 'fixtures/...'`
4. `node --check data/**/*.js`

Skill 示例：`examples/sample-customer-*.js`。

## 4. 编写 Case（T2）

1. Front Matter（含 `source.tds`、`tags`、`platform`）
2. `## 测试数据` 表（参照 [`../examples/customer-create-customer.case.md`](../examples/customer-create-customer.case.md)）
3. `## 测试用例清单` + 分类型 TC 章节
4. 步骤引用数据集名，不写具体值
5. `## TDS 覆盖关系`
6. `./scripts/validate-cases.sh`

## 5. 交付

- Case / data 变更、DS→TC 表、校验结果、缺 Flow 清单

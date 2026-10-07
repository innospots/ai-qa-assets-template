# 测试用例编写规范

## 1. 定义与目标

Case 将 TDS 中的 `DS-` 测试场景落实为**可执行、可判定**的测试用例（`TC-`）。Case 回答「具体怎么测、用什么数据、步骤与预期是什么」，**不**重新设计测试范围，也不写执行器 DSL。

```text
PRD / PDD
    ↓
designs/{domain}/index.md + {scene}.design.md（TDS，DS- 清单）
    ↓
cases/{domain}/{scene}.case.md（TC- 清单与步骤）
    ↓
data/{domain}/*.js（具体值，output 层级）
    ↓
fixtures/（二进制素材，由 data 脚本引用 path）
    ↓
flows/{domain}/{scene}/TC-*.yaml（执行实现）
```

基本原则：

> TDS 定义「测什么」；Case 定义「具体怎么测」。

---

## 2. 文件组织

### 2.1 一场景一 Case 文件

与 TDS 场景文档一一对应：

```text
designs/customer/create-customer.design.md
        ↓
cases/customer/create-customer.case.md
        ↓
data/customer/users.js、customers.js、…
        ↓
fixtures/（若有二进制素材）
```

- 路径：`cases/{domain}/{scene}.case.md`
- `{scene}` 与 TDS 文件名一致（kebab-case）
- **禁止**一个 TC 一个文件；**禁止**按 smoke/反向/平台拆多个 Case 文件

### 2.2 与 TDS、数据、Flow 的对应

| 资产 | 路径 | 职责 |
| --- | --- | --- |
| 模块 Index | `designs/{domain}/index.md` | 公共规则 |
| 场景 TDS | `designs/{domain}/{scene}.design.md` | `DS-` 意图与清单 |
| Case | `cases/{domain}/{scene}.case.md` | `TC-` 步骤与预期；引用**数据集名称** |
| 业务数据 | `data/{domain}/{business-object}.js` | 具体值；`output.<domain>` 层级 |
| 二进制素材 | `fixtures/{domain}/` | 路径登记在 data 脚本的 `path` 字段 |
| Flow | `flows/{domain}/{scene}/TC-*.yaml` | 一 TC 一 Flow；`runScript` 加载 data |

**标准参照**：[`../examples/sample-customer-customers.js`](../examples/sample-customer-customers.js)。Case 只写数据集名称；Flow 引用与 data Object 一致的层级。

详见 [`../../../docs/data-env-standard.md`](../../../docs/data-env-standard.md)。

---

## 3. TDS 与 TC 映射

### 3.1 每条 TC 必须可追溯 DS

```text
DS-CUSTOMER-CREATE-103  →  TC-CUSTOMER-CREATE-103-001
```

无来源的正式 TC 禁止落盘。

### 3.2 一个 DS 可对应一个或多个 TC

| 情况 | 做法 |
| --- | --- |
| DS 仅一种路径/一种结果 | 1 个 TC |
| DS 含多个边界值且结果不同（如 1/100/101 字符） | 每个边界 1 个 TC |
| DS 含多种角色/路径（查看人员 vs 跨租户） | 按路径拆多个 TC |
| DS 含多种失败原因（名称为空 vs 编号为空） | 各 1 个 TC |
| 同构逻辑、步骤与预期相同、仅输入不同 | 1 个 TC + 多组数据（数据驱动） |

**不是 DS 有多少条就一定有多少 TC**；Case 层展开 TDS 已明确但未拆开的具体可执行路径。

### 3.3 读 TDS 的范围

除 §9 场景清单外，还须读：

- 场景业务规则、权限与一致性要求（§5、§7.8）
- 风险与优先级（§7.10）
- 待确认与暂缓项（§11）— 暂缓 DS 不落 TC 或标 `execution: deferred`

---

## 4. TC 编号规范

### 4.1 推荐格式（TDS 追溯）

```text
TC-{DOMAIN}-{SCENE}-{DS后缀}-{CASE序号}
```

示例：

```text
TC-CUSTOMER-CREATE-103-001
TC-CUSTOMER-CREATE-201-003
```

| 段 | 含义 |
| --- | --- |
| `DOMAIN` | 模块，如 `CUSTOMER` |
| `SCENE` | 场景，如 `CREATE` |
| `DS后缀` | 与 `DS-*-{后缀}` 一致，如 `103`、`201` |
| `CASE序号` | 同一 DS 下从 `001` 递增 |

### 4.2 存量格式

存量示范领域使用 `TC-{DOMAIN}-{FEATURE}-{NNN}`（如 `TC-API-HEALTH-001`）。**已发布 ID 不重编号**；新建或从 TDS 全量落盘时优先采用 §4.1。

### 4.3 类型与 DS 后缀对应

| DS 后缀区间 | 类型 | `type` 字段 |
| --- | --- | --- |
| 001–099 | 正向 | `positive` |
| 101–199 | 反向 | `negative` |
| 201–299 | 边界 | `boundary` |
| 301–399 | 异常 | `exception` |
| — | 权限 | `permission` |
| — | 幂等 | `idempotency` |

权限、幂等若占用 DS 编号（如 105、106），TC 仍继承该 DS 后缀。

---

## 5. Case 文件结构

### 5.1 Front Matter

```yaml
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
---
```

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `id` | 是 | `{DOMAIN}-{SCENE}` 大写，与 `{scene}` 对应 |
| `name` | 是 | 中文场景名 |
| `module` | 是 | 小写，与 `cases/` 目录一致 |
| `scene` | 是 | 与文件名 `{scene}.case.md` 一致 |
| `priority` | 是 | 场景默认优先级 |
| `source.tds` | 是 | 场景 TDS 的 `id` |
| `platform` | 是 | `android` / `ios` / `web` |
| `tags` | 是 | 至少含领域 tag；正向套件见 §12 |

校验脚本**强制**存在 `## 正向测试` 与 `## 反向测试` 两节（可为空说明「本节无项」时仍保留标题，但通常应有内容）。

### 5.2 推荐正文章节

```markdown
# 创建客户

> 本文件基于 `CUSTOMER-CREATE-DESIGN` 生成。数据见 `data/customer/`（Skill 示例见 `examples/sample-customer-*.js`）。

## 测试用例清单

## 测试数据

| 数据 | 说明 |
| --- | --- |
| users.operator | 有创建权限的运营人员 `users.operator` |
| customers.validFull | 全部合法字段 `customers.validFull` |

## 正向测试

## 反向测试

## 权限测试      （按 TDS 有则写）

## 幂等与重复操作  （按 TDS 有则写）

## 边界测试      （按 TDS 有则写）

## 异常测试      （按 TDS 有则写）

## TDS 覆盖关系
```

无对应类型时可省略该章，但 §5.1 两节必填；**推荐**含 `## 测试数据` 表（参照 `cases/web/`）。

---

## 6. 测试用例清单

文件开头维护全量 TC 索引表：

| Case ID | TDS 场景 | 测试用例 | 类型 | 优先级 |
| --- | --- | --- | --- | --- |
| TC-CUSTOMER-CREATE-001-001 | DS-CUSTOMER-CREATE-001 | 使用完整合法信息创建客户 | 正向 | P0 |

清单不含详细步骤；用于评审、覆盖检查与 AI 定位。

---

## 7. 单条 TC 结构

每条 TC 放在类型章节（如 `## 反向测试`）下，标题用 `### TC-...`：

- **基本信息**（可选 YAML）：`id`、`title`、`source`、`priority`、`type`；`data` 写**数据集名称**（如 `customers.validFull`），不写 JSONPath
- **步骤 / 预期**：可直接用 `**步骤**` / `**预期结果**`（参照 `cases/web/attach-image.case.md`），步骤中引用数据集名（如 `normalImage`、`general`）

可选：`### 测试目标`（一句）；专项异常在基本信息中加 `execution: deferred`。

---

## 8. 标题、步骤与预期

### 8.1 标题

必须表达：**在什么条件下做什么操作**。

- 推荐：「使用已存在客户编号创建客户」「客户名称长度为 101 个字符时创建客户」
- 禁止：「创建客户测试」「Case 01」「编号测试」

### 8.2 步骤

- 一步一主要业务动作；动词开头
- 引用数据用**数据集名称**（如 `validFull`、`normalImage`、`zh`），不写具体字段值
- 禁止：选择器、坐标、Maestro/API 代码、「执行相关操作」
- 前置状态写入「前置条件」，不把登录点击链写进前置（除非该 Case 专测登录）

### 8.3 预期

必须可判定 Pass/Fail：

- 禁止：「系统正常」「结果正确」「页面正常」
- 推荐：明确拒绝/成功、可见错误、记录数量、字段一致、租户归属、操作日志等

TDS 要求数据一致性时（创建成功），正向 TC 预期须覆盖：列表、详情、持久化或接口、租户、创建人/时间、操作日志（按环境能力选取，不可 silent 省略）。

### 8.4 控制变量（反向/边界）

只改变当前验证的主条件，其余字段保持合法，以便归因单一失败原因。

---

## 9. 测试数据

数据文件位于 `data/{domain}/{business-object}.js`；业务对象参照 [`../examples/sample-customer-customers.js`](../examples/sample-customer-customers.js)。Case 只声明数据集名称，不复制敏感值或执行器表达式。环境目标路径属于 env 配置，不应伪装为测试数据。

### 9.1 按业务对象拆分

```javascript
output.customer = output.customer || {};
output.customer.customers = {
  validFull: { name: '测试客户A', code: 'CUST001' },
  emptyName: { name: '', code: 'CUST101' }
};
```

- 每个脚本增量写入 `output.<domain>`，不得覆盖其他域。
- 字段按业务含义命名；二进制素材置于 `fixtures/`，data 中只引用路径。
- 密码、Token 从 env/CI Secret 读取，不写入仓库或 Artifact。
- Flow 先用 `runScript` 加载本场景需要的脚本，再按实际 Object 层级引用，例如 `${output.customer.customers.validFull.code}`。

### 9.2 Case 引用方式

```markdown
## 测试数据

| 数据集 | 用途 |
| --- | --- |
| validFull | 合法客户资料 |
| emptyName | 名称为空的资料 |

### TC-CUSTOMER-CREATE-101-001 名称为空

1. 使用 `emptyName` 提交创建请求。
2. 验证系统拒绝创建，记录未落库。
```

Case 中不写 Maestro、pytest 或 Playwright 变量语法。

### 9.3 数组数据

只有步骤与判定逻辑相同、输入不同的场景，才用一条 TC 加 `records[]`。完整示例见 [`../examples/sample-customer-batch-records.js`](../examples/sample-customer-batch-records.js) 与 [`../examples/batch-one-case.md`](../examples/batch-one-case.md)。各行步骤或预期不同则拆为多个 TC。

变更 data 后检查所有引用 Flow，并运行 `find data -name '*.js' -type f -exec node --check {} \;`。

---

## 10. 类型专项要求

| 类型 | 要点 |
| --- | --- |
| 正向 | 合法输入下成功；验证业务结果 + 必要数据一致性 |
| 反向 | 拒绝 + 明确错误 + 无错误数据落库 |
| 权限 | UI 不可用 **且** 接口拒绝 **且** 无落库 |
| 幂等 | 最终至多一条有效记录；状态可判定 |
| 边界 | 一具体边界值一条 TC；不同结果必须拆开 |
| 异常 | 错误可识别、无残缺数据、可恢复；专项标 `execution: deferred` |

---

## 11. TDS 覆盖关系

文件末尾维护：

| TDS 场景 | Test Case | 状态 |
| --- | --- | --- |
| DS-CUSTOMER-CREATE-001 | TC-CUSTOMER-CREATE-001-001 | Covered |
| DS-CUSTOMER-CREATE-301 | TC-CUSTOMER-CREATE-301-001 | Deferred |

状态：`Covered` / `Pending` / `Deferred` / `N/A`。

---

## 12. 执行范围与 Tags

| 场景类型 | 默认套件 | Flow tags（`test:flow`） |
| --- | --- | --- |
| 正向 | smoke + regression | `smoke, regression, positive` |
| 反向、边界（界面可构造） | regression | `regression, negative` / `boundary` |
| 异常、故障注入 | **专项，不默认跑** | `special, exception`；`execution: deferred` |

Front Matter `tags` 表示文件级范围；各 TC 的专项属性写在基本信息 YAML 中。

---

## 13. 写作边界

禁止写入 Case：

- Maestro/YAML/选择器/坐标
- 真实凭据与环境地址
- 与 TDS 无关的新测试意图
- 把 Flow 实现细节当作预期

Case **不**修改 `flows/`、`modules/`（可声明数据引用名；实现归 `test:flow`）。

---

## 14. 修改与评审

- 业务变化：先 TDS → 再 Case → 再 Flow
- 仅执行变化：可只改 Flow；交付说明为何不改动 Case
- 已发布 `TC-` 意图不变则保留 ID
- 评审：DS 覆盖完整、步骤可执行、预期可判定、数据引用有效、无工具耦合

---

## 15. 相关规范

- [`SKILL.md`](../SKILL.md)：`test:case` 入口
- [`workflow.md`](workflow.md)：从 TDS 生成 Case 的流程
- [`review-checklist.md`](review-checklist.md)：生成后审查
- [`../examples/customer-create-customer.case.md`](../examples/customer-create-customer.case.md)：完整 Case 示例
- [`../examples/sample-customer-batch-records.js`](../examples/sample-customer-batch-records.js)：数组批量 data 示例
- [`../examples/batch-one-case.md`](../examples/batch-one-case.md)：一条 Case 循环 `records[]` 写法
- [`../examples/sample-customer-customers.js`](../examples/sample-customer-customers.js)：业务 data 标准参照
- [`../../../docs/data-env-standard.md`](../../../docs/data-env-standard.md)：data 与 env 边界
- [`../../test-design/references/tds-spec.md`](../../test-design/references/tds-spec.md)：TDS 规范
- [`../../../docs/test-asset-guide.md`](../../../docs/test-asset-guide.md)：资产模型

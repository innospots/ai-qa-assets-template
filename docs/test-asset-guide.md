# 测试资产管理指南

## 1. 目的与适用范围

本指南规定测试资产从需求分析、测试设计、自动化实现、执行到结果归档的统一管理方式。适用于人工维护、AI Agent 生成、CI 执行以及测试报告生成。

本仓库管理的是可长期复用的测试资产，不负责绑定或规定某一种测试执行工具。

## 2. 核心原则

1. **TDS 先定设计范围，Case 是可执行测试意图的唯一事实源。** TDS 定义风险、覆盖与 `DS-` 场景意图；Case 落实步骤和可判定预期。
2. **业务定义与执行实现分离。** Case 不包含执行器 DSL；Flow 和 Module 可以承载可替换的执行实现。
3. **资产必须可追溯。** Flow、Journey、报告和 Artifact 都应能追溯到稳定 Case ID。
4. **目录表达业务，Tag 表达属性。** 目录按领域和功能组织；范围、类型、优先级、平台使用 Tag。
5. **数据、环境与逻辑分离。** data 脚本描述业务数据结构，环境变量提供敏感值，Flow 描述执行逻辑。
6. **源资产与派生产物分离。** `generated/` 和 `artifacts/` 中的内容不能反向成为测试定义。

## 3. 资产模型

| 资产 | 位置 | 职责 | 是否源资产 | 主要维护者 |
| --- | --- | --- | --- | --- |
| Design | `designs/` | 模块 Index + 场景 TDS：范围、公共规则、风险、场景意图 | 是 | 测试人员、产品、AI Agent |
| Case | `cases/` | 定义测试目标、步骤和预期结果 | 是 | 测试人员、产品、AI Agent |
| Flow | `flows/` | 实现一个 Case 场景的执行流程 | 是 | 自动化维护者、AI Agent |
| Module | `modules/` | 封装可复用的执行操作 | 是 | 自动化维护者 |
| Journey | `journeys/` | 组合跨功能业务链路 | 是 | 测试人员、自动化维护者 |
| Data | `data/` | 定义 JavaScript Object 业务测试数据 | 是 | 测试人员 |
| Environment | `env/` | 声明环境变量模板 | 模板是 | 环境维护者 |
| Generated | `generated/` | 保存派生文档、汇总及 OpenAPI 待审查草稿 | 否 | 自动生成 |
| Artifact | `artifacts/` | 保存日志、截图和执行报告 | 否 | 执行器、CI |
| Skill | `skills/` | 定义模型如何设计、生成、执行、审查和分析 | 是 | 测试平台维护者 |
| Script | `scripts/` | 执行确定性校验、命令和报告收集 | 是 | 自动化维护者 |

## 4. 资产关系

```text
PRD / PDD
      ↓
   Design（模块 Index → 场景 TDS）
      ↓
    Case ──────────────→ generated/docs
      ↓
    Flow ──→ Module
      ↓         ↑
   Journey ─────┘
      ↓
    执行器 ← data + Environment
      ↓
  Artifact / generated/reports
```

当业务要求发生变化时，从 Design 到 Case 再向下同步；不要先修改执行脚本再反向猜测 Case。
OpenAPI 只提供接口契约，可先用 `test:openapi-import` 生成独立草稿；业务预期确认后再进入正式 TDS/Case/Flow。

## 5. 目录与命名规则

```text
designs/{domain}/index.md
designs/{domain}/{scene}.design.md
cases/{domain}/{feature}.case.md
flows/{domain}/{feature}/{case-id}.yaml
modules/{domain}/{action}.yaml
journeys/{business-goal}.yaml
data/{domain}/{business-object}.js
```

- `{domain}`、`{feature}`、`{action}` 使用小写短横线命名。
- Case ID 使用 `TC-{DOMAIN}-{FEATURE}-{NUMBER}`，其中领域和功能使用大写。
- 文件和目录不得以执行工具、测试范围、优先级或人员姓名命名。
- `smoke`、`regression`、`positive`、`p0` 等属性只通过 Tag 表达。

## 6. 标准工作流程

### 6.1 新增功能测试

1. 阅读 PRD、PDD 和已存在的相关 TDS、Case。
2. 创建或更新模块 Index，再编写对应场景 TDS，明确范围、风险与 `DS-` 场景意图。
3. 场景 TDS 评审通过后，创建或更新一个功能级 Case，覆盖正向和反向场景。
4. 评审 Case 的完整性、可执行性和预期结果。
5. 查询并复用已有 Module；必要时新增公共操作。
6. 为每个 Case ID 创建一个对应 Flow。
7. 准备 data 脚本和环境变量模板，不提交真实值。
8. 运行 `./scripts/validate-cases.sh`。
9. 独立运行新增 Flow，再运行受影响的 Smoke/Regression 范围。
10. TDS、Case、Flow、Module、data 脚本和规范变更放在同一提交或同一评审中。

需要语义理解和模型生成时依次使用 `test:design`、`test:case`、`test:flow`；脚本不负责从 Case 自主推导 Flow。执行、审查和失败分析分别使用 `test:execution`、`test:review`、`test:analysis`，详细边界见 [`../skills/README.md`](../skills/README.md)。

### 6.2 修改已有测试

1. 先判断变化来自业务要求、执行实现、测试数据还是运行环境。
2. 业务变化先改 TDS（Index / 场景）再改 Case；仅执行器变化时通常只改 Flow/Module。
3. 搜索受影响的 Case ID、Module 和变量引用。
4. 同步更新所有下游资产并重新校验。
5. 保留原 Case ID 的业务含义；若测试意图发生根本变化，应创建新 ID。

### 6.3 删除测试

1. 在评审中说明删除原因和替代覆盖。
2. 同时删除对应 Flow，并更新引用该 ID 的 Journey 和报告配置。
3. 不把已删除的 ID 重新分配给其他用例。

## 7. Tag 使用规则

| 维度 | 允许值 | 说明 |
| --- | --- | --- |
| 业务领域 | `auth`、`meeting`、`knowledge`、`user`、`settings` | 与目录领域一致 |
| 范围 | `smoke`、`regression`、`e2e` | 可同时属于多个范围 |
| 类型 | `positive`、`negative`、`boundary`、`exception` | Flow 应明确一种主要类型 |
| 优先级 | `p0`、`p1`、`p2` | 按业务风险确定 |
| 平台 | `api`、`web`、`android`、`ios` | 仅在平台相关时使用 |

新增 Tag 前先更新 `config.yaml` 和相关规范，避免同义词分裂统计口径。

## 8. 质量门禁

提交前至少完成：

- Case 的 Front Matter、必要章节、ID 格式和唯一性检查；
- Case ID 与 Flow 文件一一对应；
- Flow 可独立执行并包含明确结果判断；
- Module、data 脚本和环境变量引用有效；
- 真实凭据、日志、截图和报告没有进入 Git；
- 相关 README 和标准与实际结构一致；
- `./scripts/validate-cases.sh`、全部 Shell 语法检查和相关脚本测试通过。

## 9. 变更影响判断

| 变化类型 | 必须检查或修改的资产 |
| --- | --- |
| 验收标准变化 | Design、Case、Flow、Journey、生成文档 |
| 页面或接口实现变化 | Flow、Module、selector data，必要时环境变量 |
| 公共操作变化 | Module 及全部引用它的 Flow/Journey |
| 测试数据变化 | data 脚本、环境模板及引用者 |
| 更换执行器 | Flow、Module、执行脚本、CI；Case 原则上不变 |
| 新增业务领域 | `config.yaml`、业务目录、相关 README/规范 |

## 10. 评审清单

- 测试意图是否来自明确需求，边界和异常是否与风险匹配？
- 每个步骤是否无需猜测即可执行，每个预期是否可观察或可计算？
- 资产是否放在正确层级，有无重复步骤应该抽为 Module？
- ID、路径、Tag 和变量是否符合约定？
- 失败结果能否追溯到 Case，并提供足够诊断信息？
- 变更是否引入敏感数据或具体执行工具对资产模型的污染？

## 11. 相关规范

- [`skills/test-design/references/tds-spec.md`](../skills/test-design/references/tds-spec.md)：TDS 分层、Front Matter、编号与写法（`test:design` Skill）。
- [`case-standard.md`](case-standard.md)：Case 字段、DS→TC 映射与写法（`test:case` Skill，见 `skills/test-case/`）。
- [`flow-standard.md`](flow-standard.md)：Flow 结构、映射与执行要求。
- [`module-standard.md`](module-standard.md)：公共操作抽取和兼容性规则。
- [`journey-standard.md`](journey-standard.md)：跨功能链路设计规则。
- [`data-env-standard.md`](data-env-standard.md)：数据和环境变量管理。
- [`maestro-guide.md`](maestro-guide.md)：当前 Android/iOS 执行层、构建顺序和实践。
- [`ai-agent-guide.md`](ai-agent-guide.md)：AI Agent 的允许行为和交付要求。

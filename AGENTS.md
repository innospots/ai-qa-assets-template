# 测试资产仓库 Agent 工作规范

Agent 在本仓库创建、修改、执行和分析测试资产时的**强制规则**。详细协作流程、允许/禁止行为与自检清单见 [`docs/ai-agent-guide.md`](docs/ai-agent-guide.md)。

## 1. 适用范围

本文件适用于在本仓库中进行测试设计、Case/Flow 维护、执行、审查、分析和文档更新的 AI Agent。

- 子目录可放置更具体的 `AGENTS.md`，作为**增量规则**；与根文件冲突时，以**更靠近所编辑文件**的子目录规则为准，根规则其余部分仍有效。
- 子目录没有更具体的 `AGENTS.md` 时，全部遵循本文件。

## 2. 开始前阅读

按任务类型加载上下文，避免跳过 Skill 或规范直接改资产：

| 顺序 | 内容 | 路径 |
| --- | --- | --- |
| 1 | 工程入口与主链路 | [`README.md`](README.md) |
| 2 | 本文件（强制规则） | `AGENTS.md` |
| 3 | Agent 协作细则 | [`docs/ai-agent-guide.md`](docs/ai-agent-guide.md) |
| 4 | 资产总览 | [`docs/test-asset-guide.md`](docs/test-asset-guide.md) |
| 5 | 当前任务 Skill | [`skills/README.md`](skills/README.md) → 对应 `skills/*/SKILL.md` |

业务测试变更时，**先**读 `test:design`（[`skills/test-design/`](skills/test-design/)），再 `test:case` → `test:flow`；仅执行实现变化可跳过设计 Skill。

## 3. 资产链路与边界

```text
PRD / PDD
      ↓
Design（TDS：测什么、为什么测、覆盖与风险）
      ↓
Case（测试什么、预期是什么；可执行意图的唯一事实源）
      ↓
Flow（一个 Case 的执行实现）──→ Module（公共操作）
      ↓                              ↑
Journey（跨功能目标）───────────────┘
      ↓
执行器 ← data（业务数据/选择器）+ env（环境/敏感值）
      ↓
Artifact（运行结果）
```

**不可破坏：**

- 一个 Case ID 只对应一个正式 Flow；Case ID 不因工具、排序或平台变化而改变。
- Case 不包含 Maestro、pytest 或 Playwright DSL。工具实现只进入 Flow 清单、`executors/`、Module、Journey、脚本和执行配置。
- API/Web 的 Flow 文件为**执行清单**（`executor`、`tags`、`test`）；Mobile 的 Flow 为 Maestro YAML。
- TDS 只写入 `designs/`，不写逐步操作、Case/Flow 内容或下游资产模板；规范在 `skills/test-design/`。
- `data/` 使用 JavaScript Object 保存结构化业务数据和平台选择器；Mobile Flow 通过 `runScript` 按需加载，再以 `${output.<层级>}` 引用。API/Web 的 pytest 实现须显式说明数据来源。
- `env/` 只保存应用、设备、环境地址和敏感值的模板。业务数据、页面文案和选择器不得塞入 env。
- `generated/`、`artifacts/` 是派生产物，不能作为测试意图的唯一来源，也不得提交真实凭据。

## 4. 事实来源与冲突处理

按以下优先级理解和修改资产：

1. 用户当前任务中的明确要求；
2. 已批准的需求、验收标准和产品规范（PRD/PDD）；
3. `designs/` 中的 TDS（模块 Index、场景文档、`DS-` 意图与范围）；
4. `cases/` 中的 Case 源资产（可执行测试意图的唯一事实源）；
5. 本文件、`docs/` 规范和各目录 README；
6. `flows/`、`modules/`、`journeys/`、`data/` 中的执行实现；
7. 日志、报告、截图和实际页面行为。

低优先级来源不得覆盖高优先级规则。`designs/` 与 `cases/` 冲突且会改变业务范围、预期或风险时，停止扩大修改并报告冲突；不要根据当前 UI 偶然行为反向改写 Case 或 TDS。

## 5. Skill 与脚本分工

需要模型理解、取舍或生成时使用对应测试 Skill：

| 任务 | Skill | 主要结果 | 关键约束 |
| --- | --- | --- | --- |
| 风险与覆盖设计 | `test:design`（`skills/test-design/`） | `designs/{domain}/index.md` 与 `designs/**/*.design.md` | 先 `using-superpowers` 拆任务；逐份生成 + `references/review-checklist.md` 审查；无文档时用 `references/guided-intake.md` 引导 |
| 从 OpenAPI 导入 API 草稿 | `test:openapi-import`（`skills/test-openapi-import/`） | `generated/openapi-drafts/` | 仅提取接口契约；业务预期确认后才进入正式 TDS/Case/Flow |
| Case 创建/修改 | `test:case`（`skills/test-case/`） | `cases/**/*.case.md` | 追溯 TDS `DS-`；不写 Flow DSL |
| 从 Case 实现 Flow | `test:flow`（`skills/test-flow/`） | Flow、必要的 Module/data 引用 | 一 Case 一 Flow |
| 运行测试 | `test:execution`（`skills/test-execution/`） | Artifact 与执行摘要 | API/Web：`scripts/api`、`scripts/web`；Mobile：`scripts/maestro`；默认 Smoke：`scripts/run-smoke.sh` |
| 资产审查 | `test:review`（`skills/test-review/`） | 问题与风险清单 | — |
| 失败分析 | `test:analysis`（`skills/test-analysis/`） | 证据、归因和建议 | 事实与推断分开 |
| Skill 目录规范 | `skill:authoring`（`skills/skill-authoring/`） | 新 Skill 结构与审查 | 见 `references/skill-structure-spec.md` |

Shell/Python 脚本只承担参数明确、结果确定的校验、执行和报告收集。正式执行入口是 `scripts/`；`python_runner` 由这些脚本调用，负责 Maestro 编排与汇总报告。`generate-flows.sh`、`generate-docs.sh` 是旧 CI 兼容入口，不是正式 AI 生成入口；不得在脚本中加入提示词编排或模型决策。

## 6. 按任务类型执行

### 新增或变更业务测试

1. 阅读需求、相关 TDS/Case 和对应规范。
2. **先**更新 TDS（模块 Index 与场景文档），**再**更新 Case，然后更新下游 Flow/Journey。存量 TDS 结构不符合规范时，用 `test:design` 做对齐（保留 `DS-` 意图；见 `skills/test-design/references/tds-spec.md` §12）。
3. `test:design` 禁止一次性生成整个模块的全部 TDS；须 Index → 各场景逐份生成并审查。
4. 搜索并复用已有 Module 和 data 数据集。
5. 为每个 Case ID 维护一个可独立执行、可判断结果的 Flow。
6. 运行结构校验和最小相关测试，再扩大到受影响范围。

### 仅修改执行实现

若业务意图和预期不变，可只修改 Flow、Module、data 或脚本；交付时说明为什么不需要修改 TDS/Case。修改共享 Module 或 data 前，先查询全部引用者。

### 执行与分析

执行前确认平台、环境文件、设备和测试范围。分析失败时依次区分产品缺陷、测试资产缺陷、环境问题和执行器问题；事实与推断分开陈述，不为让测试通过而降低 Case 预期。

### 文档变更

先更新最具体的规范（Skill 内 `references/` 优先于 `docs/` 跳转），再同步根 README、目录 README、命令示例和检查清单。`docs/superpowers/` 是历史设计与实施记录，除非任务明确要求，不用当前实现反向重写历史记录。

## 7. 数据与变量规则

- 数据文件：`data/{domain}/{business-object}.js`。
- 数据脚本增量写入 `output`，例如 `output.auth = output.auth || {}`，不得覆盖其他已加载域。
- 引用层级必须与 Object 层级一致，例如 `${output.data.users.insertUsers.records}`。
- Mobile Flow 只加载当前场景需要的数据文件；未执行 `runScript` 的数据不属于本次 Maestro 运行上下文。
- Android/iOS 共用业务数据，分别加载 `data/contracts/selectors/android.js` 或 `ios.js`。
- 密码、Token 等敏感字段由 data 脚本读取 env/CI Secret；禁止打印、提交或写入 Artifact。
- 本次执行产生的 ID、Token 或临时值写入 `output.runtime`，不得回写静态数据文件。

## 8. 文件与脚本维护规则

- 保留用户已有和不相关的工作区修改，不擅自回退、覆盖或清理。
- 搜索文件和引用优先使用 `rg`；路径、命令和示例必须能在当前仓库中找到。
- Shell 脚本使用 `set -euo pipefail`，从脚本自身位置解析仓库根目录，失败时返回非 0。
- 新增或修改脚本时补充中文用途、参数、输出和关键限制注释。
- 尚未实现完整能力的脚本必须保留明确注释：`# TODO: [待完善] <缺失能力、完成条件>`，文档不得把它描述为已完成。
- 禁止硬编码真实账号、密码、Token、生产地址、设备 ID 或个人信息。

## 9. 禁止行为（摘要）

完整列表见 [`docs/ai-agent-guide.md` §8](docs/ai-agent-guide.md)。核心禁止项：

- 跳过 TDS/Case，直接把自动化实现当作测试设计或测试定义；
- 根据 UI 偶然行为反向补写未经确认的业务规则；
- 更改稳定 Case ID 或已发布 `DS-` 编号来适配工具或排序；
- 将 Maestro 等执行器 DSL 写入 Case 或 TDS；
- 保存、输出或提交真实凭据与生产数据；
- 为通过测试而降低、删除或改写 Case/TDS 预期；
- 在未说明的情况下扩大到其他业务领域或做破坏性清理。

## 10. 最低验证要求

根据变更范围执行适用命令：

```bash
./scripts/validate-cases.sh
bash -n scripts/*.sh scripts/api/*.sh scripts/web/*.sh scripts/lib/*.sh scripts/maestro/*.sh scripts/tests/*.sh
bash scripts/tests/test-maestro-scripts.sh
bash scripts/tests/test-executor-scripts.sh
python3 -m pytest -q scripts/tests/test_openapi_import.py scripts/tests/test_asset_validation.py
git diff --check
git status --short
```

修改 `data/**/*.js` 时还应执行：

```bash
find data -name '*.js' -type f -exec node --check {} \;
```

修改 Flow/Module/Journey 时，应至少运行直接受影响的单 Flow 及引用共享资产的范围。缺少 Maestro CLI、设备或真实环境时，不得声称端到端运行通过；应说明未执行原因并给出准确命令。

## 11. 交付要求

最终说明至少包含：

- 修改了哪些源资产和规范；
- TDS、`DS-`、Case、Flow、Module、data 之间的关键追溯或影响；
- 实际执行的校验及结果；
- 未执行项、已知 TODO 和后续动作；
- 是否新增 env 变量、共享资产或敏感配置要求。

避免只报告「已完成」；交付信息应让评审者不阅读全部差异也能判断变更范围和风险。

## 12. 延伸阅读

| 主题 | 文档 |
| --- | --- |
| 资产模型与质量门禁 | [`docs/test-asset-guide.md`](docs/test-asset-guide.md) |
| TDS 规范与样例 | [`skills/test-design/`](skills/test-design/) |
| Case / Flow / Module / Journey | [`skills/test-case/references/test-case-spec.md`](skills/test-case/references/test-case-spec.md) 等专项规范 |
| Maestro 执行实践 | [`docs/maestro-guide.md`](docs/maestro-guide.md) |
| Skill 列表与调用顺序 | [`skills/README.md`](skills/README.md) |
| 规范索引 | [`docs/README.md`](docs/README.md) |

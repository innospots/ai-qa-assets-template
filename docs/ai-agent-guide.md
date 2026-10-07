# AI Agent 协作指南

## 1. 目的

本指南规定 AI Agent 创建、修改、执行和分析测试资产时的输入、允许行为、禁止行为、验证要求和交付格式。目标是让 Agent 提高效率，同时保持 Case 优先、资产可追溯和结果可审查。

## 2. 事实来源优先级

Agent 应按以下顺序理解任务：

1. 用户在当前任务中的明确要求；
2. 已批准的需求、验收标准和产品规范；
3. `designs/` 中的 TDS 与 `DS-` 意图；
4. `cases/` 中现有 Case；
5. 根目录 `AGENTS.md`、`docs/` 和各目录 README 中的资产规范；
6. `flows/`、`modules/`、`data/` 中的现有实现；
7. 页面、接口、日志和 Artifact 中观察到的行为。

观察结果可用于发现实现差异和提出建议，不能绕过 Case 直接定义新的业务要求。来源之间冲突时停止扩大变更，明确列出冲突并请求决策。

## 3. 标准处理流程

```text
读取任务与规范
   ↓
定位对应 TDS、DS 意图、Case 和 Case ID
   ↓
判断是业务变化还是执行实现变化
   ↓
查询现有 Module、data 脚本、环境变量和引用关系
   ↓
创建或更新资产
   ↓
校验 Case/Flow 映射和敏感信息
   ↓
执行最小相关测试，再执行受影响范围
   ↓
分析 Artifact 并报告结果
```

需要模型理解或生成时使用对应 Skill：OpenAPI 草稿导入用 `test:openapi-import`，设计用 `test:design`，Case 用 `test:case`，Flow 用 `test:flow`，执行用 `test:execution`，审查用 `test:review`，失败分析用 `test:analysis`。脚本只负责确定性转换、校验、执行和报告收集。

## 4. 新增 Case 的规则

Agent 必须有明确需求或用户授权，才能新增测试意图。新增时：

- 一个功能创建一个 Case 文件；
- 至少覆盖核心正向和高风险反向场景；
- 步骤使用业务语言，预期结果必须可判定；
- 使用未占用且符合分类区间的 ID；
- 不从当前 UI 偶然行为推断产品永久规则；
- 不自动填入真实账号、密码或环境地址。

需求不完整但不影响主体设计时，Agent 可采用最小、明确的假设，并在交付说明中列出。会改变业务范围或风险判断的缺失信息必须交由用户决定。

## 5. 生成或更新 Flow 的规则

1. 逐场景读取 Case 的步骤和预期结果。
2. 搜索 `modules/`，优先复用已有公共操作。
3. 搜索 `data/` 和 `env/*.env.example`：复用结构化数据、选择器及真正的环境变量。
4. 一个 Case ID 创建一个 Flow 文件，路径和文件名严格对应。
5. 保留业务、范围、类型、优先级 Tag。
6. 对 Case 的每项关键预期提供等价可执行判断。
7. 确保 Flow 可独立准备状态、运行、失败和重试。

如果执行器能力不足以验证某项预期，Agent 应明确标记缺口并说明需要人工验证或扩展执行能力，不能静默删除预期。

## 6. Module 与 data 脚本处理

- 相同操作在多个位置重复时，Agent 可提取 Module；提取前检查职责和全部引用者。
- 修改共享 Module 必须回归所有直接引用的 Flow/Journey。
- data 脚本只保存结构、业务数据名称和非敏感值。
- Mobile 入口 Flow 通过 `runScript` 加载所需 data，并以 `${output...}` 使用；Module 不隐式加载调用方数据。API/Web 的数据读取由 executor 实现并与 Case 数据集对齐。
- 选择器位于 `data/contracts/selectors/`，不放入 env 文件。
- 新增环境变量时同步更新适用的 `env/*.env.example`，真实值留空。
- 不为了减少文件数量而把不相关业务操作合并到同一 Module。

## 7. 允许行为

在用户授权的测试资产范围内，Agent 可以：

- 读取需求、Case、规范、代码和运行产物；
- 创建或修改 Case、Flow、Module、Journey、data 脚本、模板及文档；
- 运行只读校验和用户授权的测试命令；
- 根据失败信息定位 Case、Flow 或 Module 的不一致；
- 提出新的覆盖建议，但应区分“已实现”和“建议新增”。

## 8. 禁止行为

Agent 不得：

- 仅根据 UI 或现有脚本反向补写未经确认的业务规则；
- 跳过 Case，直接把自动化实现当作测试设计；
- 更改稳定 Case ID 来适配执行器或排序；
- 将具体工具名称写入目录、Case ID、业务分类或通用规范名称；
- 保存或输出真实密码、Token、Cookie、API Key 和生产数据；
- 为通过测试而降低、删除或改写 Case 预期结果；
- 在未说明的情况下扩大到其他业务领域或执行破坏性清理；
- 把生成文件和 Artifact 当作人工长期维护的源资产。

## 9. 验证要求

完成变更前至少执行：

```bash
./scripts/validate-cases.sh
bash -n scripts/*.sh scripts/api/*.sh scripts/web/*.sh scripts/lib/*.sh scripts/maestro/*.sh scripts/tests/*.sh
bash scripts/tests/test-maestro-scripts.sh
bash scripts/tests/test-executor-scripts.sh
python3 -m pytest -q scripts/tests/test_openapi_import.py scripts/tests/test_asset_validation.py
git diff --check
git status --short
```

若变更 Flow/Module/Journey，还应运行：

1. 直接受影响的单个 Flow；
2. 引用已修改 Module 的所有 Flow/Journey；
3. 对应 Smoke 或 Regression 范围。

无法运行时，Agent 必须说明未验证项目、原因和用户可执行的准确命令。

若脚本能力尚不完整，必须确认脚本包含 `TODO: [待完善]`，并在交付中把缺失能力列为限制；不得用文档把占位脚本描述成已完成实现。

## 10. Artifact 分析

Agent 分析失败时依次确认：

1. Case 预期是否明确且仍然有效；
2. Flow 是否忠实实现 Case；
3. Module、data 脚本和环境变量是否正确；
4. 失败属于产品缺陷、资产缺陷、环境问题还是执行器问题；
5. 日志、报告或截图是否足以支持结论。

结论必须区分事实与推断。不要仅凭单次截图断言根因，也不要在没有证据时修改 Case。

## 11. 交付说明

Agent 的最终交付至少包含：

- 创建或修改了哪些资产；
- 主要测试覆盖和追溯关系；
- 执行了哪些校验或测试及结果；
- 未执行项目、已知限制和后续动作；
- 是否涉及新变量、共享 Module 或规范变化。

避免只报告“已完成”。交付信息应让评审者不阅读全部差异也能判断变更范围和风险。

## 12. 自检清单

- 变更是否由明确 Case 或批准需求驱动？
- Case、Flow 和文件路径是否一一对应？
- 是否复用已有 Module，且共享变更已检查全部引用者？
- 是否没有降低业务预期或引入未经确认的假设？
- 是否没有敏感信息、生产数据和执行工具耦合？
- 验证结果是否真实、最新并在交付说明中完整呈现？

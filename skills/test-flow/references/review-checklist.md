# Flow 生成后审查清单

## 追溯与结构

- [ ] 一个 Main Flow 对应一个 Case 测试 ID
- [ ] 路径 `flows/{domain}/{scene}/{case-id}.yaml` 与 [repo-conventions.md](repo-conventions.md) 一致
- [ ] `name` 以 Case ID 开头
- [ ] API/Web 有 `executor`、`name`、`tags`、`test`，`test` 指向存在的 pytest 节点
- [ ] Mobile Header 与 Commands 有 `---` 分隔，`appId` 来自 env
- [ ] `tags` 与 Case 执行范围一致

## Case 对齐

- [ ] 步骤顺序与 Case 一致（未擅自增删业务步骤）
- [ ] 每个关键预期在 API/Web pytest 或 Mobile Maestro 中有等价断言
- [ ] 未降低/删除 Case 预期以通过执行
- [ ] Case 信息不足时已报告而非臆造

## 数据

- [ ] 业务值在 `data/`；Mobile Flow 用 `${output...}` 或 `runFlow.env`
- [ ] 无硬编码密码、Token、生产地址
- [ ] Mobile `runScript` 只加载本场景需要的 data 文件
- [ ] `output.<domain>` 命名空间正确

## Module / Subflow

- [ ] Mobile 重复操作已按需复用 `modules/`
- [ ] Module 单一职责，非「一步一文件」
- [ ] Module 不含 Case 级最终业务结论（错误密码 Flow 也能复用登录 Module）
- [ ] 修改共享 Module 前已查全部引用者

## Mobile Selector

- [ ] 优先 id / 稳定 text（见 [selector-guide.md](selector-guide.md)）
- [ ] 未滥用 `point` / `index`（有理由则注释说明）
- [ ] 平台差异在 selector data 或平台 Module

## Mobile 控制流

- [ ] `when` 仅用于平台/合法分支，不掩盖失败（见 [control-flow-guide.md](control-flow-guide.md)）
- [ ] 无无边界 `retry` / `repeat`
- [ ] 等待优先 Assertion，`extendedWaitUntil` 有 timeout 理由

## Mobile JavaScript

- [ ] 优先 YAML；JS 仅数据/计算/API（见 [javascript-guide.md](javascript-guide.md)）
- [ ] 未用大量 `runScript` 替代 UI 流程

## 脚本校验

- [ ] `python3 skills/test-flow/scripts/validate-flow.py <flow>` 通过
- [ ] Mobile 的 `python3 skills/test-flow/scripts/check-references.py <flow>` 通过
- [ ] `./scripts/validate-cases.sh` 通过（全量 Case 时）

## 交接

- [ ] 列出待人工审核差异
- [ ] 未未经审核覆盖共享 Module

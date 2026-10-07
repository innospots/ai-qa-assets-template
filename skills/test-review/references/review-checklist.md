# 测试资产审查清单

默认**只读**；除非用户明确要求修复，不修改文件。

## 规范来源

- [`docs/design-standard.md`](../../../docs/design-standard.md)
- [`docs/case-standard.md`](../../../docs/case-standard.md)
- [`docs/flow-standard.md`](../../../docs/flow-standard.md)
- [`test-design/references/tds-spec.md`](../../test-design/references/tds-spec.md)
- [`test-case/references/test-case-spec.md`](../../test-case/references/test-case-spec.md)

## Design（TDS）

- [ ] 模块有 `index.md`
- [ ] 场景 TDS 含 Front Matter（`kind` / `inherits`）
- [ ] 章节符合 tds-spec；`DS-` 意图清晰
- [ ] 无逐步操作、Case/Flow 内容

## Case

- [ ] 一场景一 Case 文件
- [ ] `DS-` → `TC-` 追溯完整
- [ ] 步骤明确、预期可判定、ID 唯一
- [ ] 含 `## 正向测试`、`## 反向测试`

## Flow

- [ ] 每个 Case 测试 ID 有且仅有一个 Flow
- [ ] API/Web 清单含 `executor`、`name`、`tags`、`test`，pytest 节点存在
- [ ] Mobile Flow 含 Maestro 命令与断言
- [ ] 关键预期有等价断言；Tag 与 Case 一致

## Module / Data

- [ ] 公共操作已复用；共享修改已查引用者
- [ ] Mobile data 经 `runScript` 按需加载；`${output...}` 路径存在
- [ ] API/Web 的环境地址与业务数据来源清晰，未将业务值混入 env
- [ ] 无执行逻辑、无敏感值硬编码

## 平台与覆盖

- [ ] Android/iOS 共用业务 Flow；差异在 selector / 平台 Module
- [ ] API/Web 跨业务域 Flow 能通过 `executor` 被套件发现
- [ ] 覆盖：`已实现 Flow 数 / Case 测试 ID 数`；列出缺失、孤立、重复

## 输出格式

按严重程度：问题、证据文件、影响、建议；区分必须修复 / 建议优化 / 需业务确认。

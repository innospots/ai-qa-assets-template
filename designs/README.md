# Design（TDS）

测试设计说明：覆盖范围、风险与 `DS-` 场景意图。TDS 不编写逐步操作或执行 DSL。

## 示范模块

- [`api/`](api/) — HTTP 接口
- [`web/`](web/) — Web UI
- [`mobile/`](mobile/) — 客户端（Maestro）

新建产品域时在 `designs/{domain}/` 增加 `index.md` 与 `*.design.md`。使用 Skill `test:design` 维护结构。

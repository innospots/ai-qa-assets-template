# Case 目录

一个业务特性对应一个 `{feature}.case.md`。Case 是测试意图的**唯一事实源**，不得写入 Maestro、pytest 或 Playwright DSL。

## 示范布局

```text
cases/
├── api/health.case.md
├── web/home.case.md
└── mobile/demo.case.md
```

## 规范

- Case ID 格式：`TC-{DOMAIN}-{FEATURE}-{NUMBER}`（见 `config.yaml`）
- 必填 Front Matter：`id`、`name`、`module`、`priority`、`tags`、`platform`
- 必填章节：`## 正向测试`、`## 反向测试`

校验：`./scripts/validate-cases.sh`

详细标准：[`docs/case-standard.md`](../docs/case-standard.md)

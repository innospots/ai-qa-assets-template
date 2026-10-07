# Case 生成后审查清单

## Front Matter 与结构

- [ ] 必填字段完整；`source.tds` 正确
- [ ] 存在 `## 正向测试`、`## 反向测试`
- [ ] 存在 `## 测试数据` 表（或等价说明）
- [ ] `validate-cases.sh` 通过

## 数据（对齐 data Object 与 Case 数据集）

- [ ] 具体值只在 `data/{domain}/*.js`，Case 无硬编码
- [ ] data 脚本使用 `output.<domain> = output.<domain> || {}`
- [ ] 数据集名有业务含义；二进制走 `fixtures/` + `path`
- [ ] Case 表/步骤引用的名称在 data 中存在
- [ ] 未使用 JSONPath `$.…` 或独立 JSON 作为主数据
- [ ] 改 data 后 `node --check` 通过

## TDS 与 TC 质量

- [ ] 每条 TC 可追溯 `DS-`
- [ ] 覆盖表完整；Deferred 项明确
- [ ] 步骤为业务动作；预期可判定
- [ ] 反向/边界遵循控制变量

## 交接

- [ ] 列出待生成 Flow
- [ ] 未擅自改 flows/modules

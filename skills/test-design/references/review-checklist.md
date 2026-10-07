# TDS 生成后审查清单

每份文档**生成完成后、进入下一份之前**必须逐项核对。有问题先修正，再标记该任务完成。

## 通用

- [ ] 路径在 `designs/{domain}/`，未写入 `docs/` 或 `skills/`
- [ ] YAML Front Matter 完整；无真实凭据、环境地址、执行器名称
- [ ] `sources` 能追溯到 PRD/PDD/产品功能文档条目
- [ ] 无逐步操作、逐步预期、Case/Flow/Maestro 内容
- [ ] 无「Case 生成指引」「建议 TC」等下游资产写法
- [ ] 待确认问题已列出，未关闭项在清单中标注暂缓

## 模块 Index（`index.md`）

- [ ] `kind: index`；`id` 为 `{DOMAIN}-DESIGN`
- [ ] §1–§13 结构符合 [`tds-spec.md`](tds-spec.md) 第 9 节；未展开具体 `DS-` 测试点
- [ ] 公共规则、角色、状态、公共数据只维护一份
- [ ] §10 场景清单链接正确，覆盖本模块全部场景 TDS
- [ ] 与 [`../examples/customer-index.md`](../examples/customer-index.md) 层级一致

## 场景 TDS（`{scene}.design.md`）

- [ ] `kind: scene`；`inherits` 指向模块 Index 的 `id`；`scene` 与文件名一致
- [ ] 正文开头有 Index 继承引用，未复制 Index 公共规则全文
- [ ] §1–§12 结构符合 [`tds-spec.md`](tds-spec.md) 第 10 节；无内容的小节已删除
- [ ] §7 测试设计与 §9 测试场景清单一致；边界写出具体值
- [ ] `DS-` 编号符合区间；已发布 ID 未无故重编号
- [ ] 同构正向未拆多条 `DS-`；故障注入标为专项/暂缓
- [ ] 与 [`../examples/customer-create-customer-tds.md`](../examples/customer-create-customer-tds.md) 层级一致

## 模块级收尾

- [ ] Index 场景清单与磁盘上 `.design.md` 文件一一对应
- [ ] 跨场景公共规则只在 Index，场景无重复粘贴
- [ ] 高风险项均有 `DS-`；PRD/PDD 关键条目在清单中可追溯

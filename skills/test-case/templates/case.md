---
domain: {DOMAIN}
scene: {scene}
title: {场景名称}
design: designs/{domain}/{scene}.design.md
version: 0.1.0
status: draft
---

# {场景名称}

> 本文件基于 `{SCENE-DESIGN-ID}` 生成。数据见 `data/{domain}/`。

## 文档信息

| 项 | 值 |
| --- | --- |
| Case 文件 | cases/{domain}/{scene}.case.md |
| 设计文档 | designs/{domain}/{scene}.design.md |
| 版本 | 0.1.0 |

## 测试数据

| 数据集 | 脚本 | 说明 |
| --- | --- | --- |
| | data/{domain}/xxx.js | |

Flow 加载 `data/{domain}/xxx.js` 后引用 `${output.{domain}.xxx.yyy}`。

## 正向测试

### TC-{DOMAIN}-{SCENE}-001-001

- **追溯**: DS-{DOMAIN}-{SCENE}-001
- **优先级**: P0
- **标签**: smoke, regression, positive

**前置条件**

- 

**步骤**

1. 

**预期结果**

- 

## 反向测试

### TC-{DOMAIN}-{SCENE}-002-001

- **追溯**: DS-{DOMAIN}-{SCENE}-002
- **优先级**: P1
- **标签**: regression, negative

**前置条件**

- 

**步骤**

1. 

**预期结果**

- 

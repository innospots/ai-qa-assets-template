---
id: API-HEALTH-DESIGN
name: API 健康检查设计
module: api
priority: P0
---

# API 健康检查

## 1. 目标

确认服务对外探测路径可用，并对明显错误路径返回可观测失败。

## 2. 场景意图

| DS ID | 意图 | 覆盖 |
| --- | --- | --- |
| DS-API-HEALTH-001 | 探测路径 2xx | Smoke / Regression |
| DS-API-HEALTH-101 | 不存在路径 404 | Regression |

## 3. 风险与假设

- 依赖 `API_BASE_URL` 指向可访问环境；生产探测需单独策略。

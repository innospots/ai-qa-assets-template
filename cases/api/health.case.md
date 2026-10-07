---
id: API-HEALTH
name: API 健康检查
module: api
scene: health
source:
  tds: API-HEALTH-DESIGN
priority: P0
tags:
  - api
  - smoke
  - regression
platform:
  - api
---

# API 健康检查

> 示范 Case：HTTP 接口可达性与错误状态。数据见 [`data/api/`](../../data/api/).

## 测试用例清单

| Case ID | TDS 场景 | 测试用例 | 类型 | 优先级 |
| --- | --- | --- | --- | --- |
| TC-API-HEALTH-001 | DS-API-HEALTH-001 | GET 探测返回 2xx | 正向 | P0 |
| TC-API-HEALTH-101 | DS-API-HEALTH-101 | 请求不存在路径返回 404 | 反向 | P1 |

## 功能说明

验证 API 网关或后端在探测路径上返回预期 HTTP 状态。

## 前置条件

- `API_BASE_URL` 已在 `env/api.env` 或 CI 中配置。
- 网络可访问目标（或使用项目内 mock 服务）。

## 测试数据

| 数据 | 说明 |
| --- | --- |
| probePath | 正常探测路径，由目标环境的 `API_PROBE_PATH` 配置 |
| missingPath | 不存在路径，由目标环境的 `API_MISSING_PATH` 配置 |

## 正向测试

### TC-API-HEALTH-001 GET 探测返回 2xx

- **追溯**: DS-API-HEALTH-001
- **优先级**: P0

**步骤**

1. 对 `probePath` 发起 GET。

**预期结果**

- HTTP 状态码为 2xx。
- 响应体可解析（非空）。

## 反向测试

### TC-API-HEALTH-101 请求不存在路径返回 404

- **追溯**: DS-API-HEALTH-101
- **优先级**: P1

**步骤**

1. 对 `missingPath` 发起 GET。

**预期结果**

- HTTP 状态码为 404。

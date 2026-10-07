---
id: WEB-HOME
name: 站点首页
module: web
scene: home
source:
  tds: WEB-HOME-DESIGN
priority: P0
tags:
  - web
  - smoke
  - regression
platform:
  - web
---

# 站点首页

> 示范 Case：Web 页面标题与可见文案。数据见 [`data/web/`](../../data/web/).

## 测试用例清单

| Case ID | TDS 场景 | 测试用例 | 类型 | 优先级 |
| --- | --- | --- | --- | --- |
| TC-WEB-HOME-001 | DS-WEB-HOME-001 | 首页标题符合预期 | 正向 | P0 |
| TC-WEB-HOME-101 | DS-WEB-HOME-101 | 访问不存在路径显示 404 | 反向 | P1 |

## 功能说明

验证 Web 应用首页可访问且关键品牌文案可见。

## 前置条件

- `WEB_BASE_URL` 已配置。
- Playwright 浏览器依赖已安装（`playwright install chromium`）。

## 测试数据

| 数据 | 说明 |
| --- | --- |
| home | 首页路径与期望标题 `pages.home` |
| notFound | 404 路径 `pages.notFound` |

## 正向测试

### TC-WEB-HOME-001 首页标题符合预期

- **追溯**: DS-WEB-HOME-001
- **优先级**: P0

**步骤**

1. 打开 `home.path`。

**预期结果**

- 页面标题包含 `home.titleContains`。

## 反向测试

### TC-WEB-HOME-101 访问不存在路径显示 404

- **追溯**: DS-WEB-HOME-101
- **优先级**: P1

**步骤**

1. 打开 `notFound.path`。

**预期结果**

- HTTP 状态为 404，或页面出现 Not Found 类文案。

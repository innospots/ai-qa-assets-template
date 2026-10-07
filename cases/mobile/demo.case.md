---
id: MOBILE-DEMO
name: 客户端示范
module: mobile
scene: demo
source:
  tds: MOBILE-DEMO-DESIGN
priority: P1
tags:
  - mobile
  - smoke
platform:
  - android
  - ios
---

# 客户端示范

> 示范 Case：Maestro 启动应用并断言占位文案。执行见 `flows/mobile/demo/`。

## 测试用例清单

| Case ID | TDS 场景 | 测试用例 | 类型 | 优先级 |
| --- | --- | --- | --- | --- |
| TC-MOBILE-DEMO-001 | DS-MOBILE-DEMO-001 | 启动应用 | 正向 | P1 |
| TC-MOBILE-DEMO-101 | DS-MOBILE-DEMO-101 | 未登录时无首页内容 | 反向 | P2 |

## 功能说明

验证示例应用可被自动化启动；具体断言需按真实应用替换。

## 前置条件

- `APP_ID`、`MAESTRO_DEVICE` 已在 `env/android.env` 或 `env/ios.env` 中配置。
- 已安装 Maestro CLI 与目标模拟器/真机。

## 测试数据

| 数据 | 说明 |
| --- | --- |
| launch | 启动后期望可见文案 `selectors.launchHint` |

## 正向测试

### TC-MOBILE-DEMO-001 启动应用

- **追溯**: DS-MOBILE-DEMO-001
- **优先级**: P1

**步骤**

1. 启动应用。

**预期结果**

- 应用进程在前台。
- 可见 `launchHint` 文案（按项目替换）。

## 反向测试

### TC-MOBILE-DEMO-101 未登录时无首页内容

- **追溯**: DS-MOBILE-DEMO-101
- **优先级**: P2

**步骤**

1. 冷启动应用且未登录。

**预期结果**

- 不显示已登录首页专属内容（按项目定义）。

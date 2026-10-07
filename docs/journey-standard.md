# Journey 编写规范

## 1. 定义

Journey 验证跨越多个功能点的完整业务目标，例如“登录—创建会议—结束会议—查看纪要”。它组合已有 Case、Flow 或 Module，不替代单功能测试。

## 2. 位置与命名

```text
journeys/{business-goal}.yaml
```

文件名使用小写短横线，描述用户目标或业务结果，如 `login-to-home.yaml`、`meeting-full-process.yaml`。

## 3. 推荐结构

```yaml
appId: ${APP_ID}
name: J-AUTH-LOGIN-TO-HOME 登录进入首页
tags: [auth, e2e, positive, p0]
---
- runScript: ../data/auth/users.js
- runFlow:
    when:
      platform: Android
    commands:
      - runScript: ../data/contracts/selectors/android.js
- runFlow:
    when:
      platform: iOS
    commands:
      - runScript: ../data/contracts/selectors/ios.js
- runFlow: ../modules/app/launch.yaml
- runFlow:
    file: ../modules/auth/login.yaml
    env:
      USERNAME: ${output.auth.users.normal.username}
      PASSWORD: ${output.auth.users.normal.password}
- assertVisible:
    text: "${output.selectors.login.homeText}"
```

## 4. 设计规则

- Journey 名称或注释应说明直接验证的核心 Case ID，报告可以据此追溯。
- `runFlow` 优先组合已有 Module；缺少公共操作时先在 `modules/` 补齐。
- Maestro 断言描述完整链路最终业务结果，并在必要节点增加关键中间结果。
- Journey 不复制已有 Flow/Module 的全部底层步骤。
- Journey 通常标记为 `e2e`，是否加入常规回归取决于业务风险、稳定性和执行成本。

Android/iOS 共用相同 Journey；选择器差异通过条件加载平台 selector JS，系统操作差异通过平台 Module 处理。执行命令为 `./scripts/maestro/run-suite.sh <android|ios> e2e <env-file>`。

## 5. 前置、数据与清理

- 明确链路起始状态，避免依赖其他测试残留。
- Journey 是入口 Flow，必须自行加载链路所需的 data 和 selector 文件，不能依赖某个 Case Flow 已经运行。
- 为本次运行创建唯一数据，防止并行冲突。
- 对跨系统或长链路设置合理阶段信息，失败时指出具体节点。
- 测试结束后清理可清理数据；不可逆操作只能在隔离环境执行。

## 6. 何时不应创建 Journey

- 只验证一个功能或一个 Case 场景时，应使用 Flow。
- 仅为复用几步操作时，应创建 Module。
- 没有明确最终业务价值，只是把多个用例串行执行时，应使用执行计划或测试套件配置。

## 7. 更新与评审

业务链路变化时先更新相关 Case，再调整 Journey。评审时检查：

- 链路是否代表真实、重要的用户目标；
- 所有关联 Case ID 和 Module 路径有效；
- 是否可以从干净状态独立运行；
- 是否存在重复步骤、隐式依赖或无法清理的数据；
- 最终及关键中间结果是否可判定；
- 失败信息是否能定位到明确业务阶段。

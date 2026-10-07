# Maestro Android/iOS 构建与执行指南

## 1. 定位与边界

Maestro 是本仓库当前的 UI 自动化执行实现。它只进入 Flow、Module、Journey、执行配置、脚本和 CI；Case、Case ID、业务目录和测试意图继续保持工具无关。

官方文档入口：

- [Maestro Flow 结构](https://docs.maestro.dev/maestro-flows)
- [命令参考](https://docs.maestro.dev/reference)
- [官方示例](https://docs.maestro.dev/examples)
- [CLI 命令与参数](https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options)

## 2. 当前结构

```text
.maestro/config.yaml                 工作区发现与输出配置
flows/auth/login/*.yaml              五个可独立执行的登录 Case Flow
modules/app/launch.yaml              双平台共用启动入口
modules/app/prepare-android.yaml     Android 权限/系统状态示例
modules/app/prepare-ios.yaml         iOS 权限/系统状态示例
modules/auth/login.yaml              双平台共用登录动作
data/auth/users.js                   共用登录业务数据集
data/operations/users-batch.js       批量创建和查询业务数据集
data/contracts/selectors/*.js        Android/iOS 选择器契约
journeys/login-to-home.yaml          双平台共用 E2E Journey
env/android.env.example              Android 环境模板
env/ios.env.example                  iOS 环境模板
scripts/maestro/                     预检、单 Flow、套件与构建脚本
```

## 3. 哪些内容共用

以下内容应在 Android/iOS 间保持一致：

- Case 文件、Case ID、业务步骤和预期结果；
- Flow 的场景边界、名称、Tag 和关键断言；
- `normal`、`wrongPassword` 等 data 数据集名称；
- 登录、启动等业务 Module 的调用接口；
- Journey 的业务目标和追溯关系；
- 报告结构、构建顺序和质量门禁。

共用的前提是两端提供一致的 accessibility 语义。业务步骤一致但底层 ID 不同时，分别加载 Android/iOS selector JS，并统一通过 `${output.selectors...}` 引用。

## 4. 哪些内容单独定义

| 类型 | Android | iOS |
| --- | --- | --- |
| 应用标识 | package name | bundle ID |
| 设备标识 | emulator/physical device ID | simulator/device UDID |
| 选择器 | resource-id 或 accessibility id | accessibility identifier |
| 权限/系统 UI | Android 权限文案及系统组件 | iOS 权限文案、Keychain 等 |
| 返回和系统页面 | Android back/system activity | iOS navigation/system sheet |
| 清理成本 | 清除应用数据 | 可能重新安装应用，Keychain 另行处理 |

平台差异较小时，在共享 Flow 中用变量解决；差异步骤超过少量命令时，使用 `runFlow.when.platform` 调用平台子 Flow。Maestro 官方支持按 `Android`、`iOS`、`Web` 条件执行，并建议避免过度条件化。[平台条件](https://docs.maestro.dev/maestro-flows/flow-control-and-logic/conditions)

## 5. 准备 Android

1. 安装可测试 APK，并确认 package name。
2. 启动模拟器或连接设备，确认 Maestro 可识别其 ID。
3. 复制环境模板：

```bash
cp env/android.env.example env/android.env
```

4. 修改 `APP_ID`、`MAESTRO_DEVICE`，并配置测试环境敏感密码。
5. 在 Flow 中通过 `runScript` 声明认证 data 与 Android 选择器 data；不要把业务数据复制到 `env/android.env`。
6. 执行预检：

```bash
./scripts/maestro/preflight.sh android env/android.env
```

## 6. 准备 iOS

1. 将应用安装到可用模拟器/设备，并确认 bundle ID。
2. 获取模拟器或设备 UDID。
3. 复制环境模板：

```bash
cp env/ios.env.example env/ios.env
```

4. 修改 `APP_ID`、`MAESTRO_DEVICE`，并配置测试环境敏感密码。
5. 在 Flow 中通过 `runScript` 声明认证 data 与 iOS 选择器 data；不要把业务数据复制到 `env/ios.env`。
6. 执行预检：

```bash
./scripts/maestro/preflight.sh ios env/ios.env
```

`clearState` 在 iOS 上会重新安装应用，行为与 Android 清除应用数据不同；需要保留或清理 Keychain 的场景应独立设计。[clearState 说明](https://docs.maestro.dev/reference/commands-available/clearstate)

## 7. Flow 结构示例

```yaml
appId: ${APP_ID}
name: TC-AUTH-LOGIN-001 正常登录
tags: [auth, smoke, regression, positive, p0]
---
- runScript: ../../../data/auth/users.js
- runFlow:
    when:
      platform: Android
    commands:
      - runScript: ../../../data/contracts/selectors/android.js
- runFlow:
    when:
      platform: iOS
    commands:
      - runScript: ../../../data/contracts/selectors/ios.js
- runFlow: ../../../modules/app/launch.yaml
- runFlow:
    file: ../../../modules/auth/login.yaml
    env:
      USERNAME: ${output.auth.users.normal.username}
      PASSWORD: ${output.auth.users.normal.password}
- assertVisible:
    text: "${output.selectors.login.homeText}"
```

Maestro Flow 由 `---` 分隔的配置区和命令区组成；`appId` 位于每个 Flow 顶部，变量使用 `${VARIABLE}`。[Flow 概览](https://docs.maestro.dev/maestro-flows) [参数与常量](https://docs.maestro.dev/maestro-flows/flow-control-and-logic/parameters-and-constants)

## 8. data 和选择器

`data/auth/users.js` 保存测试环境专用的脱敏账号；`data/operations/users-batch.js` 保存批量记录和查询条件。Flow 执行对应的 `runScript` 后，通过 `output` 层级引用数据，例如 `${output.auth.users.normal.username}` 与 `${output.data.users.insertUsers.records}`。`data/contracts/selectors/{platform}.js` 也是运行时数据，Flow 通过 `${output.selectors.login.usernameId}` 引用平台选择器。

数据文件由入口 Flow 显式选择和加载，不需要通过 CLI 再传一份数据文件参数：

```yaml
# 数据路径由 Flow 的 runScript 控制，不需要额外的文件列表参数。
- runScript: ../../../data/auth/users.js
```

应用标识、设备和敏感值放在未提交的环境文件中；业务数据与选择器仍放在 `data/`。优先使用稳定 accessibility id/resource-id；只有稳定 ID 不可用时才使用可见文本。不要使用坐标和长层级路径。

当页面多、选择器数量增长时，可升级为 Maestro 官方示例中的 Page Object Model：平台 JavaScript 文件输出选择器，Flow 通过 `${output...}` 引用。[Page Object Model](https://docs.maestro.dev/examples/page-object-model)

## 9. Module 与平台分支

公共 Module 通过 `runFlow` 接收数据：

```yaml
- runFlow:
    file: ../../../modules/auth/login.yaml
    env:
      USERNAME: ${output.auth.users.normal.username}
      PASSWORD: ${output.auth.users.normal.password}
```

平台差异通过条件子 Flow：

```yaml
- runFlow:
    when:
      platform: Android
    file: prepare-android.yaml
- runFlow:
    when:
      platform: iOS
    file: prepare-ios.yaml
```

`runFlow` 支持文件子 Flow 和 `env` 参数，适合复用登录、初始化等步骤；数据应在入口 Flow 中先通过 `runScript` 加载。[runFlow 参考](https://docs.maestro.dev/api-reference/commands/runflow)

## 10. Journey

Journey 是带 `e2e` Tag 的顶层 Maestro Flow。它应自行创建起始状态并组合 Module，不依赖其他测试先运行。Maestro 默认不保证 Flow 顺序，官方也建议每个 Flow 可在重置设备上独立运行。[顺序执行](https://docs.maestro.dev/maestro-flows/workspace-management/sequential-execution)

执行 Journey：

```bash
./scripts/maestro/run-suite.sh android e2e env/android.env
./scripts/maestro/run-suite.sh ios e2e env/ios.env
```

## 11. 执行命令

单 Flow：

```bash
./scripts/maestro/run-flow.sh android flows/auth/login/TC-AUTH-LOGIN-001.yaml env/android.env JUNIT
./scripts/maestro/run-flow.sh ios flows/auth/login/TC-AUTH-LOGIN-001.yaml env/ios.env HTML
```

按 Tag 执行：

```bash
./scripts/maestro/run-suite.sh android smoke env/android.env
./scripts/maestro/run-suite.sh ios regression env/ios.env
```

通用入口：

```bash
MAESTRO_PLATFORM=android MAESTRO_ENV_FILE=env/android.env ./scripts/run-smoke.sh
MAESTRO_PLATFORM=ios MAESTRO_ENV_FILE=env/ios.env ./scripts/run-regression.sh
```

## 12. 构建顺序

Maestro YAML 不需要传统编译。本工程把“构建”定义为验证资产、平台配置、设备和报告链路能够组成可执行工作区。

```text
1. validate-cases.sh：Case/Flow 映射
2. bash -n：执行脚本语法
3. 加载平台环境并检查必需变量
4. 检查 Maestro CLI 与 Flow 结构
5. Smoke：快速判断核心能力
6. Regression：验证完整功能回归
7. e2e Journey：验证跨功能目标
8. 检查 JUnit/HTML/debug Artifact
```

执行完整顺序：

```bash
./scripts/maestro/build-and-test.sh android env/android.env
./scripts/maestro/build-and-test.sh ios env/ios.env
```

双平台应作为两个独立任务执行，使设备资源、失败状态和报告互不覆盖。

也可从一个调度入口依次执行两端：

```bash
./scripts/maestro/build-all-platforms.sh env/android.env env/ios.env
```

该脚本会在一个平台失败后继续执行另一平台，最终以失败状态退出；两个平台的报告仍按平台目录隔离。

## 13. 报告与 Artifact

脚本使用 Maestro CLI 的 `--format`、`--output`、`--debug-output` 和 `--test-output-dir` 参数，将结果写入：

```text
artifacts/maestro/{platform}/{run-id}/{scope}/
├── report.xml 或 report.html
├── debug/
└── tests/
```

CLI 官方支持 JUnit、HTML、设备和 Tag 过滤参数。[CLI 参数](https://docs.maestro.dev/maestro-cli/maestro-cli-commands-and-options)

CI 应上传报告和 debug 目录，但不能把 Artifact 提交到 Git。日志输出前必须脱敏。

## 14. 构建实践

- **从 Case 开始**：先评审业务覆盖，再实现 Maestro Flow。
- **小步验证**：先运行单 Flow，再运行 Smoke，最后运行 Regression/Journey。
- **稳定选择器**：Android/iOS 使用含义一致、平台值独立的可访问性标识。
- **状态隔离**：普通 Flow 用干净状态启动；登录保持场景明确验证不清理状态的重新启动。
- **有限可选步骤**：`optional: true` 只用于已知可选权限弹窗，不用于业务断言。
- **避免顺序依赖**：需要前置状态时通过 Module/Hook/嵌套 Flow 建立，而不是依赖上一用例。
- **失败可诊断**：报告必须包含 Case ID，保留 debug 输出和必要截图。
- **平台分别验证**：共享 Flow 修改后必须至少在 Android 和 iOS 各运行一次相关范围。

## 15. CI 建议

1. Android 与 iOS 使用独立 Job 和设备池。
2. PR 先运行资产校验和 Smoke；主分支或定时任务运行 Regression/E2E。
3. 通过 CI 密钥管理注入账号，不落地到仓库。
4. 失败时上传 JUnit/HTML、debug 和测试输出目录。
5. 使用 Case ID 作为报告和缺陷追踪的关联键。

## 16. 故障排查

| 问题 | 检查顺序 |
| --- | --- |
| `Maestro CLI not found` | 安装 CLI，或用 `MAESTRO_BIN` 指定可执行文件 |
| 环境变量为空 | 检查平台 `.env` 是否从模板复制并填写 |
| 找不到控件 | 检查平台选择器、可访问性标识、页面状态和键盘遮挡 |
| Android 通过、iOS 失败 | 对照两个 selector 文件和平台准备 Flow |
| Flow 未被发现 | 检查 `.maestro/config.yaml` 的递归 glob 和 Tag |
| 登录保持失败 | 确认第二次 `launchApp` 没有 `clearState: true` |
| 报告缺失 | 检查 Maestro 返回状态和 Artifact 目录权限 |

## 17. 接入真实应用检查清单

- 在两个实际环境文件中填写 `APP_ID`、设备 ID 和敏感值，并在两个 selector JS 中配置真实控件标识；
- 在 Android/iOS 应用中提供含义一致的 accessibility 标识；
- 确认权限弹窗文案，按地区和系统版本调整平台子 Flow；
- 为测试环境创建最小权限账号并安全配置；
- 单独运行五个登录 Flow 和 Journey；
- 在两端验证 Smoke、Regression、JUnit/HTML 与 debug 输出；
- 将双平台任务接入 CI，并设置 Artifact 保留期限。

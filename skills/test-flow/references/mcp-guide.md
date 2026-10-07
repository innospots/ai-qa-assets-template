# Maestro MCP 使用指南（test:flow）

> 官方文档：[Maestro MCP Server](https://docs.maestro.dev/get-started/maestro-mcp)  
> MCP 随 Maestro CLI 内置；本仓库 Cursor 配置见 `~/.cursor/mcp.json`。

## 1. 定位：MCP 与 test:flow 的分工

| 能力 | test:flow Skill | Maestro MCP |
| --- | --- | --- |
| 从 Case 生成正式 Flow | **是** | 否（辅助探索） |
| 写入 `flows/`、`modules/` | **是** | 否（`run` 为临时验证） |
| 查看当前屏幕层级 | 规范层引用 | **`inspect_screen`** |
| 试跑 YAML 片段 | 校验脚本 | **`run` `{ yaml }`** |
| 查设备 | — | **`list_devices`** |
| 查命令语法 | references | **`cheat_sheet`** |
| 正式 CI / 套件执行 | `test:execution` + `scripts/` | 可选 Cloud |

**原则：** MCP 用于**探索、试跑、调试**；落盘的 Flow 仍须符合 Case、`references/` 与审查清单。

## 2. 何时使用 MCP（推荐时机）

### 应在 test:flow 过程中使用

| 阶段 | MCP 工具 | 目的 |
| --- | --- | --- |
| T0/T1：Case 已有，Selector 未知 | `list_devices` → `inspect_screen` | 确认控件 text/id，避免臆造 Selector |
| T2：编写 Flow 前 | `cheat_sheet` | 确认 Command 语法与参数 |
| T2：Draft 验证 | `run` + `{ yaml: "..." }` | 小步试跑，**不写**正式资产 |
| 调试失败 Selector/时序 | `inspect_screen`、`take_screenshot` | 对比 Case 预期与真实 UI |
| 需要可视化操作设备 | `open_maestro_viewer` | 在 Agent 内嵌模拟器/真机 |

### 不应依赖 MCP 替代

- 跳过 Case 直接 `run` 当测试定义
- 用 MCP 试跑通过后就地改 Case 预期
- 用 `run` 批量覆盖 `flows/` 而不走审查
- 把 MCP 探索用的 `point` 坐标直接进正式 Flow（应换稳定 id/text）

## 3. Cursor 配置

项目与用户级均已配置（示例）：

```json
{
  "mcpServers": {
    "maestro": {
      "command": "/Users/mac/.maestro/bin/maestro",
      "args": ["mcp"],
      "env": {
        "JAVA_HOME": "/opt/homebrew/opt/openjdk@25/libexec/openjdk.jdk/Contents/Home"
      }
    }
  }
}
```

启用：**Cursor Settings → Tools & MCPs → maestro**（或重启 Cursor）。

CLI 与 MCP 同版本升级：`maestro` 更新后重连 MCP。

## 4. MCP 工具速查

| 工具 | 用途 |
| --- | --- |
| `list_devices` | 列出本机 Android 模拟器、iOS 模拟器、Chromium |
| `inspect_screen` | 当前屏幕可交互层级（写 Selector 前调用；UI 变化后重调） |
| `take_screenshot` | 截图辅助判断 |
| `run` | 执行 Flow：`yaml`（探索优先）/ `files` / `dir`+tags |
| `cheat_sheet` | Maestro 命令与 Flow 语法摘要 |
| `open_maestro_viewer` | 打开 Maestro Viewer URL |
| `list_cloud_devices` / `run_on_cloud` / `get_cloud_run_status` | Maestro Cloud（需 `maestro login` 或 API Key） |

## 5. 与 test:flow 工作流结合

```text
读 Case + data 规范
    ↓
list_devices（确认有设备）
    ↓
inspect_screen（目标页）
    ↓
cheat_sheet（不熟命令时）
    ↓
run { yaml: 草稿片段 }（小步验证）
    ↓
按 references 写入 flows/.../TC-*.yaml
    ↓
validate-flow.py + check-references.py + validate-cases.sh
    ↓
test:execution 正式跑 flows/（非 MCP 临时 yaml）
```

### 探索性 `run` 示例（不落盘）

向 Agent 说明意图即可，例如：

> 在已连接 Android 设备上试跑：launchApp 后 assertVisible 首页文案

Agent 通过 MCP `run` 传入 inline yaml；**通过后**再将等价步骤写入正式 Flow，并绑定 `${output...}`。

### 正式 Flow 执行

仓库内正式执行走 `test:execution`：

```bash
scripts/maestro/run-flow.sh android flows/mobile/demo/TC-MOBILE-DEMO-001.yaml env/android.env
```

不用 MCP `run` 替代 CI/门禁。

## 6. 数据与 MCP

- MCP 试跑仍应使用 `${output...}` / env，与 [data-binding-guide.md](data-binding-guide.md) 一致
- 探索阶段可临时写死 text 验证定位；**提交前**必须改回 data 引用
- `runScript` 加载 `data/**/*.js` 在正式 Flow 中保留；MCP inline yaml 可省略 data 仅验证 Selector（需标注为 draft）

## 7. 常见问题

| 现象 | 处理 |
| --- | --- |
| MCP 未连接 | 检查 `maestro` 路径、`JAVA_HOME`；重启 Cursor |
| `list_devices` 为空 | 启动模拟器/连接真机 |
| inline yaml 通过但正式 Flow 失败 | 检查 data 路径、Module 引用、平台 selector |
| Cloud 工具不可用 | `maestro login` 或设置 `MAESTRO_CLOUD_API_KEY` |

## 8. 官方链接

- [Maestro MCP](https://docs.maestro.dev/get-started/maestro-mcp)
- [Maestro Flows](https://docs.maestro.dev/maestro-flows)
- [Commands](https://docs.maestro.dev/reference/commands-available)

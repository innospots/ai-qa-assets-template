# 引导式创建（AskQuestion）

当用户**没有完整 PRD/PDD**、只给出功能描述、或明确要求「引导我创建测试设计」时，在 T0 之前用 **AskQuestion** 分轮收集信息，再进入 [`workflow.md`](workflow.md) 的 T0→T1→… 流程。

有完整 PRD/PDD 且用户未要求引导时，**跳过**本文件，直接做 T0 输入盘点。

## 使用规则

1. **必须用 AskQuestion 工具**提问；不要把选项堆在正文里让用户打字选。
2. **每轮 1–3 个问题**，答完再发下一轮；单轮不超过 3 题。
3. 每题 **2–5 个选项** + 系统自带的 **Other**（用户可填路径、场景名、补充说明）。
4. 用户选 Other 或补充文本时，记入 **intake 摘要**，冲突项写入待确认问题。
5. 引导结束产出 **T0 草案**（domain、场景列表、sources、待确认问题），**经用户确认**后再拆 T1… 任务。
6. 引导阶段**不写** `designs/` 文件；只收集与整理。

## 何时启动

| 情况 | 动作 |
| --- | --- |
| 用户提供 PRD/PDD 路径且信息足够 | 跳过引导，T0 从文档提取 |
| 用户只有口头/简短功能描述 | 从 Phase 1 开始 |
| 用户说「新建测试设计」「帮我设计 XX 模块」 | 从 Phase 1 开始 |
| 用户要扩展已有 `designs/{domain}/` | Phase 1 选「扩展现有模块」，Phase 2 带已有 domain |
| 用户只要存量对齐 | 不用本引导，走 workflow §6 |

---

## Phase 1 — 任务类型与输入方式

**目标：** 确定新建 / 扩展 / 对齐，以及是否有文档。

**AskQuestion（整批一次调用）：**

| id | prompt | options | allow_multiple |
| --- | --- | --- | --- |
| `task_type` | 这次测试设计任务属于哪种？ | `new_module` 新建模块（尚无 `designs/` 目录） · `extend_module` 扩展现有模块（已有 Index，增场景或改范围） · `single_scene` 只新建/重写单个场景 TDS · `align_existing` 仅规范对齐存量 TDS | 否 |
| `input_mode` | 你目前有哪些输入材料？ | `has_prd` 有 PRD/需求文档 · `has_pdd` 有产品功能文档/PDD · `has_both` PRD 和 PDD 都有 · `has_partial` 有部分文档或笔记 · `none` 暂无文档，靠对话补充 | 否 |
| `doc_delivery` | 文档如何提供？（无文档可选 Other 说明） | `repo_path` 仓库内路径（Phase 2 后请填 Other） · `paste_next` 下一轮消息粘贴正文 · `skip_docs` 暂不提供，先引导梳理 · `already_given` 本轮已给出/已读过 | 否 |

**分支：**

- `align_existing` → 结束引导，转 workflow §6；仅问缺口时可补 1 轮 Phase 6。
- `has_both` 或 `has_prd` + 路径明确 → 可缩短 Phase 3–5，Phase 2 后快速进入 Phase 6 确认。
- `none` / `has_partial` → 完整走 Phase 2–6。

---

## Phase 2 — 模块定位

**目标：** 确定 `{domain}`、模块名称、平台与优先级。

**AskQuestion：**

| id | prompt | options | allow_multiple |
| --- | --- | --- | --- |
| `domain` | 模块英文标识（用于 `designs/{domain}/`）？ | 根据上下文生成 3–4 个合理 slug（如 `customer`、`catalog`、`billing`）；无匹配时用户选 Other 填写 | 否 |
| `module_scope` | 模块一句话范围是？ | 由 Agent 根据已读 PRD 或用户描述生成 3–4 条摘要选项 + Other 自定义 | 否 |
| `platform` | 需要覆盖哪些平台？ | `android` · `ios` · `web` · `api` · `all_mobile` Android+iOS | 是 |
| `priority` | 测试优先级？ | `p0` 核心回归 · `p1` 重要功能 · `p2` 一般 · `unknown` 待确认 | 否 |

**写入 T0：** `domain`、`name`（中文模块名）、`platform[]`、`priority`、Front Matter 初稿字段。

---

## Phase 3 — 场景拆分

**目标：** 列出 `{scene}.design.md` 清单（按**业务动作**，不按页面控件）。

**AskQuestion：**

| id | prompt | options | allow_multiple |
| --- | --- | --- | --- |
| `scene_strategy` | 场景如何拆分？ | `agent_proposed` 采用 Agent 根据需求提议的列表 · `user_list` 我在 Other 里列场景名 · `one_scene_first` 先只做 1 个核心场景，其余后续补 · `match_prd_sections` 按 PRD 章节一一对应 | 否 |
| `scenes` | 请确认要写的场景 TDS（文件名 `{scene}.design.md`） | Agent 提议 4–8 个 kebab-case 场景 id + 短标签；用户多选；Other 增删 | 是 |

**规则：**

- 单场景任务（`single_scene`）只保留 1 个选中项。
- 公共规则（登录、权限、租户）**不**单独成场景，写入 Index。
- 与用户描述明显无关的选项不要出现。

**写入 T0：** `scenes: [{ id, title }]`。

---

## Phase 4 — 公共上下文（Index 级）

**目标：** 收集 Index §3–§6 所需公共信息。

**AskQuestion：**

| id | prompt | options | allow_multiple |
| --- | --- | --- | --- |
| `preconditions` | 使用本模块前通常需要哪些前置？ | `login` 已登录 · `role` 特定角色 · `tenant` 租户/组织上下文 · `data_seed` 依赖预置数据 · `none` 无特殊前置 · Other | 是 |
| `shared_rules` | 有哪些**跨场景**业务规则必须在 Index 写一次？ | Agent 从 PRD/对话提炼 3–5 条（权限、唯一性、状态机、审计…）+ Other | 是 |
| `out_of_scope` | 明确**不在**本模块测试设计范围内？ | Agent 提议常见排除项 + Other | 是 |
| `platform_diff` | 是否存在显著平台差异？ | `no` 无 · `ui_only` 仅 UI 差异 · `capability` 能力开关不同 · `major` 流程不同需分场景说明 · `unknown` 待确认 | 否 |

**写入 T0：** Index 章节要点、待确认问题（`unknown` 项）。

---

## Phase 5 — 覆盖与风险（模块级）

**目标：** 对齐数据驱动与风险分层，供 Index §7 与各场景 §7 引用。

**AskQuestion：**

| id | prompt | options | allow_multiple |
| --- | --- | --- | --- |
| `risk_focus` | 本模块最需重点关注的风险？ | `data_integrity` 数据正确性 · `security` 权限/越权 · `state` 状态流转 · `concurrency` 并发/重复提交 · `ux_block` 关键路径不可用 · Other | 是 |
| `negative_depth` | 反向/异常覆盖深度？ | `standard` 标准（每核心功能约 3–5 条 DS-101+） · `light` 仅关键反向 · `deep` 含较多边界与异常 · `defer` 部分标暂缓，写待确认 | 否 |
| `boundary_known` | 是否已有明确边界值（长度、数量、超时等）？ | `yes_in_docs` 文档已写清 · `partial` 部分已知 · `none` 暂无，TDS 标待确认 · `agent_propose` 由 Agent 按常识提议并标待确认 | 否 |
| `defer_items` | 哪些类型用例暂不设计、标专项/暂缓？ | `fault_injection` 故障注入 · `performance` 性能压测 · `compatibility` 兼容矩阵 · `security_scan` 安全扫描 · `none` 无 · Other | 是 |

**写入 T0：** 风险标签、覆盖策略、暂缓清单。

---

## Phase 6 — 确认与缺口

**目标：** 展示 T0 摘要，确认后开始生成。

**先输出文字摘要**（非 AskQuestion）：

- domain / 模块名 / 平台 / 优先级
- 场景列表
- sources（PRD/PDD 路径或「对话引导 intake-{date}」）
- 待确认问题列表

**AskQuestion（最后一轮）：**

| id | prompt | options | allow_multiple |
| --- | --- | --- | --- |
| `t0_confirm` | T0 规划是否准确？ | `approve` 确认，开始按 workflow 生成 Index · `edit_scenes` 调整场景列表（Other 说明） · `edit_scope` 调整模块范围 · `pause` 先暂停，补充材料后再继续 | 否 |
| `start_task` | 确认后首先生成？ | `index_first` 先生成模块 Index（推荐） · `one_scene` 跳过 Index，只写单个场景（需说明原因，Other） · `review_plan_only` 只输出任务清单，暂不写文件 | 否 |

**分支：**

- `edit_*` → 更新 T0，必要时回到 Phase 2 或 3 **只问变更相关的一轮**。
- `approve` + `index_first` → 创建 todo：T1…Tn + T_review…，进入 workflow §2。

---

## intake 摘要模板

引导结束后，Agent 内部维护如下结构，并作为 T0 产出的一部分：

```yaml
intake:
  task_type: new_module | extend_module | single_scene
  input_mode: has_prd | has_pdd | has_both | has_partial | none
  domain: "{domain}"
  module_name: "{中文名}"
  platform: [android, ios]
  priority: P0
  scenes:
    - id: create-customer
      title: 创建客户
  sources:
    - type: prd
      ref: "{path or 对话引导}"
  shared_rules: []
  out_of_scope: []
  risk_focus: []
  coverage: standard
  defer: [fault_injection]
  open_questions: []
```

写入 TDS 时：`sources` 进 Front Matter；`open_questions` 进 Index/场景「待确认问题」。

---

## 示例：首轮 AskQuestion 载荷

Agent 调用 AskQuestion 时参考（选项需按实际上下文替换）：

```json
{
  "title": "测试设计 · 任务与输入",
  "questions": [
    {
      "id": "task_type",
      "prompt": "这次测试设计任务属于哪种？",
      "options": [
        { "id": "new_module", "label": "新建模块（尚无 designs/ 目录）" },
        { "id": "extend_module", "label": "扩展现有模块（已有 Index，增场景或改范围）" },
        { "id": "single_scene", "label": "只新建/重写单个场景 TDS" },
        { "id": "align_existing", "label": "仅规范对齐存量 TDS" }
      ]
    },
    {
      "id": "input_mode",
      "prompt": "你目前有哪些输入材料？",
      "options": [
        { "id": "has_prd", "label": "有 PRD / 需求文档" },
        { "id": "has_pdd", "label": "有产品功能文档 / PDD" },
        { "id": "has_both", "label": "PRD 和 PDD 都有" },
        { "id": "has_partial", "label": "有部分文档或笔记" },
        { "id": "none", "label": "暂无文档，靠对话补充" }
      ]
    },
    {
      "id": "doc_delivery",
      "prompt": "文档如何提供？",
      "options": [
        { "id": "repo_path", "label": "仓库内路径（下一轮在 Other 填写）" },
        { "id": "paste_next", "label": "下一轮消息粘贴正文" },
        { "id": "skip_docs", "label": "暂不提供，先引导梳理" },
        { "id": "already_given", "label": "本轮已给出 / Agent 已读过" }
      ]
    }
  ]
}
```

---

## 与 workflow 的衔接

```text
用户请求
  ↓
有完整 PRD/PDD 且无需引导？ —是→ workflow §1.2 文档盘点
  ↓ 否
guided-intake Phase 1…6（AskQuestion 分轮）
  ↓
T0 摘要 + 用户 confirm（Phase 6）
  ↓
using-superpowers 拆任务 → T1 Index → T2… 场景 → checklist 审查
```

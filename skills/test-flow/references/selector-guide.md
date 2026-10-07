# Selector Guide

## 1. 目的

建立统一的 Selector 选择顺序，降低由于页面调整、设备尺寸、国际化和动态数据造成的 Flow 脆弱性。

## 2. 官方依据

- How to use Selectors  
  https://docs.maestro.dev/maestro-flows/flow-control-and-logic/how-to-use-selectors
- Core Selectors  
  https://docs.maestro.dev/reference/selectors/core-selectors
- Relational Selectors  
  https://docs.maestro.dev/reference/selectors/relational-selectors
- State Selectors  
  https://docs.maestro.dev/reference/selectors/state-selectors
- Dimension Matchers  
  https://docs.maestro.dev/reference/selectors/dimension-matchers
- Element Traits  
  https://docs.maestro.dev/reference/selectors/element-traits

## 3. Selector 基础

Maestro 主要通过 Accessibility Tree 识别 UI。

常见 Selector：

```text
text
id
index
point
css (Web)
above / below / leftOf / rightOf
containsChild / childOf / containsDescendants
enabled / checked / focused / selected
width / height / tolerance
```

多个属性组合时按 AND 逻辑匹配。

## 4. 统一优先级

### 4.1 通用移动端

```text
用户可见且稳定的 text
        ↓
稳定的 accessibility/resource id
        ↓
text/id + state
        ↓
稳定 anchor + relational selector
        ↓
结构关系 selector
        ↓
index
        ↓
dimension / trait
        ↓
coordinate / point
```

### 4.2 国际化场景

多语言情况下可见文字会变化：

```text
稳定 accessibility id
    ↓
结构 / relational
    ↓
当前 locale 的 text
```

### 4.3 Web

```text
稳定 text / accessibility
    ↓
稳定 CSS selector
    ↓
关系组合
```

CSS 不支持 text/id 那样的 regex 行为。

## 5. `text`

适合：

- 按钮名称；
- 页面标题；
- 提示语；
- Expected Result；
- 用户真实可见业务内容。

```yaml
- assertVisible: "Payment successful"
```

`text` 默认支持正则，因此动态文字可以使用有边界的模式：

```yaml
- assertVisible:
    text: "Order #.* created"
```

不要使用过宽正则：

```yaml
text: ".*"
```

## 6. `id`

适合：

- 图标；
- 无文字控件；
- 动态文字区域；
- 多语言界面；
- 关键可交互组件。

```yaml
- tapOn:
    id: login_button
```

优先使用稳定、语义化、不会因布局变化而修改的 accessibility identifier。

## 7. State Selector

用于表达“目标不仅存在，而且处于正确状态”。

```yaml
- assertVisible:
    id: submit_button
    enabled: false
```

常见：

- `enabled`
- `checked`
- `focused`
- `selected`

推荐用于：

- 表单按钮可用性；
- Checkbox / Switch；
- Tab 选中状态；
- 输入焦点。

## 8. Relational Selector

当页面存在多个相同按钮或目标缺少唯一 ID 时使用。

```yaml
- tapOn:
    text: "Delete"
    childOf:
      id: order_123
```

或者：

```yaml
- tapOn:
    id: edit_icon
    rightOf: "Customer name"
```

规则：

- Anchor 必须比目标本身更稳定；
- Relational 不应建立在另一个脆弱 Selector 上；
- 多个候选存在时，应再增加 text/id/state 约束。

## 9. `index`

仅用于：

- 多个完全相同元素无法通过业务语义区分；
- 顺序本身就是测试意图；
- 页面顺序已明确稳定。

```yaml
- tapOn:
    text: "Add"
    index: 1
```

禁止把 `index` 当作默认消歧方式。

## 10. Dimension / Trait

尺寸匹配受设备和缩放影响，仅用于特殊 UI。

如确需使用尺寸：

```yaml
- assertVisible:
    id: settings_icon
    width: 48
    height: 48
    tolerance: 2
```

必须与其他 Selector 组合。

## 11. Coordinate / Point

属于最后手段。

可以使用的情况：

- 元素不在 Accessibility Tree；
- Canvas / 地图 / 自绘区域；
- 测试目标本身就是屏幕位置。

禁止：

- 普通按钮、输入框存在 text/id 时仍使用坐标；
- 使用绝对像素适配多设备；
- Agent 未检查 UI 结构就自动生成坐标。

## 12. Selector 生成决策

```text
是否有稳定可见业务文本？
 ├─ 是 → text
 └─ 否
    ↓
是否有稳定 accessibility id？
 ├─ 是 → id
 └─ 否
    ↓
是否有稳定 Anchor？
 ├─ 是 → relational
 └─ 否
    ↓
是否可以使用结构关系定位？
 ├─ 是 → child/descendant
 └─ 否
    ↓
index / dimension / point
```

## 13. Review Checklist

- [ ] Selector 与用户/业务语义一致
- [ ] text 正则不过宽
- [ ] id 稳定
- [ ] 多元素匹配已经消歧
- [ ] state 被正确表达
- [ ] relational anchor 稳定
- [ ] index 有明确理由
- [ ] point 是最后手段

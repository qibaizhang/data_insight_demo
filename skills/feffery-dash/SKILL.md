---
name: feffery-dash
description: Feffery-Dash 全栈开发辅助 Skill。用于开发基于 Plotly Dash + Feffery 组件库的 Web 应用。包含 fac(UI组件)、fuc(工具组件)、fact(图表)、flc/fm(地图)、fmc(Markdown)、famc(移动端)、magic-dash(脚手架) 的使用指南和最佳实践。当用户提到 Dash 开发、feffery 组件、fac/fuc/fact/fmc/famc 组件、回调函数、magic-dash 项目模板、仪表盘开发、移动端应用时使用此 Skill。
---

# Feffery-Dash AI 开发辅助 Skill

> 为 Claude Code 提供 Feffery-Dash 生态系统的完整开发支持

---

## 核心模块导航

### 1. 开发规范 (references/core/)

| 文档 | 内容 |
|------|------|
| [feffery-dash-core.md](references/core/feffery-dash-core.md) | **核心入口** - 标准导入、应用实例化、回调规范 |
| [project_standards.md](references/core/project_standards.md) | 项目结构规范、文件组织 |
| [callback_patterns.md](references/core/callback_patterns.md) | 回调模式大全：ctx、Patch、set_props、模式匹配 |
| [layout_guide.md](references/core/layout_guide.md) | 布局指南：栅格、Flex、响应式 |
| [best_practices.md](references/core/best_practices.md) | 最佳实践：性能、安全、代码组织 |
| [plugins.md](references/core/plugins.md) | Dash 3.x 插件系统 |

### 2. 组件库 (references/components/)

| 组件库 | 文档 | 用途 |
|--------|------|------|
| **fac** | [feffery-fac.md](references/components/fac/feffery-fac.md) | Ant Design UI 组件 (100+) |
| **fuc** | [feffery-fuc.md](references/components/fuc/feffery-fuc.md) | 工具组件、性能优化 |
| **fact** | [feffery-fact.md](references/components/fact/feffery-fact.md) | 数据可视化图表 |
| **flc** | [feffery-flc.md](references/components/flc/feffery-flc.md) | Leaflet 地图组件 |
| **fm** | [feffery-fm.md](references/components/fm/feffery-fm.md) | MapLibre/Deck.gl 高性能地图 |
| **fi** | [feffery-fi.md](references/components/fi/feffery-fi.md) | 声明式信息图 (59 模板) |

### 3. 专题指南 (references/topics/)

| 专题 | 文档 | 说明 |
|------|------|------|
| **magic-dash** | [magic-dash.md](references/topics/magic-dash/magic-dash.md) | 项目脚手架 CLI 工具 |
| **仪表盘** | [dashboard.md](references/topics/dashboard/dashboard.md) | 仪表盘开发完整指南 |

### 4. 扩展组件 (references/extras/)

| 组件/插件 | 文档 | 说明 |
|-----------|------|------|
| **fmc** | [fmc_markdown.md](references/extras/fmc_markdown.md) | Markdown 渲染、代码高亮、LaTeX |
| **famc** | [mobile_components.md](references/extras/mobile_components.md) | 移动端 UI 组件 (57个) |
| **插件** | [plugins.md](references/extras/plugins.md) | Tailwind CSS / Vite 插件 |
| **汇总** | [feffery-extras.md](references/extras/feffery-extras.md) | 扩展组件入口文档 |

### 5. 案例库 (references/examples/)

| 文档 | 说明 |
|------|------|
| [feffery-examples.md](references/examples/feffery-examples.md) | 案例索引入口 |
| [by_category.md](references/examples/by_category.md) | 按类别浏览 |
| [by_component.md](references/examples/by_component.md) | 按组件浏览 |

---

## 快速参考

### 标准导入模板

```python
# Dash 核心
import dash
from dash import html, dcc, ctx, Patch, set_props, no_update
from dash.dependencies import Input, Output, State, ALL, MATCH

# Feffery 组件库（必须使用指定别名）
import feffery_antd_components as fac
import feffery_utils_components as fuc
```

### 应用基础结构

```python
app = dash.Dash(
    __name__,
    title='应用标题',
    suppress_callback_exceptions=True,
)
server = app.server

app.layout = fac.AntdConfigProvider(
    locale='zh-cn',
    children=[
        # 页面内容
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
```

### 常用组件速查

| 类别 | 组件 |
|------|------|
| 布局 | `AntdRow/Col`, `AntdSpace`, `AntdLayout`, `AntdCard` |
| 表单 | `AntdForm`, `AntdInput`, `AntdSelect`, `AntdDatePicker` |
| 展示 | `AntdTable`, `AntdTabs`, `AntdModal`, `AntdDrawer` |
| 反馈 | `AntdMessage`, `AntdNotification`, `AntdSpin`, `AntdAlert` |
| 图表 | `AntdLine`, `AntdBar`, `AntdPie`, `AntdArea` |

### 组件库一览

| 组件库 | 别名 | 组件数 | 官方文档 |
|--------|------|--------|----------|
| feffery-antd-components | fac | 109 | https://fac.feffery.tech/ |
| feffery-utils-components | fuc | 123 | https://fuc.feffery.tech/ |
| feffery-antd-charts | fact | 32 | https://fact.feffery.tech/ |
| feffery-leaflet-components | flc | 29 | http://flc.feffery.tech/ |
| feffery-maplibre | fm | 32 | - |
| feffery-markdown-components | fmc | - | http://fmc.feffery.tech/ |
| feffery-antd-mobile-components | famc | 57 | - |
| feffery-infographic | fi | 1 (59 模板) | https://infographic.antv.vision/ |

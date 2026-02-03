# feffery-extras

> feffery 系列扩展组件与插件 Skill
> 包含：fmc (Markdown)、famc (移动端)、Tailwind CSS 插件、Vite 插件

---

## 扩展组件/插件索引

| 名称 | 简称 | 功能 | 详细文档 |
|------|------|------|----------|
| **feffery-markdown-components** | fmc | Markdown 渲染、代码高亮、LaTeX、Mermaid | [fmc_markdown.md](./fmc_markdown.md) |
| **feffery-antd-mobile-components** | famc | 移动端 UI 组件库（57个组件） | [mobile_components.md](./mobile_components.md) |
| **dash-tailwindcss-plugin** | - | Tailwind CSS 集成 | [plugins.md](./plugins.md) |
| **dash-vite-plugin** | - | Vite 构建工具（Vue.js/React） | [plugins.md](./plugins.md) |

---

## feffery-markdown-components (fmc)

> Markdown 渲染组件库 | 官方文档: http://fmc.feffery.tech/

### 快速开始

```python
import dash
from dash import html
import feffery_markdown_components as fmc

app = dash.Dash(__name__)

app.layout = html.Div([
    fmc.FefferyMarkdown(
        markdownStr="""
# 标题

这是一段 **Markdown** 文本。

- 列表项 1
- 列表项 2

```python
print("Hello, fmc!")
```
"""
    )
])
```

### 组件列表

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyMarkdown` | Markdown 渲染 | `markdownStr`, `codeTheme`, `titleAsId` |
| `FefferySyntaxHighlighter` | 代码高亮+Diff | `codeString`, `language`, `addedLineNumbers` |

### FefferyMarkdown 主要特性

- ✅ 标准 Markdown + GFM 语法
- ✅ LaTeX 数学公式 (`$...$` / `$$...$$`)
- ✅ Mermaid 图表（需引入外部脚本）
- ✅ 代码语法高亮（26 种主题）
- ✅ 图片预览
- ✅ 外部链接安全检查
- ✅ 关键词高亮搜索
- ✅ 自动生成目录锚点 (`facAnchorLinkDict`)

### 代码主题（26种）

常用主题：`gh-colors`（默认）、`dracula`、`nord`、`atom-dark`、`night-owl`、`one-light`、`material-dark`、`gruvbox-dark`、`synthwave84`

**详细文档**：[fmc_markdown.md](./fmc_markdown.md)

---

## feffery-antd-mobile-components (famc)

> 移动端组件库 | 基于 Ant Design Mobile 5.x | 57 个组件

### 快速开始

```python
import dash
import feffery_antd_mobile_components as famc

app = dash.Dash(__name__)

app.layout = famc.Fragment([
    famc.MobileNavBar(children='我的应用', backArrow=True),
    famc.MobileButton('点击我', color='primary', block=True)
])
```

### 组件分类（57个）

| 分类 | 数量 | 代表组件 |
|------|------|----------|
| 通用 | 2 | `MobileButton`, `MobileIcon` |
| 数据展示 | 15 | `MobileCard`, `MobileList`, `MobileSwiper`, `MobileImage` |
| 数据输入 | 12 | `MobileInput`, `MobileForm`, `MobileSearchBar`, `MobileCascader` |
| 反馈 | 12 | `MobileDialog`, `MobilePopup`, `MobileToast`, `MobilePullToRefresh` |
| 布局 | 6 | `MobileGrid`, `MobileSpace`, `MobileSafeArea` |
| 导航 | 6 | `MobileNavBar`, `MobileTabBar`, `MobileTabs` |
| 其他 | 5 | `Fragment`, `MobileFloatingBubble` |

### 与桌面端 fac 的区别

| 特性 | famc (移动端) | fac (桌面端) |
|------|--------------|-------------|
| 目标平台 | 移动端 | 桌面端 |
| 交互方式 | 触摸优先 | 鼠标优先 |
| 组件数量 | 57 个 | 200+ 个 |

**详细文档**：[mobile_components.md](./mobile_components.md)

---

## dash-tailwindcss-plugin

> Tailwind CSS 集成 | 支持 v3 和 v4 | 在线/离线双模式

### 快速开始

```python
from dash import Dash, html
from dash_tailwindcss_plugin import setup_tailwindcss_plugin

# 在线模式（快速开发）
setup_tailwindcss_plugin(mode="online")

# 离线模式（生产推荐）
setup_tailwindcss_plugin(mode="offline", download_node=True)

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Hello!", className="text-3xl font-bold text-blue-600"),
], className="p-8")
```

### 模式对比

| 特性 | 在线模式 | 离线模式 |
|------|---------|---------|
| 启动速度 | 快 | 首次较慢 |
| CSS 体积 | 大（全量） | 小（按需） |
| 网络依赖 | 需要 | 不需要 |
| 适用场景 | 开发原型 | 生产环境 |

**详细文档**：[plugins.md](./plugins.md)

---

## dash-vite-plugin

> Vite 构建集成 | 支持 Vue.js 和 React

### 快速开始

```python
from dash import Dash, html
from dash_vite_plugin import VitePlugin, NpmPackage

vite_plugin = VitePlugin(
    build_assets_paths=['assets/js', 'assets/vue'],
    entry_js_paths=['assets/js/main.js'],
    npm_packages=[NpmPackage('vue')],
    download_node=True,
)

vite_plugin.setup()      # 必须在 Dash() 之前
app = Dash(__name__)
vite_plugin.use(app)     # 必须在 Dash() 之后

app.layout = html.Div(id='vue-container')
```

### 调用顺序（关键！）

```
VitePlugin() → setup() → Dash() → use(app) → app.run()
```

**详细文档**：[plugins.md](./plugins.md)

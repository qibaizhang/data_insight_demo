# Dash 开发插件

> dash-tailwindcss-plugin 与 dash-vite-plugin 完整指南
> 现代化前端工具链与 Dash 3.x 的无缝集成

---

## 插件概览

| 插件 | 功能 | 适用场景 |
|------|------|----------|
| **dash-tailwindcss-plugin** | Tailwind CSS 集成 | 快速样式开发、原子化 CSS |
| **dash-vite-plugin** | Vite 构建工具集成 | Vue.js/React 组件嵌入 |

---

# 一、dash-tailwindcss-plugin

## 1.1 概述

**dash-tailwindcss-plugin** 是一个将 Tailwind CSS 集成到 Plotly Dash 3.x 应用的插件，支持在线（CDN）和离线（CLI 构建）两种模式，兼容 Tailwind CSS v3 和 v4。

### 安装

```bash
pip install dash-tailwindcss-plugin
```

---

## 1.2 快速开始

### 在线模式（CDN，快速启动）

```python
from dash import Dash, html
from dash_tailwindcss_plugin import setup_tailwindcss_plugin

setup_tailwindcss_plugin(mode="online")

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Hello TailwindCSS!", className="text-3xl font-bold text-blue-600"),
    html.P("使用 Tailwind CSS 样式", className="text-gray-700 mt-4")
])

if __name__ == "__main__":
    app.run(debug=True)
```

### 离线模式（CLI 构建，生产推荐）

```python
from dash import Dash, html
from dash_tailwindcss_plugin import setup_tailwindcss_plugin

setup_tailwindcss_plugin(
    mode="offline",
    download_node=True,  # 自动下载 Node.js
    clean_after=False    # 开发环境建议 False
)

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Hello TailwindCSS!", className="text-3xl font-bold text-blue-600"),
    html.P("使用本地构建的 Tailwind CSS", className="text-gray-700 mt-4")
])

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 1.3 模式对比

| 特性 | 在线模式 (online) | 离线模式 (offline) |
|------|-------------------|-------------------|
| **启动速度** | 快（无构建） | 首次较慢（需构建） |
| **CSS 体积** | 大（全量 CSS） | 小（按需生成） |
| **网络依赖** | 需要 | 不需要 |
| **Node.js** | 不需要 | 需要 |
| **自定义主题** | 有限 | 完全支持 |
| **适用场景** | 开发原型、学习 | 生产环境 |

---

## 1.4 核心 API

### setup_tailwindcss_plugin() 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `mode` | `'online'` \| `'offline'` | `'offline'` | 在线用 CDN，离线用 CLI 构建 |
| `tailwind_version` | `'3'` \| `'4'` | `'3'` | Tailwind CSS 版本 |
| `content_path` | `List[str]` | `['**/*.py']` | 扫描 Tailwind 类的文件 glob 模式 |
| `plugin_tmp_dir` | `str` | `'_tailwind'` | 插件临时目录 |
| `download_node` | `bool` | `False` | 自动下载 Node.js |
| `node_version` | `str` | `'18.17.0'` | Node.js 版本 |
| `tailwind_theme_config` | `Dict` | `None` | 自定义主题配置 |
| `clean_after` | `bool` | `True` | 构建后清理临时文件 |
| `skip_build_if_recent` | `bool` | `True` | 跳过近期构建 |
| `skip_build_time_threshold` | `int` | `5` | 跳过阈值（秒） |

---

## 1.5 环境配置推荐

### 开发环境

```python
setup_tailwindcss_plugin(
    mode="offline",
    download_node=True,           # 自动下载 Node.js
    clean_after=False,            # 保留文件加快热重载
    skip_build_if_recent=True,    # 智能跳过构建
    skip_build_time_threshold=10  # 10秒内不重复构建
)
```

### 生产环境

```python
setup_tailwindcss_plugin(
    mode="offline",
    download_node=False,          # 使用系统 Node.js
    clean_after=True,             # 清理临时文件
    content_path=["app/**/*.py"], # 精确指定扫描路径
    tailwind_theme_config={...}   # 自定义主题
)
```

---

## 1.6 自定义主题配置

```python
theme_config = {
    "colors": {
        "brand": {
            "50": "#eff6ff",
            "500": "#3b82f6",
            "900": "#1e3a8a"
        },
        "accent": "#f59e0b"
    },
    "spacing": {
        "128": "32rem",
        "144": "36rem"
    },
    "borderRadius": {
        "4xl": "2rem"
    },
    "fontFamily": {
        "display": ["Poppins", "sans-serif"]
    }
}

setup_tailwindcss_plugin(
    mode="offline",
    tailwind_theme_config=theme_config
)

# 使用示例
html.H1("标题", className="text-brand-500 font-display")
```

---

## 1.7 常用 UI 组件模板

### 响应式卡片网格

```python
html.Div([
    html.Div([
        html.Img(src="image1.jpg", className="w-full h-48 object-cover"),
        html.Div([
            html.H3("卡片标题", className="text-lg font-semibold"),
            html.P("卡片描述文字", className="text-gray-600 mt-2"),
        ], className="p-4")
    ], className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"),
], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6")
```

### 按钮组

```python
html.Div([
    html.Button("主要按钮", className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"),
    html.Button("边框按钮", className="border border-blue-500 text-blue-500 hover:bg-blue-50 font-bold py-2 px-4 rounded"),
], className="flex gap-2")
```

### 警告/提示框

```python
html.Div("信息提示", className="p-4 text-blue-700 bg-blue-100 rounded-lg")
html.Div("成功提示", className="p-4 text-green-700 bg-green-100 rounded-lg")
html.Div("警告提示", className="p-4 text-yellow-700 bg-yellow-100 rounded-lg")
html.Div("错误提示", className="p-4 text-red-700 bg-red-100 rounded-lg")
```

---

## 1.8 Tailwind 常用类名速查

| 类别 | 常用类名 |
|------|----------|
| **Flexbox** | `flex`, `flex-col`, `items-center`, `justify-between`, `gap-4` |
| **Grid** | `grid`, `grid-cols-1`, `md:grid-cols-2`, `lg:grid-cols-3`, `gap-6` |
| **Padding** | `p-4`, `px-4`, `py-2`, `pt-4`, `pb-4` |
| **Margin** | `m-4`, `mx-auto`, `my-4`, `mt-4`, `mb-4` |
| **宽度** | `w-full`, `w-1/2`, `max-w-md`, `max-w-lg` |
| **文字大小** | `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl` |
| **文字粗细** | `font-light`, `font-normal`, `font-medium`, `font-semibold`, `font-bold` |
| **背景色** | `bg-white`, `bg-gray-100`, `bg-blue-500` |
| **边框** | `border`, `border-2`, `rounded`, `rounded-lg`, `rounded-full` |
| **阴影** | `shadow`, `shadow-md`, `shadow-lg`, `shadow-xl` |
| **悬停** | `hover:bg-blue-600`, `hover:text-white`, `hover:shadow-lg` |

### 响应式前缀

| 前缀 | 断点 | 说明 |
|------|------|------|
| `sm:` | 640px | 小屏幕及以上 |
| `md:` | 768px | 中屏幕及以上 |
| `lg:` | 1024px | 大屏幕及以上 |
| `xl:` | 1280px | 超大屏幕及以上 |

---

# 二、dash-vite-plugin

## 2.1 概述

**dash-vite-plugin** 是一个用于在 Plotly Dash 3.x 应用中集成 Vite 构建工具的插件。它利用 Dash 3.x 的 hooks 机制，让开发者能够在 Dash 应用中使用现代化的前端框架（Vue.js、React）。

### 基本信息

| 项目 | 内容 |
|-----|-----|
| 包名 | `dash-vite-plugin` |
| 版本 | 0.1.2 |
| Python 版本 | >=3.8 |
| 核心依赖 | `dash>=3.0.3`, `py-node-manager>=0.1.1` |
| GitHub | https://github.com/HogaStack/dash-vite-plugin |

### 安装

```bash
pip install dash-vite-plugin
```

---

## 2.2 核心特性

- ✅ 完全兼容 Dash 3.x（利用 hooks 机制）
- ✅ 支持 Vue.js 和 React 前端框架
- ✅ 自动化 Node.js 环境管理（可自动下载）
- ✅ 支持 Less 和 Sass CSS 预处理器
- ✅ 智能跳过最近构建的文件
- ✅ 自动将构建产物注入 Dash HTML

---

## 2.3 调用顺序（关键！）

```
VitePlugin() → setup() → Dash() → use(app) → app.run()
```

⚠️ **重要**：必须严格按照此顺序调用，否则插件无法正常工作！

---

## 2.4 Vue.js 集成示例

### 目录结构

```
project/
├── assets/
│   ├── js/
│   │   └── main.js          # 入口文件
│   └── vue/
│       └── App.vue          # Vue 组件
├── app.py                   # Dash 应用
└── _vite/                   # 插件临时目录（自动生成）
```

### 入口文件 (assets/js/main.js)

```javascript
import { createApp } from "vue";
import App from "../vue/App.vue";

function waitForElement(selector) {
  return new Promise((resolve) => {
    const element = document.querySelector(selector);
    if (element) {
      resolve(element);
      return;
    }
    const observer = new MutationObserver(() => {
      const el = document.querySelector(selector);
      if (el) {
        observer.disconnect();
        resolve(el);
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  });
}

waitForElement("#vue-container").then((element) => {
  createApp(App).mount(element);
});
```

### Dash 应用 (app.py)

```python
from dash import Dash, html
from dash_vite_plugin import VitePlugin, NpmPackage

vite_plugin = VitePlugin(
    build_assets_paths=['assets/js', 'assets/vue'],
    entry_js_paths=['assets/js/main.js'],
    npm_packages=[NpmPackage('vue')],
    download_node=True,
    clean_after=True,
)

vite_plugin.setup()
app = Dash(__name__)
vite_plugin.use(app)

app.layout = html.Div([
    html.H1('Dash + Vue.js'),
    html.Div(id='vue-container'),  # Vue 挂载点
])

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 2.5 React 集成示例

```python
from dash import Dash, html
from dash_vite_plugin import VitePlugin, NpmPackage

vite_plugin = VitePlugin(
    build_assets_paths=['assets/js', 'assets/react'],
    entry_js_paths=['assets/js/main.js'],
    npm_packages=[
        NpmPackage('react'),
        NpmPackage('react-dom'),
    ],
    download_node=True,
    clean_after=True,
)

vite_plugin.setup()
app = Dash(__name__)
vite_plugin.use(app)

app.layout = html.Div([
    html.H1('Dash + React'),
    html.Div(id='react-container'),  # React 挂载点
])

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 2.6 VitePlugin API

### 构造函数参数

| 参数 | 类型 | 默认值 | 必需 | 描述 |
|-----|------|-------|-----|------|
| `build_assets_paths` | `List[str]` | - | ✅ | 要构建的资源路径列表 |
| `entry_js_paths` | `List[str]` | - | ✅ | 入口 JavaScript 文件路径列表 |
| `npm_packages` | `List[NpmPackage]` | - | ✅ | 需要安装的 npm 包列表 |
| `plugin_tmp_dir` | `str` | `'_vite'` | ❌ | 插件临时目录名称 |
| `support_less` | `bool` | `False` | ❌ | 是否启用 Less 支持 |
| `support_sass` | `bool` | `False` | ❌ | 是否启用 Sass 支持 |
| `download_node` | `bool` | `False` | ❌ | 未找到 Node.js 时是否自动下载 |
| `node_version` | `str` | `'18.20.8'` | ❌ | 要下载的 Node.js 版本 |
| `clean_after` | `bool` | `False` | ❌ | 构建后是否清理临时文件 |
| `skip_build_if_recent` | `bool` | `True` | ❌ | 是否跳过最近已构建的文件 |
| `skip_build_time_threshold` | `int` | `5` | ❌ | 判定为"最近构建"的阈值（秒） |

### NpmPackage 类

```python
from dash_vite_plugin import NpmPackage

npm_packages = [
    NpmPackage('vue'),                          # 最新版本，生产依赖
    NpmPackage('react', '18.2.0'),              # 指定版本
    NpmPackage('sass', install_mode='-D'),      # 开发依赖
    NpmPackage('lodash', '4.17.21', '-S'),      # 完整参数
]
```

---

## 2.7 工作流程

```
① 初始化阶段
   └─→ 创建 vite.config.js、index.html、package.json
   └─→ 复制资源文件到临时目录 (_vite/)

② 安装阶段
   └─→ npm init -y
   └─→ 安装 Vite 和插件 (@vitejs/plugin-react, @vitejs/plugin-vue)
   └─→ 安装用户指定的 npm 包

③ 构建阶段
   └─→ npx vite build
   └─→ 生成优化的静态文件到 _vite/dist/

④ 集成阶段
   └─→ 提取 dist/index.html 中的 <script> 和 <link> 标签
   └─→ 注入到 Dash 应用的 HTML <head> 中
   └─→ 设置 /_static/ 路由服务静态文件

⑤ 清理阶段（可选，clean_after=True）
   └─→ 删除临时配置文件和 node_modules
```

---

# 三、feffery-dash-utils (fdu)

Python 工具库，提供样式、模板等便利函数。

### 安装

```bash
pip install feffery-dash-utils
```

### style 工具函数

```python
from feffery_dash_utils.style_utils import style

html.Div(
    '内容',
    style=style(
        padding=20,
        margin='10px 0',
        backgroundColor='#f5f5f5',
        borderRadius=8,
        boxShadow='0 2px 8px rgba(0,0,0,0.1)'
    )
)
```

### 仪表盘模板组件

```python
from feffery_dash_utils.template_utils.dashboard_components import (
    welcome_card,
    index_card,
    simple_chart_card,
    blank_card
)

# 欢迎卡片
welcome_card(title='欢迎回来', subtitle='今天是美好的一天')

# 指标卡片
index_card(title='总销售额', value=123456, prefix='¥', trend='up', trend_value='12.5%')

# 图表卡片
simple_chart_card(title='销售趋势', children=fact.AntdLine(...))
```

---

# 四、常见问题速查

| 错误现象 | 可能原因 | 解决方案 |
|----------|----------|----------|
| Tailwind 样式不生效 | 插件未正确初始化 | 确保 `setup_tailwindcss_plugin()` 在 `Dash()` 之前调用 |
| 离线模式构建失败 | 缺少 Node.js | 设置 `download_node=True` |
| Vite 调用顺序错误 | `setup()` 在 `Dash()` 之后 | 按照 `setup() → Dash() → use()` 顺序调用 |
| Vue/React 组件不显示 | 挂载点不存在 | 确保 HTML 中有对应的 `id` 容器 |
| 启动缓慢 | 每次都重新构建 | 设置 `clean_after=False` 和 `skip_build_if_recent=True` |

---

## 版本兼容性

| 依赖 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.8+ | 3.10+ |
| Dash | 3.0.3+ | 最新 |
| Node.js | 12+ | 18.x LTS |
| Tailwind CSS | v3 / v4 | v3（稳定） |

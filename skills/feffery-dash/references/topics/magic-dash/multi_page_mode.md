# magic-dash 多页面应用模板

> magic-dash 基础多页面应用开发模式
> 采用视图（Views）、逻辑（Callbacks）、配置（Configs）分离的架构模式

---

## 创建方式

```bash
magic-dash create --name magic-dash
```

---

## 项目结构

```
magic-dash/
├── assets/                 # 静态资源目录
│   ├── css/               # 样式文件目录
│   │   ├── base.css       # 基础样式
│   │   └── core.css       # 核心页面样式
│   ├── imgs/              # 图片文件目录
│   │   ├── logo.svg       # 应用 Logo
│   │   ├── init_loading.gif  # 加载动画
│   │   └── status/        # 状态页面图片
│   ├── js/                # 浏览器回调函数目录
│   │   └── basic_callbacks.js
│   └── favicon.ico        # 网页图标
├── callbacks/             # 回调函数模块
│   ├── __init__.py
│   └── core_pages_c/      # 核心页面回调
│       └── __init__.py
├── components/            # 自定义组件模块
│   ├── __init__.py
│   ├── core_side_menu.py  # 侧边菜单组件
│   └── page_content.py    # 页面内容组件
├── configs/               # 配置参数模块
│   ├── __init__.py
│   ├── base_config.py     # 基础配置
│   ├── layout_config.py   # 布局配置
│   └── router_config.py   # 路由配置
├── utils/                 # 工具函数模块
│   └── clear_pycache.py
├── views/                 # 页面模块
│   ├── __init__.py
│   ├── core_pages/        # 核心功能页面
│   │   ├── __init__.py
│   │   ├── index.py       # 首页
│   │   ├── page1.py       # 示例页面
│   │   └── ...
│   └── status_pages/      # 状态页面
│       ├── _404.py        # 404 页面
│       └── _500.py        # 500 页面
├── server.py              # 应用初始化模块
├── app.py                 # 应用主文件
└── requirements.txt       # 项目依赖信息
```

---

## 启动应用

```bash
pip install -r requirements.txt
python app.py
# 访问 http://127.0.0.1:8050
```

---

## 核心运行机制

### 路由机制

1. **路由监听**：`app.py` 中通过 `fuc.FefferyLocation(id="root-url")` 监听 URL 变化
2. **内容渲染**：主布局中 `html.Div(id="root-container")` 作为页面内容容器
3. **回调逻辑**：`root_router` 回调函数根据 `pathname` 调用对应 `views` 模块的 `.render()` 方法

### 错误处理

- **404 Not Found**：当 `pathname` 不在 `RouterConfig.valid_pathnames` 中时，渲染 404 页面
- **500 Internal Error**：`handle_root_router_error` 捕获全局回调错误，渲染 500 状态页

---

## 二次开发指南：添加新页面

### 步骤 1: 注册路由配置

打开 `configs/router_config.py`：

```python
class RouterConfig:
    # 1. 在 core_side_menu 中添加菜单项
    core_side_menu: List[dict] = [
        {
            "component": "ItemGroup",
            "props": {"title": "主要页面", "key": "主要页面"},
            "children": [
                # ... 现有菜单项
                {
                    "component": "Item",
                    "props": {
                        "title": "新页面",           # 菜单显示名称
                        "key": "/core/new-page",    # 唯一标识（与 href 一致）
                        "icon": "antd-app-store",   # Antd 图标名称
                        "href": "/core/new-page",   # URL 路径
                    },
                },
            ],
        },
    ]

    # 2. 在 valid_pathnames 中注册路径
    valid_pathnames: dict = {
        # ... 现有路径
        "/core/new-page": "新页面",  # 路径 -> 页面标题
    }
```

### 步骤 2: 创建视图文件

在 `views/core_pages/` 下创建 `new_page.py`：

```python
from dash import html
import feffery_antd_components as fac


def render():
    """页面渲染函数"""
    return html.Div(
        [
            fac.AntdAlert(message="这是新页面", type="info", showIcon=True),
            # 在此编写页面布局
        ]
    )
```

### 步骤 3: 注册回调逻辑

打开 `callbacks/core_pages_c/__init__.py`：

```python
# 1. 导入新页面视图模块
from views.core_pages import new_page

# 2. 在 root_router 函数的路由逻辑中添加分支
# （通常在 views/core_pages/__init__.py 的 render 函数中处理）
```

或者在 `views/core_pages/__init__.py` 的 `render` 函数中添加页面匹配逻辑。

### 步骤 4: 添加页面回调（可选）

如果页面有交互逻辑，在 `callbacks/core_pages_c/` 下创建回调文件：

```python
# callbacks/core_pages_c/new_page_c.py
from server import app  # 必须从 server 导入
from dash.dependencies import Input, Output


@app.callback(
    Output("new-page-output", "children"),
    Input("new-page-button", "nClicks"),
    prevent_initial_call=True,
)
def handle_click(n_clicks):
    return f"点击了 {n_clicks} 次"
```

**重要：** 必须在 `callbacks/__init__.py` 中导入该模块，否则回调不会生效：

```python
# callbacks/__init__.py
from . import core_pages_c
from .core_pages_c import new_page_c  # 添加这行
```

---

## 配置说明

### BaseConfig 基础配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `min_browser_versions` | 浏览器最低版本检测 | Chrome 88, Firefox 78, Edge 100 |
| `strict_browser_type_check` | 严格浏览器类型限制 | `False` |
| `app_title` | 应用基础标题 | `'Magic Dash'` |
| `app_version` | 应用版本号 | - |

### LayoutConfig 布局配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `core_side_width` | 核心页面侧边栏像素宽度 | `350` |
| `core_layout_type` | 核心页面呈现类型 | `'single'`（可选 `'tabs'`） |
| `show_core_page_search` | 是否展示页面搜索框 | `True` |

### RouterConfig 路由配置

| 配置项 | 说明 |
|--------|------|
| `index_pathname` | 首页路径别名，默认 `/index` |
| `core_side_menu` | 核心页面侧边菜单结构 |
| `valid_pathnames` | 有效页面路径 -> 标题映射字典 |
| `independent_core_pathnames` | 独立渲染页面路径列表 |
| `side_menu_open_keys` | 子菜单自动展开配置 |
| `wildcard_patterns` | 通配页面模式字典（正则表达式） |

---

## 菜单结构说明

### 菜单项类型

```python
# 1. 普通菜单项 (Item)
{
    "component": "Item",
    "props": {
        "title": "页面名称",
        "key": "/core/page-path",
        "icon": "antd-home",  # Antd 图标名称
        "href": "/core/page-path",
    },
}

# 2. 菜单分组 (ItemGroup)
{
    "component": "ItemGroup",
    "props": {"title": "分组标题", "key": "分组标题"},
    "children": [
        # 子菜单项...
    ],
}

# 3. 子菜单 (SubMenu)
{
    "component": "SubMenu",
    "props": {
        "key": "子菜单标识",
        "title": "子菜单标题",
        "icon": "antd-catalog",
    },
    "children": [
        # 子菜单项...
    ],
}
```

### 子菜单自动展开配置

当页面隶属于子菜单时，配置 `side_menu_open_keys`：

```python
side_menu_open_keys: dict = {
    "/core/sub-menu-page1": ["子菜单演示"],  # 页面路径 -> 需展开的菜单 key 列表
    "/core/sub-menu-page2": ["子菜单演示"],
}
```

---

## 通配页面模式

支持基于正则表达式的动态路由：

```python
import re

class RouterConfig:
    # 定义通配模式
    wildcard_patterns: dict = {
        "详情页面": re.compile(r"^/core/detail/(.*?)$")
    }

    # 在 valid_pathnames 中注册
    valid_pathnames: dict = {
        # ... 其他路径
        wildcard_patterns["详情页面"]: "详情页面",
    }
```

---

## 修改应用基础信息

### 修改标题/版本

编辑 `configs/base_config.py`：

```python
class BaseConfig:
    app_title: str = "我的应用"
    app_version: str = "1.0.0"
```

### 修改 Logo/图标

- 替换 `assets/favicon.ico`
- 替换 `assets/imgs/logo.svg`

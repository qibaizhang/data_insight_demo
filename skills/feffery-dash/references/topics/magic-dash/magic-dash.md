# magic-dash

> magic-dash CLI 项目脚手架工具 Skill
> 三个模板：simple-tool | magic-dash | magic-dash-pro

当用户需要快速创建 Dash 项目或使用项目模板时使用。

---

## 概述

magic-dash 是一个命令行工具，用于快捷生成开箱即用的标准 Dash 应用工程模板。

**安装：**
```bash
pip install magic-dash -U
```

---

## CLI 命令

```bash
# 查看内置项目模板
magic-dash list

# 生成指定项目模板（到当前路径）
magic-dash create --name <模板名称>

# 生成到指定路径
magic-dash create --name <模板名称> --path <目标路径>

# 查看版本
magic-dash --version

# 查看帮助
magic-dash --help
magic-dash list --help
magic-dash create --help
```

---

## 三个内置模板

| 模板名称 | 描述 | 适用场景 |
|----------|------|----------|
| `simple-tool` | 单页面工具应用模板 | 简单工具、快速原型 |
| `magic-dash` | 基础多页面应用模板 | 中型应用、多页导航 |
| `magic-dash-pro` | 多页面+用户登录应用模板 | 企业应用、用户管理、权限控制 |

---

## 1. simple-tool 单页面模板

最简单的项目结构，适合快速原型开发。

### 创建方式

```bash
magic-dash create --name simple-tool
```

### 项目结构

```
simple-tool/
├── app.py              # 应用主文件
└── requirements.txt    # 项目依赖信息
```

### 启动应用

```bash
pip install -r requirements.txt
python app.py
# 访问 http://127.0.0.1:8050
```

### 详细文档

→ 参见 [single_page_mode.md](./single_page_mode.md)

---

## 2. magic-dash 多页面模板

支持多页面路由的基础应用模板，采用视图/回调/配置分离的架构。

### 创建方式

```bash
magic-dash create --name magic-dash
```

### 项目结构

```
magic-dash/
├── assets/             # 静态资源目录
│   ├── css/            # 样式文件目录
│   ├── imgs/           # 图片文件目录
│   ├── js/             # 浏览器回调函数目录
│   └── favicon.ico     # 网页图标
├── callbacks/          # 回调函数模块
├── components/         # 自定义组件模块
├── configs/            # 配置参数模块
├── utils/              # 工具函数模块
├── views/              # 页面模块
├── server.py           # 应用初始化模块
├── app.py              # 应用主文件
└── requirements.txt    # 项目依赖信息
```

### 启动应用

```bash
pip install -r requirements.txt
python app.py
# 访问 http://127.0.0.1:8050
```

### 配置说明

#### BaseConfig 基础配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `min_browser_versions` | 浏览器最低版本检测 | Chrome 88, Firefox 78, Edge 100 |
| `strict_browser_type_check` | 严格浏览器类型限制 | `False` |
| `app_title` | 应用基础标题 | `'Magic Dash'` |
| `app_version` | 应用版本号 | - |

#### LayoutConfig 布局配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `core_side_width` | 核心页面侧边栏像素宽度 | `350` |
| `core_layout_type` | 核心页面呈现类型 | `'single'` (可选 `'tabs'`) |
| `show_core_page_search` | 是否展示页面搜索框 | `True` |

#### RouterConfig 路由配置

| 配置项 | 说明 |
|--------|------|
| `index_pathname` | 首页路径别名，默认 `/index` |
| `core_side_menu` | 核心页面侧边菜单结构 |
| `valid_pathnames` | 有效页面路径&标题映射 |
| `independent_core_pathnames` | 独立渲染页面路径列表 |
| `side_menu_open_keys` | 子菜单自动展开配置 |
| `wildcard_patterns` | 通配页面模式字典（正则表达式） |

### 详细文档

→ 参见 [multi_page_mode.md](./multi_page_mode.md)

---

## 3. magic-dash-pro 登录认证模板

完整的用户认证系统，支持用户管理和权限控制。

### 创建方式

```bash
magic-dash create --name magic-dash-pro
```

### 项目结构

```
magic-dash-pro/
├── assets/             # 静态资源目录
│   ├── css/
│   ├── imgs/
│   ├── js/
│   ├── videos/         # 登录页视频背景
│   └── favicon.ico
├── callbacks/          # 回调函数模块
├── components/         # 自定义组件模块
├── configs/            # 配置参数模块
├── models/             # 数据库模型模块
├── utils/              # 工具函数模块
├── views/              # 页面模块
├── magic_dash_pro.db   # 数据库文件（初始化后自动生成）
├── server.py           # 应用初始化模块
├── app.py              # 应用主文件
└── requirements.txt    # 项目依赖信息
```

### 启动应用

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库（必须）
python -m models.init_db

# 3. 启动应用
python app.py

# 访问 http://127.0.0.1:8050
# 默认管理员账号：admin / admin123
```

### 详细文档

→ 参见 [login_app_mode.md](./login_app_mode.md)

---

## 开发规范

### 添加新页面步骤

1. 在 `configs/router_config.py` 中注册路由和菜单
2. 在 `views/core_pages/` 下创建页面视图模块
3. 在 `callbacks/core_pages_c/` 下创建对应的回调模块（如有交互）
4. 在 `callbacks/__init__.py` 中导入回调模块

### 回调模块规范

```python
# callbacks/xxx_c.py
from server import app  # 必须从 server 导入
from dash.dependencies import Input, Output

@app.callback(
    Output('output-id', 'children'),
    Input('input-id', 'nClicks'),
    prevent_initial_call=True,
)
def my_callback(n):
    return f'点击了 {n} 次'
```

### 视图模块规范

```python
# views/xxx.py
from dash import html
import feffery_antd_components as fac

def render():
    """页面渲染函数"""
    return html.Div([
        fac.AntdCard(
            title='页面标题',
            children=[...]
        )
    ])
```

---

## 生产部署

```bash
# 使用 gunicorn 启动
gunicorn server:server -b 0.0.0.0:8050 -w 4
```

---

## 依赖版本要求

magic-dash 模板要求以下依赖版本：
- `dash>=3.3.0,<4.0.0`
- `feffery_antd_components>=0.4.0,<0.5.0`
- `feffery_utils_components>=0.3.2,<0.4.0`
- `feffery_dash_utils>=0.2.6`
- Python 3.8 - 3.13

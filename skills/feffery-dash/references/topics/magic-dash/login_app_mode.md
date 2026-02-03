# magic-dash-pro 多页面用户登录应用模板

> magic-dash 企业级多页面应用开发模式
> 支持用户登录、基于角色的权限控制 (RBAC)、单点登录限制

---

## 创建方式

```bash
magic-dash create --name magic-dash-pro
```

---

## 项目结构

```
magic-dash-pro/
├── assets/                 # 静态资源目录
│   ├── css/
│   │   ├── base.css       # 基础样式
│   │   ├── core.css       # 核心页面样式
│   │   └── login.css      # 登录页样式
│   ├── imgs/
│   │   ├── logo.svg
│   │   ├── init_loading.gif
│   │   ├── login/         # 登录页面图片资源
│   │   └── status/        # 状态页面图片
│   ├── js/
│   │   └── basic_callbacks.js
│   ├── videos/            # 视频资源（登录页背景）
│   │   └── login-bg.mp4
│   └── favicon.ico
├── callbacks/             # 回调函数模块
│   ├── __init__.py
│   ├── login_c.py         # 登录相关回调
│   └── core_pages_c/      # 核心页面回调
├── components/            # 自定义组件模块
│   ├── __init__.py
│   ├── core_side_menu.py  # 侧边菜单
│   ├── page_content.py    # 页面内容
│   ├── personal_info.py   # 个人信息组件
│   └── user_manage.py     # 用户管理组件
├── configs/               # 配置参数模块
│   ├── __init__.py
│   ├── base_config.py     # 基础配置
│   ├── layout_config.py   # 布局配置
│   ├── router_config.py   # 路由配置
│   ├── auth_config.py     # 用户鉴权配置
│   └── database_config.py # 数据库配置
├── models/                # 数据库模型模块
│   ├── __init__.py
│   ├── init_db.py         # 数据库初始化
│   ├── users.py           # 用户模型
│   ├── logs.py            # 日志模型
│   └── exceptions.py      # 异常定义
├── utils/                 # 工具函数模块
│   └── clear_pycache.py
├── views/                 # 页面模块
│   ├── __init__.py
│   ├── login.py           # 登录页面
│   ├── core_pages/        # 核心功能页面
│   └── status_pages/      # 状态页面（403/404/500）
├── magic_dash_pro.db      # SQLite 数据库（初始化后生成）
├── server.py              # 应用初始化模块
├── app.py                 # 应用主文件
└── requirements.txt       # 项目依赖信息
```

---

## 应用初始化启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库（必须执行）
python -m models.init_db

# 3. 启动应用
python app.py

# 访问 http://127.0.0.1:8050
# 默认管理员账号: admin / admin123
```

---

## 核心技术栈

- **框架：** Dash + Flask
- **认证：** `flask-login` (用户会话管理)
- **权限：** `flask-principal` (角色与权限管理)
- **数据库：** SQLite (默认)，可扩展 PostgreSQL / MySQL

---

## 权限控制体系

### 角色定义与页面权限

在 `configs/auth_config.py` 中配置：

```python
class AuthConfig:
    # 角色权限类别定义
    roles: dict = {
        "admin": {
            "type": "all"  # 允许访问所有页面
        },
        "normal": {
            "type": "include",  # 白名单模式
            "keys": ["/core/home", "/core/dashboard"]  # 仅能访问这些
        },
        "guest": {
            "type": "exclude",  # 黑名单模式
            "keys": ["/core/admin-panel"]  # 不能访问这些
        }
    }

    # 常规用户角色键名
    normal_role: str = "normal"

    # 管理员角色键名
    admin_role: str = "admin"
```

### 权限类型说明

| 类型 | 说明 |
|------|------|
| `type="all"` | 允许访问所有页面（管理员） |
| `type="include"` | 白名单模式，仅允许访问 `keys` 列表中的路径 |
| `type="exclude"` | 黑名单模式，禁止访问 `keys` 列表中的路径 |

**注意：** 路由拦截是自动的。如果用户访问无权页面，系统会自动重定向到 403 页面。

### 细粒度内容权限（组件级）

在视图或回调中根据当前用户角色动态渲染内容：

```python
from flask_login import current_user
from configs.auth_config import AuthConfig


def render():
    # 仅管理员可见的按钮
    if current_user.user_role == AuthConfig.admin_role:
        admin_button = fac.AntdButton("管理操作", type="primary", danger=True)
    else:
        admin_button = None

    return html.Div([
        # 通用内容
        fac.AntdAlert(message="欢迎", type="info"),
        # 管理员专属内容
        admin_button,
    ])
```

### API 接口权限保护

在 `server.py` 中使用 Flask-Principal 定义权限装饰器：

```python
from flask_principal import Permission, RoleNeed

# 定义管理员权限
admin_permission = Permission(RoleNeed("admin"))


@app.server.route("/api/sensitive-data")
@admin_permission.require(http_exception=403)
def sensitive_data():
    return {"data": "secret"}
```

---

## 安全机制：单点登录限制

防止同一账号在多地（多浏览器/设备）同时登录。

### 机制原理

1. **Token 比对：** 数据库 `User` 表存储 `session_token`
2. **登录更新：** 每次登录生成新 Token 存入数据库和浏览器 Cookie
3. **前端轮询：** 前端通过 `dcc.Interval` 定期请求后端
4. **后端校验：** 比较 Cookie 中的 Token 与数据库是否一致，不一致则强制登出

### 配置开启

在 `configs/base_config.py` 中：

```python
class BaseConfig:
    # 开启重复登录检测
    enable_duplicate_login_check: bool = True

    # 检查间隔（秒）
    duplicate_login_check_interval: int = 10

    # 登录会话 token 的 cookies 名称
    session_token_cookie_name: str = "session_token"
```

---

## 全屏水印功能

### 配置开启

```python
class BaseConfig:
    # 开启全屏水印
    enable_fullscreen_watermark: bool = True

    # 水印内容生成函数
    fullscreen_watermark_generator = lambda current_user: current_user.user_name
```

---

## 二次开发指南：添加新功能页面

### 步骤 1: 定义菜单与路由

编辑 `configs/router_config.py`：

```python
class RouterConfig:
    core_side_menu: List[dict] = [
        # ... 现有菜单
        {
            "component": "Item",
            "props": {
                "title": "新功能页面",
                "icon": "antd-app-store",
                "key": "/core/new-feature",
                "href": "/core/new-feature"
            }
        },
    ]

    valid_pathnames: dict = {
        # ... 现有路径
        "/core/new-feature": "新功能页面",
    }
```

### 步骤 2: 创建页面视图

在 `views/core_pages/` 下创建 `new_feature.py`：

```python
from dash import html
import feffery_antd_components as fac


def render():
    return html.Div([
        fac.AntdButton("点击我", id="new-btn", type="primary"),
        html.Div(id="new-output")
    ])
```

### 步骤 3: 注册路由逻辑

在 `views/core_pages/__init__.py` 的路由匹配逻辑中添加新页面。

### 步骤 4: 编写回调（如有交互）

在 `callbacks/core_pages_c/` 下创建 `new_feature_c.py`：

```python
from server import app
from dash.dependencies import Input, Output


@app.callback(
    Output("new-output", "children"),
    Input("new-btn", "nClicks"),
    prevent_initial_call=True,
)
def handle_click(n):
    return f"点击了 {n} 次"
```

**重要：** 在 `callbacks/__init__.py` 或 `app.py` 中导入该模块。

### 步骤 5: 配置权限（可选）

在 `configs/auth_config.py` 中配置访问权限：

```python
roles = {
    "admin": {"type": "all"},
    "normal": {
        "type": "include",
        "keys": ["/core/home", "/core/new-feature"]  # 添加新页面
    }
}
```

---

## 配置说明

### BaseConfig 基础配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `app_title` | 应用基础标题 | `'Magic Dash'` |
| `app_version` | 应用版本号 | - |
| `app_secret_key` | 应用密钥（用户登录底层逻辑） | - |
| `enable_duplicate_login_check` | 开启重复登录检测 | `False` |
| `duplicate_login_check_interval` | 重复登录检测间隔（秒） | `10` |
| `session_token_cookie_name` | 登录会话 token 的 cookies 名 | `'session_token'` |
| `enable_fullscreen_watermark` | 开启全屏水印 | `False` |
| `fullscreen_watermark_generator` | 水印内容生成函数 | `lambda u: u.user_name` |

### LayoutConfig 布局配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `core_side_width` | 侧边栏像素宽度 | `350` |
| `login_left_side_content_type` | 登录页左侧内容类型 | `'image'`（可选 `'video'`） |
| `core_layout_type` | 核心页面呈现类型 | `'single'`（可选 `'tabs'`） |
| `show_core_page_search` | 是否展示页面搜索框 | `True` |

### RouterConfig 路由配置

| 配置项 | 说明 |
|--------|------|
| `index_pathname` | 首页路径别名 |
| `core_side_menu` | 侧边菜单结构 |
| `valid_pathnames` | 有效页面路径映射 |
| `independent_core_pathnames` | 独立渲染页面路径列表 |
| `public_pathnames` | 无需登录的公开页面路径列表 |
| `side_menu_open_keys` | 子菜单自动展开配置 |
| `wildcard_patterns` | 通配页面模式字典 |

**public_pathnames 默认值：**
```python
["/login", "/logout", "/403-demo", "/404-demo", "/500-demo"]
```

### DatabaseConfig 数据库配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `database_type` | 数据库类型 | `'sqlite'` |
| `postgresql_config` | PostgreSQL 连接参数 | - |
| `mysql_config` | MySQL 连接参数 | - |

**支持的数据库类型：** `'sqlite'`、`'postgresql'`、`'mysql'`

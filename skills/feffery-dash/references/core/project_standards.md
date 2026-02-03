# Feffery-Dash 项目规范

> 标准化项目结构和开发规范

---

## 1. 依赖安装

### 1.1 核心依赖

```bash
# 核心框架
pip install dash

# Feffery 系列（必装）
pip install feffery-antd-components -U --pre
pip install feffery-utils-components -U --pre
pip install feffery-dash-utils -U

# 可视化（按需）
pip install feffery-antd-charts -U --pre

# 地图（按需）
pip install feffery-leaflet-components -U --pre
pip install feffery-maplibre -U --pre

# Markdown（按需）
pip install feffery-markdown-components -U --pre
```

### 1.2 部署依赖

```bash
# Windows
pip install waitress

# Linux
pip install gunicorn
# 或高性能
pip install granian
```

### 1.3 数据处理

```bash
pip install pandas openpyxl  # Excel 处理
pip install peewee           # 轻量级 ORM
```

---

## 2. 项目结构

### 2.1 单页应用结构

```
simple-app/
├── app.py              # 主入口
├── requirements.txt
└── assets/
    └── base.css
```

### 2.2 多页面应用结构（推荐）

```
project/
├── server.py           # Dash 实例化
├── app.py              # 入口，组装布局
├── config.py           # 配置参数
├── wsgi.py             # 生产部署入口
├── requirements.txt
│
├── assets/             # 静态资源（自动加载）
│   ├── base.css        # 全局样式
│   ├── favicon.ico     # 网站图标
│   └── js/
│       └── callbacks.js  # 客户端回调
│
├── views/              # 视图/布局模块
│   ├── __init__.py
│   ├── index.py        # 首页布局
│   ├── page1.py
│   └── page2.py
│
├── callbacks/          # 回调模块
│   ├── __init__.py
│   ├── index_c.py
│   ├── page1_c.py
│   └── page2_c.py
│
├── components/         # 公共组件
│   ├── __init__.py
│   ├── navbar.py
│   └── sidebar.py
│
├── models/             # 数据库模型
│   ├── __init__.py
│   └── user.py
│
└── utils/              # 工具函数
    ├── __init__.py
    └── helpers.py
```

### 2.3 magic-dash-pro 结构（完整后台）

```
magic-dash-pro/
├── server.py
├── app.py
├── config.py
│
├── views/
│   ├── login.py           # 登录页
│   ├── core_pages/        # 核心页面
│   │   ├── dashboard.py
│   │   └── settings.py
│   └── status_pages/      # 状态页
│       ├── _403.py
│       ├── _404.py
│       └── _500.py
│
├── callbacks/
│   ├── login_c.py
│   └── core_pages_c/
│
├── components/
│   ├── core_side_menu.py  # 侧边菜单
│   ├── user_manage.py     # 用户管理
│   └── personal_info.py   # 个人信息
│
├── configs/
│   ├── base_config.py     # 基础配置
│   ├── auth_config.py     # 认证配置
│   ├── router_config.py   # 路由配置
│   └── database_config.py # 数据库配置
│
└── models/
    ├── users.py
    └── init_db.py
```

---

## 3. 关键文件模板

### 3.1 server.py

```python
"""
Dash 应用实例化
"""
import dash

app = dash.Dash(
    __name__,
    title='应用标题',
    suppress_callback_exceptions=True,  # 动态组件必需
    assets_folder='assets',
)

# 暴露 Flask 实例（部署必需）
server = app.server
```

### 3.2 app.py

```python
"""
应用入口，组装布局和回调
"""
from dash import html, dcc
import feffery_antd_components as fac

from server import app, server

# 导入视图
from views.index import index_layout
from views.page1 import page1_layout

# 导入回调（必须导入以注册）
import callbacks.index_c
import callbacks.page1_c

# 组装布局
app.layout = fac.AntdConfigProvider(
    locale='zh-cn',
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

# 路由回调
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def route(pathname):
    if pathname == '/' or pathname == '/index':
        return index_layout
    elif pathname == '/page1':
        return page1_layout
    return fac.AntdResult(status='404', title='页面不存在')


if __name__ == '__main__':
    app.run(debug=True, port=8050)
```

### 3.3 views/page1.py

```python
"""
页面视图模块
"""
from dash import html
import feffery_antd_components as fac

page1_layout = fac.AntdCard(
    title='页面1',
    children=[
        fac.AntdButton('按钮', id='page1-btn', type='primary'),
        html.Div(id='page1-output')
    ]
)
```

### 3.4 callbacks/page1_c.py

```python
"""
页面回调模块
"""
from dash import Input, Output
from server import app  # 从 server 导入，避免循环引用

@app.callback(
    Output('page1-output', 'children'),
    Input('page1-btn', 'nClicks'),
    prevent_initial_call=True
)
def handle_click(n_clicks):
    return f'点击了 {n_clicks} 次'
```

### 3.5 wsgi.py（生产部署）

```python
"""
生产环境部署入口
"""
from app import app, server

# Windows - Waitress
if __name__ == '__main__':
    from waitress import serve
    serve(server, host='0.0.0.0', port=8050, threads=8)

# Linux - 使用 gunicorn 命令启动
# gunicorn -w 4 -b 0.0.0.0:8050 wsgi:server
```

---

## 4. 命名规范

### 4.1 文件命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 视图文件 | 小写下划线 | `user_list.py` |
| 回调文件 | 视图名 + `_c` | `user_list_c.py` |
| 组件文件 | 小写下划线 | `side_menu.py` |

### 4.2 组件 ID 命名

```python
# 格式：页面前缀-组件类型-功能描述
id='page1-btn-submit'
id='user-table-main'
id='login-input-username'

# 模式匹配 ID
id={'type': 'item-btn', 'index': i}
```

### 4.3 回调函数命名

```python
# 格式：动作_目标
def handle_submit(n_clicks):
    pass

def update_table_data(filter_value):
    pass

def toggle_modal_visible(n_clicks):
    pass
```

---

## 5. 配置管理

### 5.1 config.py

```python
"""
应用配置
"""
import os

class Config:
    # 应用配置
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    # 数据库配置
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')

    # 服务器配置
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8050))

config = Config()
```

### 5.2 使用配置

```python
from config import config

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)
```

---

## 6. assets 目录规范

### 6.1 自动加载规则

- `assets/` 目录下的 `.css` 和 `.js` 文件会自动加载
- 加载顺序：按文件名字母排序
- 可用数字前缀控制顺序：`01_base.css`, `02_theme.css`

### 6.2 推荐结构

```
assets/
├── favicon.ico
├── 01_base.css           # 基础样式
├── 02_theme.css          # 主题样式
├── 03_components.css     # 组件样式
├── js/
│   ├── callbacks.js      # 客户端回调
│   └── utils.js          # 工具函数
└── images/
    └── logo.png
```

### 6.3 base.css 模板

```css
/* 全局样式重置 */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
}

/* 全屏容器 */
.full-height {
    min-height: 100vh;
}
```

---

## 7. Git 忽略配置

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
.env
venv/

# IDE
.vscode/
.idea/

# Dash
.dash_jwt_secret

# 数据库
*.db
*.sqlite

# 日志
*.log

# 临时文件
*.tmp
.DS_Store
```

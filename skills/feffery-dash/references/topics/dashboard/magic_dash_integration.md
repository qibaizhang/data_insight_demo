# Magic-Dash 集成指南

> 将仪表盘集成到 Magic-Dash 多页面框架
> 基于第11课：仪表盘在 magic-dash 中的集成

---

## 框架概述

`magic-dash` 是一个用于快速构建企业级 Dash 应用的 CLI 工具和框架。

### 安装与初始化

```bash
# 安装/更新
pip install magic-dash -U

# 创建项目 (使用 magic-dash-pro 模板)
magic-dash create --name my-dashboard-app

# 进入项目目录
cd my-dashboard-app

# 初始化数据库
python -m models.init_db

# 启动应用
python app.py
```

---

## 项目结构映射

将独立仪表盘代码迁移到框架的 MVC 结构：

| 独立应用 | Magic-Dash 路径 | 说明 |
|----------|-----------------|------|
| `app.py` 中的 `layout` | `views/core_pages/<page>.py` | 页面视图/布局 |
| `app.py` 中的 `@app.callback` | `callbacks/core_pages_c/<page>_c.py` | 回调逻辑 |
| `assets/` 资源 | `assets/images/` 等子目录 | 静态资源 |
| 无 (手动路由) | `configs/router_config.py` | 路由与菜单配置 |
| 回调注册 | `callbacks/__init__.py` | 确保回调生效 |

---

## 集成步骤

### 步骤一：配置路由与菜单

在 `configs/router_config.py` 中添加新页面配置：

```python
# router_config.py
ROUTER_CONFIG = [
    # ... 其他页面配置
    {
        "component": "views.core_pages.dashboard",  # 视图模块路径
        "name": "dashboard",                        # 路由名称
        "title": "数据看板",                        # 侧边栏菜单标题
        "icon": "antd-dashboard",                   # 菜单图标
        "path": "/core/dashboard"                   # URL 路径
    }
]
```

### 步骤二：迁移视图布局

在 `views/core_pages/` 下新建视图文件（如 `dashboard.py`）：

```python
# views/core_pages/dashboard.py

import feffery_antd_components as fac
import feffery_antd_charts as fact
import feffery_utils_components as fuc
from dash import html, dcc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    welcome_card, index_card, simple_chart_card, blank_card
)


def render():
    """页面渲染函数 - 必须定义此函数"""
    return fac.AntdSpace(
        [
            # 全局组件
            dcc.Interval(id="update-data-interval", interval=3000),
            fac.Fragment(id="message-target"),
            dcc.Download(id="global-download"),

            # 主布局
            fac.AntdRow(
                [
                    # 欢迎卡片
                    fac.AntdCol(
                        welcome_card(
                            title="欢迎访问数据看板",
                            description="实时监控业务数据",
                            icon=fac.AntdAvatar(
                                # 注意：路径需要修正
                                src="assets/images/avatar.png",
                                size=72
                            )
                        ),
                        span=24
                    ),

                    # KPI 指标
                    fac.AntdCol(
                        index_card(
                            index_name="今日访问量",
                            index_value=fuc.FefferyCountUp(
                                id="today-visits",
                                end=12580,
                                duration=1.5
                            ),
                            extra_content=fact.AntdTinyArea(
                                id="today-visits-chart",
                                data=[120, 150, 180, 200],
                                height=60,
                                smooth=True
                            )
                        ),
                        xs=24, md=12, xl=6
                    ),
                    # ... 更多组件
                ],
                gutter=[18, 18]
            )
        ],
        direction="vertical",
        style={"width": "100%"}
    )
```

### 步骤三：迁移静态资源

1. 将原项目 `assets/` 下的资源复制到 Magic-Dash 项目：
   - 图片 → `assets/images/`
   - CSS → `assets/css/`

2. **修正路径引用**：

```python
# 原路径
src="/assets/avatar.png"

# 新路径 (根据实际存放位置)
src="assets/images/avatar.png"
```

### 步骤四：迁移回调函数

在 `callbacks/core_pages_c/` 下新建回调文件（如 `dashboard_c.py`）：

```python
# callbacks/core_pages_c/dashboard_c.py

# ⚠️ 关键：必须从 server 导入 app，不能自己创建
from server import app

from dash import Patch, set_props
from dash.dependencies import Input, Output, State
import datetime
import random


@app.callback(
    [
        Output("update-datetime", "children"),
        Output("today-visits", "children"),
        Output("today-visits-chart", "data"),
    ],
    Input("update-data-interval", "n_intervals"),
    State("today-visits", "children"),
    prevent_initial_call=True,
)
def update_dashboard_data(n_intervals, origin_today_visits):
    """实时更新仪表盘数据"""

    # 1. 更新时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. 数字滚动动画 (FefferyCountUp)
    today_visits_chunk = random.randint(20, 50)
    origin_today_visits["props"]["start"] = origin_today_visits["props"]["end"]
    origin_today_visits["props"]["end"] += today_visits_chunk

    # 3. 图表增量更新 (Patch)
    chart_patch = Patch()
    chart_patch.append(today_visits_chunk)

    return current_time, origin_today_visits, chart_patch
```

### 步骤五：注册回调

在 `callbacks/__init__.py` 中导入新模块：

```python
# callbacks/__init__.py

from .core_pages_c import dashboard_c  # 导入仪表盘回调模块
```

---

## 常见问题排查

### 页面加载但回调不执行

**原因**: 未在 `callbacks/__init__.py` 中导入回调模块

**解决**: 添加 `from .core_pages_c import dashboard_c`

### 图片 404 错误

**原因**: 静态资源路径不正确

**解决**: 检查 `assets/` 文件夹结构和代码中的 `src` 路径是否匹配

### ImportError

**原因**: 遗漏了必要的 import 语句

**解决**: 检查 views 和 callbacks 中的导入

### 回调冲突

**原因**: 多个页面的组件 ID 重复

**解决**: 使用页面前缀确保 ID 唯一，如 `dashboard-chart-1`

---

## 关键规则

### 1. 必须使用框架的 app 实例

```python
# ✅ 正确
from server import app

@app.callback(...)
def my_callback(...):
    pass

# ❌ 错误 - 严禁自己创建 Dash 实例
app = dash.Dash(__name__)
```

### 2. 视图必须定义 render 函数

```python
# views/core_pages/dashboard.py

def render():
    """必须定义此函数作为视图入口"""
    return fac.AntdSpace([...])
```

### 3. 使用 set_props 避免回调冲突

```python
# 多个回调需要控制同一组件时使用 set_props
from dash import set_props

@app.callback(
    Input("export-btn", "nClicks"),
    prevent_initial_call=True
)
def export_data(n):
    set_props("global-download", {
        "data": dcc.send_bytes(file_data, "export.xlsx")
    })
```

### 4. 静态资源路径规范

```python
# 图片资源放在 assets/images/ 下
src="assets/images/logo.png"

# CSS 文件放在 assets/css/ 下
# 会自动加载，无需手动引用
```

---

## 迁移检查清单

- [ ] 在 `router_config.py` 中添加页面路由配置
- [ ] 创建 `views/core_pages/<page>.py` 视图文件
- [ ] 视图文件包含 `def render():` 函数
- [ ] 创建 `callbacks/core_pages_c/<page>_c.py` 回调文件
- [ ] 回调文件使用 `from server import app`
- [ ] 在 `callbacks/__init__.py` 中导入回调模块
- [ ] 静态资源复制到正确目录
- [ ] 检查并修正资源路径引用
- [ ] 检查组件 ID 唯一性

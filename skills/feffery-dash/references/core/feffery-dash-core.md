# feffery-dash-core

> Feffery-Dash 开发核心规范 Skill
> 版本: 1.1 | 更新: 2025-12-19

当用户提到 Dash 项目开发、feffery 组件、回调函数、布局样式时，请参考本 Skill 的规范和模式。

## 触发场景

- 创建新的 Dash 项目
- 使用 feffery 组件库开发
- 编写回调函数 (callback)
- 布局和样式控制
- 项目结构规范

---

## 1. 生态总览

### 1.1 核心组件库

| 库名 | 别名 | 用途 | 官方文档 |
|------|------|------|----------|
| feffery-antd-components | **fac** | Ant Design 风格 UI 组件 | https://fac.feffery.tech/ |
| feffery-utils-components | **fuc** | 工具组件（性能优化/事件监听） | https://fuc.feffery.tech/ |
| feffery-antd-charts | **fact** | 数据可视化图表 | https://fact.feffery.tech/ |
| feffery-leaflet-components | **flc** | Leaflet 地图 | http://flc.feffery.tech/ |
| feffery-maplibre | **fm** | MapLibre/Deck.gl 高性能地图 | - |
| feffery-markdown-components | **fmc** | Markdown 渲染 | http://fmc.feffery.tech/ |
| feffery-antd-mobile-components | **famc** | 移动端 UI 组件（手机/微信） | - |
| feffery-infographic | **fi** | 声明式信息图（59 模板，支持 LLM 流式生成） | https://infographic.antv.vision/ |

### 1.2 工程脚手架

- **magic-dash**: 标准化项目脚手架
  - `simple-tool`: 单页工具应用
  - `magic-dash`: 多页面应用（推荐默认）
  - `magic-dash-pro`: 带登录鉴权的完整后台

### 1.3 Dash 3.x 插件系统

Dash 3.x 引入了基于 hooks 的插件系统，将横切关注点从业务逻辑中剥离：

| 插件名称 | 功能 | 典型场景 |
|----------|------|----------|
| `dash-change-cdn-plugin` | CDN 切换 | 国内访问慢时切换到 npmmirror/jsdelivr |
| `dash-console-filter-plugin` | 控制台过滤 | 屏蔽冗余 React 警告 |
| `dash-performance-monitor-plugin` | 性能监控 | 实时 FPS/内存监控（开发环境） |
| `dash-react-scan-plugin` | 渲染监控 | 组件重绘分析优化 |
| `dash-disable-devtool-plugin` | 安全加固 | 禁用 F12/右键（生产环境） |
| `dash-offline-detect-plugin` | 断线检测 | 后端不可用时前端提示 |
| `dash-vite-plugin` | Vite 构建 | HMR 热更新加速开发 |
| `dash-tailwindcss-plugin` | Tailwind CSS | 实用优先的 CSS 样式 |

### 1.4 浏览器端 API

客户端 JS 中可用（供 `clientside_callback` 使用）：

```javascript
// 获取组件的完整 props 与状态
dash_component_api.getLayout('component-id')

// 将字典 ID 序列化为 DOM ID 字符串
dash_component_api.stringifyId({type: 'btn', index: 0})
// 返回: '{"type":"btn","index":0}'
```

---

## 2. 标准导入模板

```python
# 1. Dash 核心
import dash
from dash import html, dcc

# 2. Feffery 组件库（必须使用指定别名）
import feffery_antd_components as fac
import feffery_utils_components as fuc

# 3. 回调依赖
from dash.dependencies import Input, Output, State, ALL, MATCH, ClientsideFunction
from dash import ctx, Patch, set_props, no_update

# 4. 异常处理
from dash.exceptions import PreventUpdate

# 5. 样式工具（推荐）
from feffery_dash_utils.style_utils import style
```

**重要规则**:
- 必须使用 `fac` 作为 feffery-antd-components 的别名
- 必须使用 `fuc` 作为 feffery-utils-components 的别名
- 优先使用 fac 组件，而非 html 原生标签

---

## 3. 应用实例化

### 3.1 基础实例化

```python
import dash

app = dash.Dash(
    __name__,
    title='应用标题',
    suppress_callback_exceptions=True,  # 动态组件必需
)
server = app.server  # 部署必需
```

### 3.2 启动方式

```python
# ✅ 正确（Dash 3.x）
if __name__ == '__main__':
    app.run(debug=True)

# ❌ 已废弃
# app.run_server()
```

---

## 4. 布局定义

### 4.1 布局模式

```python
# 模式 A：单组件（最常用）
app.layout = html.Div([...])

# 模式 B：函数型布局（动态内容）
app.layout = lambda: html.Div(f"时间: {datetime.now()}")
```

### 4.2 中文配置

```python
app.layout = fac.AntdConfigProvider(
    locale='zh-cn',  # 组件中文化
    children=[
        # 页面内容
    ]
)
```

---

## 5. 回调函数规范

### 5.1 基础结构

```python
@app.callback(
    Output("output-id", "children"),
    Input("input-id", "nClicks"),
    State("state-id", "value"),
    prevent_initial_call=True  # 按钮触发通常需要
)
def callback_function(n_clicks, state_value):
    return f"结果: {n_clicks}"
```

### 5.2 多 Output

```python
@app.callback(
    Output("out1", "children"),
    Output("out2", "children"),
    Input("btn", "nClicks")
)
def multi_output(n):
    return [f"输出1", f"输出2"]  # 必须返回列表
```

### 5.3 ctx 判断触发源

```python
@app.callback(...)
def handle(n1, n2):
    if ctx.triggered_id == "btn1":
        return "按钮1触发"
    elif ctx.triggered_id == "btn2":
        return "按钮2触发"
```

### 5.4 Patch 局部更新

```python
@app.callback(Output("list", "children"), Input("add", "nClicks"))
def add_item(n):
    p = Patch()
    p.append(html.Div(f"新项 {n}"))
    return p
```

### 5.5 set_props 副作用

```python
@app.callback(Output("result", "children"), Input("btn", "nClicks"))
def submit(n):
    # 主逻辑
    result = process()
    # 副作用：弹出消息
    set_props("msg", {"children": fac.AntdMessage(content="成功", type="success")})
    return result
```

### 5.6 动态组件处理

```python
# 对于动态布局中"尚未渲染"的组件 ID
@app.callback(
    Output('dynamic-output', 'children'),
    Input('dynamic-input', 'value'),
    allow_optional=True  # 组件可能不存在
)
def handle_dynamic(value):
    if value is None:  # 组件不存在时为 None
        return no_update
    return process(value)
```

---

## 6. 模式匹配回调

### 6.1 ALL 模式（批量收集）

```python
# 布局
[fac.AntdButton(f"btn{i}", id={"type": "btn", "index": i}) for i in range(10)]

# 回调
@app.callback(
    Output("out", "children"),
    Input({"type": "btn", "index": ALL}, "nClicks")
)
def sum_all(n_list):
    return sum(n for n in n_list if n)
```

### 6.2 MATCH 模式（一对一）

```python
@app.callback(
    Output({"type": "out", "index": MATCH}, "children"),
    Input({"type": "btn", "index": MATCH}, "nClicks")
)
def update_single(n):
    return f"点击 {n} 次"
```

---

## 7. 项目结构规范

### 7.1 推荐结构

```
project/
├── server.py           # 实例化 app，暴露 server
├── app.py              # 组装 layout，导入回调
├── config.py           # 配置参数
├── wsgi.py             # 生产部署入口
├── assets/             # 静态资源（自动加载）
│   ├── base.css
│   └── callbacks.js
├── views/              # 视图模块
│   └── page1.py
├── callbacks/          # 回调模块
│   └── page1_c.py
└── models/             # 数据库模型
```

### 7.2 关键文件

**server.py**
```python
import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
```

**callbacks/page1_c.py**
```python
from server import app  # 从 server 导入，避免循环引用

@app.callback(...)
def callback_func(...):
    pass
```

---

## 8. 常用组件速查

### 8.1 布局组件

| 组件 | 用途 |
|------|------|
| `fac.AntdRow` / `fac.AntdCol` | 24栅格系统 |
| `fac.AntdSpace` | 间距排列 |
| `fac.AntdCenter` | 居中容器 |
| `fac.AntdLayout` | 页面骨架 |

### 8.2 表单组件

| 组件 | 用途 |
|------|------|
| `fac.AntdForm` | 表单容器 |
| `fac.AntdInput` | 输入框 |
| `fac.AntdSelect` | 下拉选择 |
| `fac.AntdDatePicker` | 日期选择 |

### 8.3 展示组件

| 组件 | 用途 |
|------|------|
| `fac.AntdTable` | 数据表格 |
| `fac.AntdCard` | 卡片容器 |
| `fac.AntdTabs` | 标签页 |
| `fac.AntdModal` | 模态框 |

### 8.4 反馈组件

| 组件 | 用途 |
|------|------|
| `fac.AntdMessage` | 全局消息 |
| `fac.AntdNotification` | 通知提醒 |
| `fac.AntdSpin` | 加载状态 |
| `fac.AntdAlert` | 警告提示 |

---

## 9. 样式规范

### 9.1 style 参数

```python
html.Div(
    "内容",
    style={
        "backgroundColor": "#f0f0f0",  # CSS 属性转小驼峰
        "fontSize": 16,                 # 数字默认 px
        "padding": "10px 20px",
    }
)
```

### 9.2 推荐使用 style 工具

```python
from feffery_dash_utils.style_utils import style

html.Div("内容", style=style(backgroundColor="#f0f0f0", padding=20))
```

---

## 10. 部署

### Windows (Waitress)

```python
from waitress import serve
from app import server
serve(server, host='0.0.0.0', port=8050, threads=8)
```

### Linux (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:8050 app:server
```

---

## 相关文档

- 项目规范详情: `project_standards.md`
- 回调模式大全: `callback_patterns.md`
- 布局指南: `layout_guide.md`
- 最佳实践: `best_practices.md`
- 插件系统详情: `plugins.md`


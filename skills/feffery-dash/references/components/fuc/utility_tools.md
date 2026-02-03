# FUC 实用工具组件

> feffery-utils-components 实用工具类组件详解
> 存储、截图、全屏、倒计时、响应式等实用功能

---

## 工具组件概览

### 存储类

| 组件 | 说明 | 数据持久性 |
|------|------|------------|
| FefferyCookie | Cookie 存储 | 可设过期时间 |
| FefferyLocalStorage | 本地存储 | 永久（手动清除） |
| FefferySessionStorage | 会话存储 | 关闭页面清除 |
| FefferyLocalLargeStorage | 大容量存储 | 基于 IndexedDB |

### 截图导出类

| 组件 | 说明 | 输出格式 |
|------|------|----------|
| FefferyDom2Image | DOM 转图片 | base64 dataUrl |

### 交互增强类

| 组件 | 说明 |
|------|------|
| FefferyFullscreen | 全屏控制 |
| FefferyCountUp | 数字递增动画 |
| FefferyCountDown | 倒计时 |
| FefferyScrollbars | 自定义滚动条 |

### 监听工具类

| 组件 | 说明 |
|------|------|
| FefferyResponsive | 响应式断点检测 |
| FefferyKeyPress | 按键监听 |
| FefferyWindowSize | 窗口尺寸监听 |

### 页面工具类

| 组件 | 说明 |
|------|------|
| FefferySetTitle | 动态设置标题 |
| FefferySetFavicon | 动态设置图标 |

---

## Cookie 存储 FefferyCookie

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| cookieKey | string | **必填** | 要绑定的 cookie 键名 |
| defaultValue | string | - | 缺省时的默认值（不覆盖已有值） |
| value | string | - | 用于更新当前绑定的 cookie 值 |
| expires | number | - | 有效存储时间，单位：秒 |
| pathname | string | '/' | cookie 可用的路径 |
| secure | boolean | False | 是否仅允许 https 传输 |

### 基础用法

```python
import feffery_utils_components as fuc
import feffery_antd_components as fac
from dash import Dash, html, Input, Output, State

app = Dash(__name__)

app.layout = html.Div([
    fuc.FefferyCookie(
        id='my-cookie',
        cookieKey='user-preference',
        defaultValue='default'
    ),
    fac.AntdInput(id='cookie-input', placeholder='输入要保存的内容'),
    fac.AntdButton('保存到 Cookie', id='save-btn', type='primary'),
    html.Div(id='cookie-output')
])

# 保存 Cookie
@app.callback(
    Output('my-cookie', 'value'),
    Input('save-btn', 'nClicks'),
    State('cookie-input', 'value'),
    prevent_initial_call=True
)
def save_cookie(n, value):
    return value

# 读取 Cookie（在服务端）
from flask import request
@app.callback(
    Output('cookie-output', 'children'),
    Input('my-cookie', 'value')
)
def read_cookie(value):
    server_value = request.cookies.get('user-preference')
    return f'Cookie 值: {server_value}'
```

---

## LocalStorage 存储 FefferyLocalStorage

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | **必填** | 组件 id，同时作为 localStorage 的 key |
| data | any | - | 存储的数据，支持布尔/数字/字符串/字典/列表 |
| initialSync | boolean | False | 初始化时是否从 localStorage 同步数据 |

### 基础用法

```python
fuc.FefferyLocalStorage(
    id='local-storage-demo',
    initialSync=True  # 初始化时从 localStorage 读取已存储的数据
)

# 写入
@app.callback(
    Output('local-storage-demo', 'data'),
    Input('save-btn', 'nClicks'),
    State('form-data', 'value'),
    prevent_initial_call=True
)
def save_local(n, data):
    return data  # 可以是任意类型：字符串、数字、字典、列表

# 读取
@app.callback(
    Output('form-data', 'value'),
    Input('local-storage-demo', 'data')
)
def load_local(data):
    return data or ''
```

### 存储复杂数据

```python
@app.callback(
    Output('local-storage-demo', 'data'),
    Input('save-settings', 'nClicks'),
    prevent_initial_call=True
)
def save_settings(n):
    return {
        'username': 'admin',
        'settings': {
            'theme': 'dark',
            'language': 'zh-CN'
        },
        'lastLogin': '2024-01-01'
    }
```

---

## SessionStorage 存储 FefferySessionStorage

与 LocalStorage 用法相同，区别是数据仅在当前会话有效，关闭页面后清除。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | **必填** | 组件 id，同时作为 sessionStorage 的 key |
| data | any | - | 存储的数据 |
| initialSync | boolean | False | 初始化时是否同步数据 |

### 使用场景

```python
# 适合存储临时会话数据
fuc.FefferySessionStorage(
    id='temp-form-data',
    initialSync=True
)
```

---

## DOM 转图片 FefferyDom2Image

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| targetSelector | string | - | 目标元素 CSS 选择器 |
| scale | number | 1 | 精度缩放比例 |
| screenshotResult | dict | - | 截图结果数据 |

### screenshotResult 结构

| 属性 | 类型 | 说明 |
|------|------|------|
| selector | string | 本次转换的选择器 |
| status | string | 执行状态：'success' 或 'failed' |
| dataUrl | string | 转换后的图片 dataUrl（base64） |
| timestamp | number | 任务完成时间戳 |

### 基础用法

```python
html.Div([
    html.Div(
        id='screenshot-target',
        children=[
            html.H1('这是要截图的内容'),
            html.P('支持任意 DOM 元素')
        ],
        style={'padding': 20, 'background': '#f0f0f0'}
    ),
    fac.AntdButton('截图', id='screenshot-btn', type='primary'),
    fuc.FefferyDom2Image(id='dom2image', scale=2),
    html.Img(id='screenshot-preview', style={'maxWidth': '100%', 'marginTop': 16})
])

# 触发截图
@app.callback(
    Output('dom2image', 'targetSelector'),
    Input('screenshot-btn', 'nClicks'),
    prevent_initial_call=True
)
def trigger_screenshot(n):
    return '#screenshot-target'

# 显示截图结果
@app.callback(
    Output('screenshot-preview', 'src'),
    Input('dom2image', 'screenshotResult'),
    prevent_initial_call=True
)
def show_screenshot(result):
    if result and result['status'] == 'success':
        return result['dataUrl']
    return ''
```

---

## 全屏控制 FefferyFullscreen

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| targetId | string | - | 要全屏的目标元素 id，缺省时全屏整个页面 |
| isFullscreen | boolean | False | 设置/监听全屏状态 |
| pageFullscreen | boolean/dict | False | 配置页面全屏模式 |

### 基础用法

```python
html.Div([
    fuc.FefferyFullscreen(id='fullscreen-control', targetId='chart-container'),
    fac.AntdButton('切换全屏', id='fullscreen-btn', type='primary'),
    html.Div(
        id='chart-container',
        children=[...],  # 图表内容
        style={'height': 400, 'background': '#f5f5f5'}
    )
])

@app.callback(
    Output('fullscreen-control', 'isFullscreen'),
    Output('fullscreen-btn', 'children'),
    Input('fullscreen-btn', 'nClicks'),
    State('fullscreen-control', 'isFullscreen'),
    prevent_initial_call=True
)
def toggle_fullscreen(n, current):
    new_state = not current
    return new_state, '退出全屏' if new_state else '全屏'
```

### 页面全屏模式

```python
fuc.FefferyFullscreen(
    id='page-fullscreen',
    targetId='dashboard',
    pageFullscreen={
        'className': 'custom-fullscreen',
        'zIndex': 9999
    }
)
```

---

## 数字递增动画 FefferyCountUp

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| end | number | **必填** | 目标值 |
| start | number | 0 | 起始值 |
| duration | number | 2 | 动画时长（秒） |
| decimals | number | 0 | 小数精度 |
| separator | string | ',' | 千分符 |
| enableScrollSpy | boolean | True | 进入视口后才开始动画 |
| scrollSpyDelay | number | 0 | 进入视口后延迟执行（毫秒） |
| scrollSpyOnce | boolean | True | 仅执行一次 |

### 基础用法

```python
fac.AntdSpace([
    fuc.FefferyCountUp(
        end=12345,
        duration=2.5,
        decimals=0,
        separator=','
    ),
    fuc.FefferyCountUp(
        end=99.99,
        duration=3,
        decimals=2,
        separator=','
    )
], style={'fontSize': 24})
```

### 动态更新

```python
fuc.FefferyCountUp(id='count-up', end=0)

@app.callback(
    Output('count-up', 'end'),
    Input('refresh-btn', 'nClicks')
)
def update_count(n):
    return fetch_latest_value()  # 每次更新 end 都会触发动画
```

---

## 倒计时 FefferyCountDown

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| delay | number | - | 倒计时总时长（秒），设置后自动开始 |
| interval | number | 1 | 时间间隔（秒） |
| countdown | number | - | 监听当前剩余时间（秒） |

### 基础用法

```python
fac.AntdSpace([
    fac.AntdButton('开始10秒倒计时', id='start-countdown', type='primary'),
    fac.AntdText(id='countdown-display'),
    fuc.FefferyCountDown(id='countdown')
], direction='vertical')

@app.callback(
    Output('countdown', 'delay'),
    Input('start-countdown', 'nClicks'),
    prevent_initial_call=True
)
def start_countdown(n):
    return 10  # 设置 delay 即开始倒计时

@app.callback(
    Output('countdown-display', 'children'),
    Input('countdown', 'countdown'),
    prevent_initial_call=True
)
def show_countdown(countdown):
    if countdown == 0:
        return '倒计时结束！'
    return f'剩余 {countdown} 秒'
```

### 按钮禁用场景

```python
# 验证码发送按钮冷却
fac.AntdButton(
    id='send-code-btn',
    children='发送验证码',
    disabled=False
)
fuc.FefferyCountDown(id='code-countdown')

@app.callback(
    Output('code-countdown', 'delay'),
    Output('send-code-btn', 'disabled'),
    Input('send-code-btn', 'nClicks'),
    prevent_initial_call=True
)
def send_code(n):
    # 发送验证码逻辑...
    return 60, True  # 60秒冷却

@app.callback(
    Output('send-code-btn', 'children'),
    Output('send-code-btn', 'disabled', allow_duplicate=True),
    Input('code-countdown', 'countdown'),
    prevent_initial_call=True
)
def update_btn(countdown):
    if countdown == 0:
        return '发送验证码', False
    return f'重新发送({countdown}s)', True
```

---

## 响应式检测 FefferyResponsive

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| responsive | dict | - | 监听当前页面各断点满足情况 |

### 基础用法

```python
fuc.FefferyResponsive(id='responsive')

@app.callback(
    Output('layout', 'children'),
    Input('responsive', 'responsive')
)
def responsive_layout(responsive):
    if responsive:
        # responsive 包含各断点状态：xs, sm, md, lg, xl, xxl
        if responsive.get('xs') or responsive.get('sm'):
            return mobile_layout()
    return desktop_layout()
```

---

## 按键监听 FefferyKeyPress

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| keys | string | **必填** | 监听的按键组合 |
| pressedCounts | number | 0 | 按键触发次数 |

### 基础用法

```python
# 监听 Ctrl+S 保存快捷键
fuc.FefferyKeyPress(id='save-shortcut', keys='ctrl.s')

@app.callback(
    Output('message', 'children'),
    Input('save-shortcut', 'pressedCounts'),
    prevent_initial_call=True
)
def handle_save(n):
    # 执行保存操作
    save_data()
    return fac.AntdMessage(content='已保存', type='success')
```

### 监听多个快捷键

```python
html.Div([
    fuc.FefferyKeyPress(id='shortcut-save', keys='ctrl.s'),
    fuc.FefferyKeyPress(id='shortcut-undo', keys='ctrl.z'),
    fuc.FefferyKeyPress(id='shortcut-redo', keys='ctrl.shift.z'),
])
```

---

## 设置页面标题 FefferySetTitle

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| title | string | - | 要设置的页面标题 |

### 基础用法

```python
fuc.FefferySetTitle(id='page-title')

@app.callback(
    Output('page-title', 'title'),
    Input('url', 'pathname')
)
def update_title(pathname):
    titles = {
        '/': '首页 - 我的应用',
        '/dashboard': '仪表盘 - 我的应用',
        '/settings': '设置 - 我的应用'
    }
    return titles.get(pathname, '我的应用')
```

### 显示未读消息数

```python
@app.callback(
    Output('page-title', 'title'),
    Input('unread-count', 'data')
)
def show_unread(count):
    if count > 0:
        return f'({count}) 新消息 - 我的应用'
    return '我的应用'
```

---

## 设置页面图标 FefferySetFavicon

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| favicon | string | - | 图标 URL |

### 基础用法

```python
fuc.FefferySetFavicon(id='page-favicon', favicon='/assets/favicon.ico')

# 动态切换图标（如未读消息提醒）
@app.callback(
    Output('page-favicon', 'favicon'),
    Input('notification-count', 'data')
)
def update_favicon(count):
    if count > 0:
        return '/assets/favicon-notification.ico'
    return '/assets/favicon.ico'
```

---

## 自定义滚动条 FefferyScrollbars

### 基础用法

```python
fuc.FefferyScrollbars(
    html.Div([...], style={'height': 2000}),  # 长内容
    style={'height': 400},
    autoHide=True,           # 自动隐藏
    autoHideTimeout=1000,    # 隐藏延迟
    thumbMinSize=30          # 滚动条最小尺寸
)
```

---

## 参考资源

- [feffery-utils-components 官方文档](https://fuc.feffery.tech/)

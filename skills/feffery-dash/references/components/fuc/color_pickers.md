# FUC 颜色选择器组件

> feffery-utils-components 颜色选择相关组件详解
> 多种风格的颜色选择器和屏幕取色工具

---

## 颜色组件概览

| 组件 | 说明 | 输出格式 | 适用场景 |
|------|------|----------|----------|
| FefferyHexColorPicker | 16进制颜色选择器 | `#rrggbb` | CSS颜色设置 |
| FefferyRgbColorPicker | RGB颜色选择器 | `rgb(r,g,b)` | 需要RGB格式 |
| FefferyBlockColorPicker | Block风格选择器 | `#rrggbb` | 预设颜色快选 |
| FefferyCircleColorPicker | Circle风格选择器 | `#rrggbb` | 美观的圆形色块 |
| FefferyGithubColorPicker | Github风格选择器 | `#rrggbb` | 简洁标签配色 |
| FefferyTwitterColorPicker | Twitter风格选择器 | `#rrggbb` | 社交风格配色 |
| FefferyWheelColorPicker | 色轮选择器 | `#rrggbb` | 专业艺术配色 |
| FefferyEyeDropper | 屏幕取色器 | `#rrggbb` | 从屏幕取色 |

---

## HEX 颜色选择器 FefferyHexColorPicker

输出十六进制格式颜色值。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| color | string | '#44cef6' | 监听/设置当前选中的16进制颜色值 |
| showAlpha | boolean | False | 是否显示透明度选择控件 |

### 基础用法

```python
import feffery_utils_components as fuc
from dash import Dash, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    fuc.FefferyHexColorPicker(
        id='hex-picker',
        color='#1890ff',
        showAlpha=True
    ),
    html.Div(id='color-output')
])

@app.callback(
    Output('color-output', 'children'),
    Output('color-output', 'style'),
    Input('hex-picker', 'color')
)
def show_color(color):
    return f'HEX: {color}', {'backgroundColor': color, 'padding': 10, 'color': 'white'}
```

---

## RGB 颜色选择器 FefferyRgbColorPicker

输出 RGB 格式颜色值。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| color | string | 'rgb(68, 206, 246)' | 监听/设置当前选中的RGB格式颜色值 |
| showAlpha | boolean | False | 是否显示透明度选择控件 |

### 基础用法

```python
fuc.FefferyRgbColorPicker(
    id='rgb-picker',
    color='rgb(24, 144, 255)',
    showAlpha=True  # 启用后输出 rgba(r, g, b, a) 格式
)

@app.callback(
    Output('preview', 'style'),
    Input('rgb-picker', 'color')
)
def apply_color(color):
    # color 格式: 'rgb(r, g, b)' 或 'rgba(r, g, b, a)'
    return {'backgroundColor': color, 'width': 100, 'height': 100}
```

---

## Block 风格选择器 FefferyBlockColorPicker

块状预设颜色选择器。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| width | string | '170px' | 整体宽度 |
| color | string | - | 监听/设置当前选中的16进制颜色值 |
| colors | list | - | 自定义可选颜色数组（16进制） |
| triangle | string | 'top' | 顶部箭头方位: 'hide', 'top' |

### 基础用法

```python
fuc.FefferyBlockColorPicker(
    id='block-picker',
    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
    triangle='top'
)

@app.callback(
    Output('tag-color', 'style'),
    Input('block-picker', 'color')
)
def update_tag(color):
    return {'backgroundColor': color}
```

---

## Circle 风格选择器 FefferyCircleColorPicker

圆形色块选择器。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| width | string | '252px' | 整体宽度 |
| circleSize | number | 28 | 圆圈像素大小 |
| circleSpacing | number | 14 | 圆圈之间的像素间隔 |
| color | string | - | 监听/设置当前选中的16进制颜色值 |
| colors | list | - | 自定义可选颜色数组（16进制） |

### 基础用法

```python
fuc.FefferyCircleColorPicker(
    id='circle-picker',
    circleSize=32,
    circleSpacing=16,
    colors=['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2']
)
```

---

## Github 风格选择器 FefferyGithubColorPicker

Github 标签风格颜色选择器。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| color | string | - | 监听/设置当前选中的16进制颜色值 |
| colors | list | - | 自定义可选颜色数组（16进制） |
| triangle | string | 'top-left' | 箭头方位: 'hide', 'top-left', 'top-right' |

### 基础用法

```python
fuc.FefferyGithubColorPicker(
    id='github-picker',
    triangle='top-right',
    colors=['#b60205', '#d93f0b', '#fbca04', '#0e8a16', '#1d76db', '#5319e7']
)
```

---

## Twitter 风格选择器 FefferyTwitterColorPicker

Twitter 风格颜色选择器。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| color | string | - | 监听/设置当前选中的16进制颜色值 |
| colors | list | - | 自定义可选颜色数组（16进制） |
| triangle | string | 'top-left' | 箭头方位: 'hide', 'top-left', 'top-right' |

### 基础用法

```python
fuc.FefferyTwitterColorPicker(
    id='twitter-picker',
    triangle='hide'
)
```

---

## 色轮选择器 FefferyWheelColorPicker

专业级色轮颜色选择器。

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| color | string | - | 监听/设置当前选中的16进制颜色值 |

### 基础用法

```python
fuc.FefferyWheelColorPicker(
    id='wheel-picker'
)

@app.callback(
    Output('design-preview', 'style'),
    Input('wheel-picker', 'color')
)
def update_design(color):
    return {'backgroundColor': color}
```

---

## 屏幕取色器 FefferyEyeDropper

从屏幕任意位置拾取颜色。

> 注意：需要浏览器支持 EyeDropper API（Chrome 95+）

### 参数说明

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一id |
| key | string | - | 强制重绘组件 |
| enable | boolean | False | 控制激活取色，完成后自动重置为 False |
| color | string | - | 监听最近一次取色结果（16进制） |

### 基础用法

```python
import feffery_antd_components as fac

html.Div([
    fac.AntdButton('开始取色', id='start-pick', type='primary'),
    fuc.FefferyEyeDropper(id='eye-dropper'),
    html.Div(id='picked-color'),
    html.Div(id='color-preview', style={'width': 50, 'height': 50, 'marginTop': 10})
])

@app.callback(
    Output('eye-dropper', 'enable'),
    Input('start-pick', 'nClicks'),
    prevent_initial_call=True
)
def start_picking(n):
    return True

@app.callback(
    Output('picked-color', 'children'),
    Output('color-preview', 'style'),
    Input('eye-dropper', 'color'),
    prevent_initial_call=True
)
def show_picked_color(color):
    if color:
        return f'拾取颜色: {color}', {'backgroundColor': color, 'width': 50, 'height': 50}
    return '请点击取色按钮', {}
```

---

## 实际应用场景

### 1. 主题颜色配置面板

```python
import feffery_antd_components as fac

fac.AntdCard(
    [
        fac.AntdForm([
            fac.AntdFormItem(
                fuc.FefferyHexColorPicker(id='primary-color', color='#1890ff'),
                label='主色'
            ),
            fac.AntdFormItem(
                fuc.FefferyHexColorPicker(id='success-color', color='#52c41a'),
                label='成功色'
            ),
            fac.AntdFormItem(
                fuc.FefferyHexColorPicker(id='warning-color', color='#faad14'),
                label='警告色'
            ),
            fac.AntdFormItem(
                fuc.FefferyHexColorPicker(id='error-color', color='#ff4d4f'),
                label='错误色'
            ),
        ])
    ],
    title='主题配置'
)
```

### 2. 颜色选择器 + 取色器组合

```python
fac.AntdSpace([
    fuc.FefferyHexColorPicker(id='color-picker', color='#1890ff'),
    fac.AntdButton('从屏幕取色', id='pick-btn', size='small'),
    fuc.FefferyEyeDropper(id='eye-dropper')
])

# 取色后更新颜色选择器
@app.callback(
    Output('color-picker', 'color'),
    Input('eye-dropper', 'color'),
    prevent_initial_call=True
)
def update_from_dropper(color):
    return color

@app.callback(
    Output('eye-dropper', 'enable'),
    Input('pick-btn', 'nClicks'),
    prevent_initial_call=True
)
def enable_dropper(n):
    return True
```

### 3. 渐变色配置

```python
html.Div([
    fac.AntdSpace([
        fuc.FefferyHexColorPicker(id='gradient-start', color='#1890ff'),
        fac.AntdIcon(icon='antd-arrow-right'),
        fuc.FefferyHexColorPicker(id='gradient-end', color='#722ed1'),
    ]),
    html.Div(id='gradient-preview', style={'width': '100%', 'height': 50, 'marginTop': 16})
])

@app.callback(
    Output('gradient-preview', 'style'),
    Input('gradient-start', 'color'),
    Input('gradient-end', 'color')
)
def update_gradient(start, end):
    return {
        'width': '100%',
        'height': 50,
        'marginTop': 16,
        'background': f'linear-gradient(90deg, {start}, {end})',
        'borderRadius': 4
    }
```

### 4. 标签颜色快速选择

```python
fac.AntdSpace([
    fuc.FefferyGithubColorPicker(
        id='tag-color-picker',
        colors=['#b60205', '#d93f0b', '#fbca04', '#0e8a16', '#1d76db', '#5319e7']
    ),
    fac.AntdTag(id='preview-tag', children='标签预览')
])

@app.callback(
    Output('preview-tag', 'color'),
    Input('tag-color-picker', 'color')
)
def update_tag_color(color):
    return color
```

---

## Python 颜色工具函数

```python
def hex_to_rgb(hex_color):
    """HEX 转 RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    """RGB 转 HEX"""
    return f'#{r:02x}{g:02x}{b:02x}'

def adjust_brightness(hex_color, factor):
    """调整亮度 (factor > 1 变亮, < 1 变暗)"""
    r, g, b = hex_to_rgb(hex_color)
    r = min(255, max(0, int(r * factor)))
    g = min(255, max(0, int(g * factor)))
    b = min(255, max(0, int(b * factor)))
    return rgb_to_hex(r, g, b)
```

---

## 参考资源

- [feffery-utils-components 官方文档](https://fuc.feffery.tech/)

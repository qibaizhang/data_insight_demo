# FUC 背景动效组件

> feffery-utils-components 背景动效类组件详解
> 丰富的 WebGL 和 Canvas 动态背景效果

---

## 背景动效概览

fuc 提供了基于 vanta.js 的多种 3D 背景动效组件：

| 组件 | 效果 | 适用场景 |
|------|------|----------|
| FefferyBirdsBackground | 飞鸟动画 | 活泼风格页面 |
| FefferyCloudsBackground | 云朵流动 | 柔和自然风格 |
| FefferyCloudsTwoBackground | 云朵变体 | 梦幻风格 |
| FefferyWavesBackground | 波浪动画 | 科技海洋风格 |
| FefferyNetBackground | 网络连线 | 科技感页面 |
| FefferyGlobeBackground | 地球仪 | 全球化主题 |
| FefferyFogBackground | 雾气效果 | 神秘朦胧风格 |
| FefferyHaloBackground | 光环效果 | 未来科技风格 |
| FefferyRingsBackground | 圆环动画 | 抽象艺术风格 |
| FefferyTopologyBackground | 拓扑网络 | 数据网络主题 |
| FefferyCellsBackground | 细胞效果 | 生物科技风格 |
| FefferyTrunkBackground | 树干效果 | 自然生长风格 |

---

## 通用参数

所有背景组件都支持以下通用参数：

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| id | string | - | 组件唯一 id |
| key | string | - | 更新可强制重绘组件 |
| children | component | - | 内嵌元素内容 |
| style | dict | - | CSS 样式 |
| className | string/dict | - | CSS 类名 |
| mouseControls | bool | True | 是否开启鼠标控制 |
| touchControls | bool | True | 是否开启触摸控制 |
| gyroControls | bool | False | 是否开启陀螺仪控制 |
| minHeight | number | 200 | 最小高度 |
| minWidth | number | 200 | 最小宽度 |
| scale | number | 1.0 | 缩放比例 |
| scaleMobile | number | 1.0 | 移动端缩放比例 |

---

## 飞鸟背景 FefferyBirdsBackground

```python
import feffery_utils_components as fuc
from dash import html

fuc.FefferyBirdsBackground(
    html.Div(
        [
            html.H1('欢迎', style={'color': 'white'}),
            html.P('探索新世界', style={'color': 'white'})
        ],
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'height': '100%'
        }
    ),
    backgroundColor='#000000',     # 背景色
    backgroundAlpha=1,             # 背景透明度 0-1
    color1='#ff0000',              # 鸟群颜色1
    color2='#13becf',              # 鸟群颜色2
    colorMode='varianceGradient',  # 颜色模式: 'lerp'|'variance'|'lerpGradient'|'varianceGradient'
    birdSize=1,                    # 鸟的大小 1-4
    wingSpan=30,                   # 翼展 10-40
    speedLimit=5,                  # 速度限制 1-10
    separation=20,                 # 分离度 1-100
    alignment=20,                  # 对齐度 1-100
    cohesion=20,                   # 聚合度 1-100
    quantity=5,                    # 数量等级 1-5
    style={'height': '100vh', 'width': '100%'}
)
```

---

## 波浪背景 FefferyWavesBackground

```python
fuc.FefferyWavesBackground(
    html.Div([...]),
    color='#11619a',       # 波浪颜色
    shininess=30,          # 光泽度 0-150
    waveHeight=15,         # 波浪高度 0-40
    waveSpeed=1,           # 波浪速度 0-2
    zoom=1,                # 缩放 0.7-1.8
    style={'height': '400px'}
)
```

---

## 网格背景 FefferyNetBackground

```python
fuc.FefferyNetBackground(
    html.Div([...]),
    color='#ff3f81',           # 线条颜色
    backgroundColor='#23153c', # 背景颜色
    points=10,                 # 点的数量 1-20
    maxDistance=20,            # 最大连接距离 10-40
    spacing=15,                # 点的间距 10-20
    showDots=True,             # 显示点
    style={'height': '100vh'}
)
```

---

## 地球背景 FefferyGlobeBackground

```python
fuc.FefferyGlobeBackground(
    html.Div([...]),
    color='#3f51b5',            # 主颜色
    color2='#1e3a8a',           # 辅助颜色
    backgroundColor='#0f0f23',  # 背景色
    style={'height': '500px'}
)
```

---

## 云朵背景 FefferyCloudsBackground

```python
fuc.FefferyCloudsBackground(
    html.Div([...]),
    backgroundColor='#1a1a2e',
    skyColor='#68b8d7',         # 天空颜色
    cloudColor='#adc1de',       # 云朵颜色
    cloudShadowColor='#183550', # 云影颜色
    sunColor='#ff9919',         # 太阳颜色
    sunGlareColor='#ff6633',    # 太阳光晕颜色
    sunlightColor='#ff9933',    # 阳光颜色
    speed=1.0,                  # 移动速度
    style={'height': '400px'}
)
```

---

## 雾气背景 FefferyFogBackground

```python
fuc.FefferyFogBackground(
    html.Div([...]),
    highlightColor='#ffc300',  # 高光颜色
    midtoneColor='#ff1f00',    # 中间调颜色
    lowlightColor='#2d00ff',   # 低光颜色
    baseColor='#ffebeb',       # 基础颜色
    blurFactor=0.6,            # 模糊系数
    zoom=1.0,                  # 缩放
    speed=1.0,                 # 速度
    style={'height': '400px'}
)
```

---

## 光环背景 FefferyHaloBackground

```python
fuc.FefferyHaloBackground(
    html.Div([...]),
    backgroundColor='#000000',
    baseColor='#1e90ff',   # 基础颜色
    size=1.0,              # 光环大小
    amplitudeFactor=1.0,   # 振幅系数
    xOffset=0,             # X偏移
    yOffset=0,             # Y偏移
    style={'height': '100vh'}
)
```

---

## 圆环背景 FefferyRingsBackground

```python
fuc.FefferyRingsBackground(
    html.Div([...]),
    backgroundColor='#202428',
    color='#ff3f81',       # 圆环颜色
    style={'height': '500px'}
)
```

---

## 拓扑背景 FefferyTopologyBackground

```python
fuc.FefferyTopologyBackground(
    html.Div([...]),
    backgroundColor='#001122',
    color='#00d4ff',       # 线条颜色
    style={'height': '100vh'}
)
```

---

## 细胞背景 FefferyCellsBackground

```python
fuc.FefferyCellsBackground(
    html.Div([...]),
    backgroundColor='#1a1a2e',
    color1='#3f51b5',      # 颜色1
    color2='#1e88e5',      # 颜色2
    size=1.5,              # 细胞大小
    speed=1.0,             # 移动速度
    style={'height': '400px'}
)
```

---

## 使用技巧

### 1. 全屏背景

```python
app.layout = fuc.FefferyWavesBackground(
    html.Div(
        [
            # 页面内容
            html.Div([...], style={'position': 'relative', 'zIndex': 1})
        ]
    ),
    style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100vw',
        'height': '100vh'
    }
)
```

### 2. 局部背景（卡片内）

```python
import feffery_antd_components as fac

fac.AntdCard(
    fuc.FefferyNetBackground(
        html.Div(
            fac.AntdStatistic(title='访问量', value=12345),
            style={'padding': 24}
        ),
        style={'height': 200, 'borderRadius': 8, 'overflow': 'hidden'}
    ),
    bordered=False,
    bodyStyle={'padding': 0}
)
```

### 3. 登录页背景

```python
fuc.FefferyFogBackground(
    fac.AntdCenter(
        fac.AntdCard(
            [
                fac.AntdForm([
                    fac.AntdFormItem(
                        fac.AntdInput(placeholder='用户名'),
                        label='用户名'
                    ),
                    fac.AntdFormItem(
                        fac.AntdInput(mode='password', placeholder='密码'),
                        label='密码'
                    ),
                    fac.AntdFormItem(
                        fac.AntdButton('登录', type='primary', block=True)
                    )
                ])
            ],
            title='系统登录',
            style={'width': 400}
        ),
        style={'height': '100%'}
    ),
    style={'height': '100vh'}
)
```

### 4. 性能优化

```python
# 移动端降低性能消耗
fuc.FefferyBirdsBackground(
    [...],
    quantity=2,        # 减少数量
    scaleMobile=0.5,   # 移动端缩小
    gyroControls=False # 关闭陀螺仪
)
```

---

## 参考资源

- [feffery-utils-components 官方文档](https://fuc.feffery.tech/)

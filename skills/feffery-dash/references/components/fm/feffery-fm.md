# feffery-fm

> feffery-maplibre MapLibre GL + Deck.gl 高性能地图组件库 Skill
> 组件数量: 32 | 版本: 0.1.0-rc3

当用户需要高性能 WebGL 地图、3D 可视化或 Deck.gl 图层时使用 fm 组件。

---

## 快速开始

```python
import dash
from dash import html
import feffery_maplibre as fm

app = dash.Dash(__name__)

app.layout = html.Div([
    fm.MapContainer(
        initialViewState={
            'longitude': 116.4,
            'latitude': 39.9,
            'zoom': 10
        },
        mapStyle='https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY',
        style={'height': '100vh'}
    )
])
```

---

## 组件分类速查

### 核心组件 (5个)

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `MapContainer` | 地图容器 | `initialViewState`, `mapStyle` |
| `Source` | 数据源 | `sourceProps` |
| `Layer` | 图层 | `layerProps` |
| `Marker` | 标记点 | `longitude`, `latitude` |
| `Popup` | 弹窗 | `longitude`, `latitude` |

### 控制组件 (5个)

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `NavigationControl` | 导航控件 | 缩放+指南针 |
| `ScaleControl` | 比例尺 | `maxWidth`, `unit` |
| `FullscreenControl` | 全屏控件 | 全屏切换 |
| `GeolocateControl` | 定位控件 | 用户定位 |
| `AttributionControl` | 署名控件 | 数据来源 |

### 动作组件 (12个)

| 组件 | 用途 | 关键参数 |
|------|------|----------|
| `EaseTo` | 平滑过渡 | `center`, `zoom`, `duration` |
| `FlyTo` | 飞行动画 | `center`, `zoom`, `duration` |
| `FitBounds` | 适配边界 | `bounds`, `padding` |
| `JumpTo` | 快速跳转 | `center`, `zoom` |
| `PanBy` | 相对平移 | `offset` |
| `PanTo` | 绝对平移 | `lngLat` |
| `ZoomIn` | 放大 | - |
| `ZoomOut` | 缩小 | - |
| `ZoomTo` | 缩放至 | `zoom` |
| `RotateTo` | 旋转至 | `bearing` |
| `Resize` | 尺寸重算 | - |
| `Stop` | 停止动画 | - |

### Deck.gl 高性能图层 (4个)

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `ArcLayer` | 弧线图层 | 起点终点弧线可视化 |
| `GeoJsonLayer` | GeoJSON图层 | GeoJSON数据渲染 |
| `HeatmapLayer` | 热力图层 | 点数据密度热力 |
| `TerrainLayer` | 地形图层 | 3D地形高程 |

### 工具组件 (6个)

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LayerGroup` | 图层组 | 批量管理图层 |
| `SourceGroup` | 数据源组 | 批量管理数据源 |
| `AddImages` | 添加图片 | 注册图标资源 |
| `Fragment` | 片段容器 | 逻辑分组 |
| `HandleRawMap` | 原始地图处理 | 自定义JS |
| `SortLayers` | 图层排序 | 动态调整顺序 |

---

## 核心概念

### 1. 组件层级关系

```
MapContainer (地图容器)
├── Source (数据源)
│   └── Layer (图层)
├── SourceGroup (数据源组)
│   └── Source → Layer
├── LayerGroup (图层组)
│   └── Layer
├── Marker (标记)
├── Popup (弹窗)
├── [Control组件] (各类控件)
├── [Action组件] (动作组件)
└── [Deck.gl图层] (高性能可视化图层)
```

### 2. Source + Layer 分离模式

```python
# Source 定义数据来源
# Layer 定义可视化样式
# 一个 Source 可被多个 Layer 引用

fm.Source(
    fm.Layer(
        id='my-layer',
        layerProps={
            'type': 'circle',
            'source': 'my-source',
            'paint': {
                'circle-radius': 5,
                'circle-color': '#007cbf'
            }
        }
    ),
    id='my-source',
    sourceProps={
        'type': 'geojson',
        'data': geojson_data
    }
)
```

---

## 常用代码模式

### 基础地图

```python
fm.MapContainer(
    initialViewState={
        'longitude': 116.4,
        'latitude': 39.9,
        'zoom': 10
    },
    mapStyle='https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY',
    style={'height': '100vh'}
)
```

### 添加标记和弹窗

```python
fm.MapContainer(
    [
        fm.Marker(
            fm.Popup('这是北京'),
            longitude=116.4,
            latitude=39.9
        )
    ],
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    mapStyle='...',
    style={'height': '100vh'}
)
```

### GeoJSON 数据渲染

```python
fm.MapContainer(
    [
        fm.Source(
            fm.Layer(
                id='geojson-layer',
                layerProps={
                    'type': 'fill',
                    'source': 'geojson-source',
                    'paint': {
                        'fill-color': '#088',
                        'fill-opacity': 0.8
                    }
                }
            ),
            id='geojson-source',
            sourceProps={
                'type': 'geojson',
                'data': geojson_data
            }
        )
    ],
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    mapStyle='...',
    style={'height': '100vh'}
)
```

### 飞行动画

```python
from dash import callback, Input, Output

fm.MapContainer(
    id='map',
    children=[html.Div(id='action-container')],
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    mapStyle='...',
    style={'height': '100vh'}
)

@callback(
    Output('action-container', 'children'),
    Input('fly-button', 'n_clicks'),
    prevent_initial_call=True
)
def trigger_fly(n_clicks):
    return fm.FlyTo(
        mapActionConfig={
            'center': [121.47, 31.23],
            'zoom': 12,
            'duration': 2000
        }
    )
```

### 绘制功能

```python
fm.MapContainer(
    enableDraw=True,
    drawControls={
        'point': True,
        'line_string': True,
        'polygon': True,
        'trash': True
    },
    drawControlsPosition='top-left',
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    mapStyle='...',
    style={'height': '100vh'}
)

# 通过 drawnFeatures 属性获取绘制结果
@callback(
    Output('output', 'children'),
    Input('map', 'drawnFeatures')
)
def show_drawn(features):
    return str(features)
```

### 点击事件监听

```python
fm.MapContainer(
    id='map',
    clickListenLayerIds=['my-layer'],
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    mapStyle='...',
    style={'height': '100vh'}
)

@callback(
    Output('output', 'children'),
    Input('map', 'clickedLngLat'),
    Input('map', 'clickListenLayerFeatures')
)
def handle_click(lnglat, features):
    return f'点击位置: {lnglat}, 要素: {features}'
```

### Deck.gl 热力图

```python
fm.MapContainer(
    [
        fm.HeatmapLayer(
            id='heatmap',
            data=points_data,  # [{'position': [lng, lat], 'weight': n}, ...]
            getPosition='position',
            getWeight='weight',
            radiusPixels=30
        )
    ],
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    mapStyle='...',
    style={'height': '100vh'}
)
```

### 使用天地图

```python
fm.MapContainer(
    [
        fm.Source(
            fm.Layer(
                id='tianditu-layer',
                layerProps={'type': 'raster', 'source': 'tianditu'}
            ),
            id='tianditu',
            sourceProps={
                'type': 'raster',
                'tiles': [
                    'http://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=YOUR_TOKEN'
                ],
                'tileSize': 256
            }
        )
    ],
    initialViewState={'longitude': 116.4, 'latitude': 39.9, 'zoom': 10},
    style={'height': '100vh'}
)
```

---

## MapContainer 常用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 组件唯一标识 |
| `children` | component | 子组件 |
| `mapStyle` | string/dict | 底图样式配置 |
| `initialViewState` | dict | 初始视角配置 |
| `longitude` | number | 受控：中心点经度 |
| `latitude` | number | 受控：中心点纬度 |
| `zoom` | number | 受控：缩放级别 |
| `pitch` | number | 受控：倾斜角度 |
| `bearing` | number | 受控：旋转角度 |
| `minZoom` | number | 最小缩放级别 (默认0) |
| `maxZoom` | number | 最大缩放级别 (默认22) |
| `enableDraw` | boolean | 启用绘制功能 |
| `clickListenLayerIds` | list | 监听点击的图层ID |
| `locale` | string | 语言设置 (默认'zh-cn') |

## initialViewState 结构

```python
{
    'longitude': 116.4,      # 中心点经度
    'latitude': 39.9,        # 中心点纬度
    'zoom': 10,              # 缩放级别 (0-24)
    'pitch': 0,              # 倾斜角度 (0-85)
    'bearing': 0,            # 旋转角度 (0-360)
    'bounds': [minLng, minLat, maxLng, maxLat]  # 边界范围
}
```

## mapActionConfig 通用结构

```python
{
    'center': [lng, lat],    # 目标中心点
    'zoom': 10,              # 目标缩放级别
    'pitch': 45,             # 目标倾斜角度
    'bearing': 90,           # 目标旋转角度
    'duration': 2000,        # 动画持续时间（毫秒）
    'animate': True,         # 是否启用动画
    'padding': {             # 视口内边距
        'top': 50,
        'bottom': 50,
        'left': 50,
        'right': 50
    }
}
```

---

## flc vs fm 对比

| 特性 | flc (Leaflet) | fm (MapLibre) |
|------|---------------|---------------|
| 底层技术 | Leaflet.js | MapLibre GL + Deck.gl |
| 渲染方式 | DOM | WebGL |
| 性能 | 中等 | 高 (适合大数据) |
| 3D支持 | 有限 | 完整 |
| 学习曲线 | 简单 | 中等 |
| 适用场景 | 一般地图应用 | 大数据、3D可视化 |

---

## 参考资源

- [MapLibre GL JS 官方文档](https://maplibre.org/maplibre-gl-js/docs/)
- [Deck.gl 官方文档](https://deck.gl/)

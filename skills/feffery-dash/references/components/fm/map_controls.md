# FM 地图控件

> feffery-maplibre 地图控件组件详解
> 导航、比例尺、定位、全屏、署名控件

---

## 控件组件概览

| 组件 | 说明 | 位置选项 |
|------|------|----------|
| `NavigationControl` | 导航控件 | top-left/right, bottom-left/right |
| `ScaleControl` | 比例尺 | top-left/right, bottom-left/right |
| `GeolocateControl` | 定位控件 | top-left/right, bottom-left/right |
| `FullscreenControl` | 全屏控件 | top-left/right, bottom-left/right |
| `AttributionControl` | 署名控件 | bottom-left/right |

**注意**: 绘制功能通过 `MapContainer` 的 `enableDraw` 参数启用，不是独立控件。

---

## NavigationControl 导航控件

提供缩放按钮和指南针功能。

### 基础用法

```python
import feffery_maplibre as fm

fm.MapContainer(
    initialViewState={
        'longitude': 116.4,
        'latitude': 39.9,
        'zoom': 10
    },
    mapStyle='https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY',
    children=[
        fm.NavigationControl()
    ],
    style={'height': '100vh'}
)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 组件唯一标识 |
| `position` | string | 'top-right' | 控件显示位置 |
| `showCompass` | boolean | True | 是否显示指南针 |
| `showZoom` | boolean | True | 是否显示缩放按钮 |
| `visualizePitch` | boolean | False | 指南针是否展示倾斜状态 |

### 自定义位置

```python
fm.NavigationControl(
    position='top-left',
    showCompass=True,
    showZoom=True,
    visualizePitch=True
)
```

---

## ScaleControl 比例尺控件

显示地图比例尺。

### 基础用法

```python
fm.ScaleControl(
    position='bottom-left',
    maxWidth=100,
    unit='metric'
)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 组件唯一标识 |
| `position` | string | 'bottom-left' | 控件显示位置 |
| `maxWidth` | number | 100 | 比例尺最大宽度（像素） |
| `unit` | string | 'metric' | 单位：'metric'/'imperial'/'nautical' |

---

## GeolocateControl 定位控件

获取用户地理位置。

### 基础用法

```python
fm.GeolocateControl(
    id='geolocate-control',
    position='top-right',
    trackUserLocation=True,
    showUserLocation=True,
    showAccuracyCircle=True
)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 组件唯一标识 |
| `position` | string | 'top-right' | 控件显示位置 |
| `trackUserLocation` | boolean | False | 持续追踪用户位置 |
| `showUserLocation` | boolean | True | 显示用户位置标记 |
| `showAccuracyCircle` | boolean | True | 显示精度圈 |

---

## FullscreenControl 全屏控件

切换地图全屏显示。

### 基础用法

```python
fm.FullscreenControl(
    position='top-right'
)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 组件唯一标识 |
| `position` | string | 'top-right' | 控件显示位置 |

---

## AttributionControl 署名控件

显示地图数据来源信息。

### 基础用法

```python
fm.AttributionControl(
    position='bottom-right',
    compact=True
)
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 组件唯一标识 |
| `position` | string | 'bottom-right' | 控件显示位置 |
| `compact` | boolean | False | 是否使用紧凑模式 |
| `customAttribution` | string | - | 自定义署名文本 |

---

## 绘制功能

绘制功能通过 `MapContainer` 的参数启用，不是独立控件。

### 启用绘制

```python
fm.MapContainer(
    id='map',
    enableDraw=True,
    drawControls={
        'point': True,
        'line_string': True,
        'polygon': True,
        'trash': True
    },
    drawControlsPosition='top-left',
    initialViewState={
        'longitude': 116.4,
        'latitude': 39.9,
        'zoom': 10
    },
    mapStyle='...',
    style={'height': '100vh'}
)
```

### 获取绘制数据

```python
from dash import callback, Input, Output

@callback(
    Output('draw-result', 'children'),
    Input('map', 'drawnFeatures')
)
def show_features(features):
    if features:
        return f"绘制了 {len(features.get('features', []))} 个要素"
    return '未绘制'
```

---

## 组合使用示例

```python
import dash
from dash import html
import feffery_maplibre as fm

app = dash.Dash(__name__)

app.layout = html.Div([
    fm.MapContainer(
        id='map',
        initialViewState={
            'longitude': 116.4,
            'latitude': 39.9,
            'zoom': 10,
            'pitch': 45
        },
        mapStyle='https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY',
        children=[
            fm.NavigationControl(
                position='top-right',
                visualizePitch=True
            ),
            fm.ScaleControl(
                position='bottom-left',
                unit='metric'
            ),
            fm.FullscreenControl(
                position='top-right'
            ),
            fm.GeolocateControl(
                position='top-right'
            )
        ],
        enableDraw=True,
        drawControls={
            'polygon': True,
            'trash': True
        },
        drawControlsPosition='top-left',
        style={'height': '100vh'}
    )
])

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 参考链接

- [MapLibre NavigationControl](https://maplibre.org/maplibre-gl-js/docs/API/classes/NavigationControl/)
- [MapLibre ScaleControl](https://maplibre.org/maplibre-gl-js/docs/API/classes/ScaleControl/)
- [MapLibre GeolocateControl](https://maplibre.org/maplibre-gl-js/docs/API/classes/GeolocateControl/)
- [MapLibre FullscreenControl](https://maplibre.org/maplibre-gl-js/docs/API/classes/FullscreenControl/)
- [MapLibre AttributionControl](https://maplibre.org/maplibre-gl-js/docs/API/classes/AttributionControl/)

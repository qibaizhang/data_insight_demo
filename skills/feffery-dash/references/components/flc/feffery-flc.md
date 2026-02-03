# feffery-leaflet-components AI 辅助开发指南

> feffery-leaflet-components (简称 `flc`) 是基于 Leaflet.js 的 Plotly Dash 地图组件库
> 组件数量: 30+ | 官方文档: https://flc.feffery.tech/

当用户需要基于 Leaflet.js 的交互式地图时使用 flc 组件。

---

## 快速开始

```python
# 安装
pip install feffery-leaflet-components

# 导入
import feffery_leaflet_components as flc
from dash import Dash, html, Input, Output, callback

# 最简单的地图
app = Dash(__name__)
app.layout = html.Div([
    flc.LeafletMap(
        [
            flc.LeafletTileLayer()
        ],
        center={'lng': 116.38, 'lat': 39.9},
        zoom=10,
        style={'height': '500px'}  # 必须设置高度！
    )
])
```

---

## 组件分类索引

### 1. 核心容器组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LeafletMap` | 地图容器 | `center`, `zoom`, `style`, `editToolbar` |
| `LeafletMapProvider` | 地图编排 | 管理多地图实例 |
| `LeafletMapSync` | 地图同步 | 多地图视角同步 |

### 2. 图层组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LeafletTileLayer` | 瓦片底图 | `url`, `attribution` |
| `LeafletVectorTile` | 矢量切片 | 矢量瓦片图层 |
| `LeafletImageOverlay` | 图片叠加 | `url`, `bounds` |
| `EsriTiledMapLayer` | ESRI瓦片 | ESRI服务 |
| `LeafletLayerGroup` | 图层分组 | 批量管理图层 |
| `LeafletFeatureGroup` | 要素分组 | 带事件的要素组 |

### 3. 标记与要素组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LeafletMarker` | 标记点 | `position`, `iconOptions`, `draggable` |
| `LeafletCircleMarker` | 圆形标记 | `center`, `radius`, `pathOptions` |
| `LeafletCircle` | 圆形要素 | `center`, `radius` (米) |
| `LeafletPolyline` | 折线 | `positions`, `pathOptions` |
| `LeafletPolygon` | 多边形 | `positions`, `pathOptions` |
| `LeafletRectangle` | 矩形 | `bounds` |
| `LeafletGeoJSON` | GeoJSON渲染 | `data`, `mode`, `featureValueToStyles` |

### 4. 信息展示组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LeafletPopup` | 弹框 | `children`, `position` |
| `LeafletTooltip` | 信息框 | `children`, `permanent` |

### 5. 可视化图层组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LeafletHeatMap` | 热力图 | `points`, `radius`, `blur`, `gradient` |
| `LeafletStaticHeatMap` | 静态热力图 | `data` |
| `LeafletFlowLayer` | 流线图(迁徙图) | `flowData` |
| `LeafletAntPath` | 蚂蚁路径(动画线) | `positions`, `delay`, `dashArray` |
| `LeafletSuperCluster` | 巨量标记聚类 | `data` |

### 6. 控件组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `LeafletMiniMap` | 迷你地图 | 鹰眼图 |
| `LeafletFullscreenControl` | 全屏控件 | 地图全屏化 |
| `LeafletExport` | 导出控件 | 导出地图图片 |
| `LeafletTileSelect` | 底图切换 | `urls`, `selectedUrl` |

### 7. 事件与交互组件

| 组件 | 用途 | 回调属性 |
|------|------|----------|
| `LeafletMapAction` | 地图动作 | `mapActionConfig` |
| `LeafletMapListener` | 事件监听 | `_center`, `_zoom`, `_bounds` |

### 8. 工具组件

| 组件 | 用途 |
|------|------|
| `LeafletDomWrapper` | 元素包装器 |
| `Fragment` | 空节点组件 |

### 9. 工具函数

| 函数/类 | 用途 |
|---------|------|
| `wgs2gcj(lng, lat)` | WGS84 → GCJ02 |
| `gcj2wgs(lng, lat)` | GCJ02 → WGS84 |
| `gcj2bd(lng, lat)` | GCJ02 → BD09 |
| `bd2gcj(lng, lat)` | BD09 → GCJ02 |
| `wgs2bd(lng, lat)` | WGS84 → BD09 |
| `bd2wgs(lng, lat)` | BD09 → WGS84 |
| `SegmentedColoring` | 分段着色工具类 |
| `get_palette()` | 获取调色方案 |

---

## 常用代码模式

### 基础地图

```python
flc.LeafletMap(
    [
        flc.LeafletTileLayer()
    ],
    center={'lng': 116.38, 'lat': 39.9},
    zoom=10,
    style={'height': '500px'}
)
```

### 添加标记点

```python
flc.LeafletMap(
    [
        flc.LeafletTileLayer(),
        flc.LeafletMarker(
            position={'lng': 116.38, 'lat': 39.9},
            children=flc.LeafletTooltip('这是北京')
        )
    ],
    center={'lng': 116.38, 'lat': 39.9},
    zoom=10,
    style={'height': '500px'}
)
```

### 自定义图标标记

```python
flc.LeafletMarker(
    position={'lng': 116.38, 'lat': 39.9},
    iconOptions={
        'iconUrl': '/assets/marker.png',
        'iconSize': [32, 32],
        'iconAnchor': [16, 32],
        'popupAnchor': [0, -32]
    }
)
```

### GeoJSON 分级渲染

```python
flc.LeafletMap(
    [
        flc.LeafletTileLayer(),
        flc.LeafletGeoJSON(
            data=geojson_data,
            mode='choropleth',
            featureValueField='value',
            featureValueToStyles={
                'bins': [[0, 100], [100, 200], [200, 300]],
                'styles': [
                    {'fillColor': '#ffffcc'},
                    {'fillColor': '#a1dab4'},
                    {'fillColor': '#41b6c4'}
                ]
            }
        )
    ],
    style={'height': '500px'}
)
```

### 热力图

```python
flc.LeafletMap(
    [
        flc.LeafletTileLayer(),
        flc.LeafletHeatMap(
            points=[
                {'lng': 116.38, 'lat': 39.9, 'weight': 1},
                {'lng': 116.40, 'lat': 39.92, 'weight': 2},
            ],
            radius=25,
            blur=15,
            gradient={
                0.4: 'blue',
                0.6: 'cyan',
                0.8: 'yellow',
                1.0: 'red'
            }
        )
    ],
    style={'height': '500px'}
)
```

### 监听地图事件

```python
from dash import callback, Input, Output

flc.LeafletMap(
    [
        flc.LeafletTileLayer(),
        flc.LeafletMapListener(id='map-listener')
    ],
    style={'height': '500px'}
)

@callback(
    Output('output', 'children'),
    Input('map-listener', '_center'),
    Input('map-listener', '_zoom')
)
def update_info(center, zoom):
    return f'中心: {center}, 缩放级别: {zoom}'
```

### 地图动作控制

```python
from dash import callback, Input, Output

flc.LeafletMap(
    [
        flc.LeafletTileLayer(),
        flc.LeafletMapAction(id='map-action')
    ],
    style={'height': '500px'}
)

@callback(
    Output('map-action', 'mapActionConfig'),
    Input('fly-btn', 'nClicks'),
    prevent_initial_call=True
)
def fly_to_location(n):
    return {
        'type': 'fly-to',
        'center': {'lng': 116.38, 'lat': 39.9},
        'zoom': 15,
        'flyToDuration': 'normal'
    }
```

### 地图编辑模式

```python
flc.LeafletMap(
    [
        flc.LeafletTileLayer()
    ],
    id='map-edit',
    editToolbar=True,
    showMeasurements=True,
    editToolbarControlsOptions={
        'drawMarker': True,
        'drawPolyline': True,
        'drawPolygon': True,
        'editMode': True,
        'dragMode': True,
        'removalMode': True
    },
    style={'height': '500px'}
)

@callback(
    Output('output', 'children'),
    Input('map-edit', '_drawnShapes')
)
def get_shapes(shapes):
    return str(shapes)
```

### 坐标系转换

```python
from feffery_leaflet_components import wgs2gcj, gcj2bd

# WGS84 转 GCJ02 (高德/腾讯)
lng, lat = wgs2gcj(116.38, 39.9)

# GCJ02 转 BD09 (百度)
lng, lat = gcj2bd(116.38, 39.9)
```

---

## 坐标系说明

| 坐标系 | 简称 | 使用场景 |
|--------|------|----------|
| WGS84 | wgs | GPS原始坐标，国际通用 |
| GCJ02 | gcj | 国测局坐标，高德/腾讯地图 |
| BD09 | bd | 百度坐标系，百度地图专用 |

---

## 注意事项

1. **地图容器必须有高度**：`style={'height': '500px'}` 是必须的
2. **底图加载**：大多数场景需要添加 `LeafletTileLayer` 作为底图
3. **组件嵌套**：标记、图层等组件应作为 `LeafletMap` 的 `children` 传入
4. **坐标格式**：统一使用 `{'lng': 经度, 'lat': 纬度}` 格式
5. **编辑模式**：设置 `editToolbar=True` 可开启绘制编辑功能

---

## 相关资源

- [feffery-leaflet-components 官方文档](https://flc.feffery.tech/)
- [Leaflet.js 官方文档](https://leafletjs.com/)
- [Plotly Dash 官方文档](https://dash.plotly.com/)
- [feffery-leaflet-components GitHub](https://github.com/CNFeffery/feffery-leaflet-components)

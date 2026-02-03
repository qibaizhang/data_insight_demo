# FLC 图层组件

> feffery-leaflet-components 图层类组件详解
> 基于 Leaflet 的各种地图图层和覆盖物

---

## 图层组件概览

### 基础图层

| 组件 | 说明 | 用途 |
|------|------|------|
| LeafletTileLayer | 瓦片图层 | 底图服务 |
| LeafletImageOverlay | 图片叠加 | 自定义底图 |
| LeafletVectorTile | 矢量切片 | 矢量瓦片图层 |
| EsriTiledMapLayer | ESRI瓦片 | ESRI服务 |

### 矢量图层

| 组件 | 说明 | 用途 |
|------|------|------|
| LeafletMarker | 标记点 | 位置标注 |
| LeafletCircleMarker | 圆形标记 | 数据点 |
| LeafletPolyline | 折线 | 路径轨迹 |
| LeafletPolygon | 多边形 | 区域范围 |
| LeafletCircle | 圆形 | 范围圈 |
| LeafletRectangle | 矩形 | 选区框 |

### 高级图层

| 组件 | 说明 | 用途 |
|------|------|------|
| LeafletGeoJSON | GeoJSON | 地理数据 |
| LeafletHeatMap | 热力图 | 密度分布 |
| LeafletFlowLayer | 流向图 | 方向流动 |
| LeafletAntPath | 蚂蚁线 | 动态路径 |

---

## 瓦片图层 TileLayer

### 常用底图服务

```python
# 高德地图
flc.LeafletTileLayer(
    url='https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
    attribution='高德地图'
)

# 天地图（需申请 token）
flc.LeafletTileLayer(
    url='https://t0.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=YOUR_TOKEN',
    attribution='天地图'
)

# OpenStreetMap
flc.LeafletTileLayer(
    url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution='OpenStreetMap'
)

# 卫星影像（高德）
flc.LeafletTileLayer(
    url='https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
    attribution='高德卫星'
)
```

### 底图切换

使用 `LeafletTileSelect` 组件实现底图切换（参见"图层组和控制"部分的详细示例）：

```python
flc.LeafletMap(
    [
        flc.LeafletTileLayer(id='tile-layer'),
        flc.LeafletTileSelect(
            id='tile-select',
            urls=[
                {'url': 'https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}'},
                {'url': 'https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'},
            ]
        )
    ],
    style={'height': '500px'}
)
```

---

## 标记点 Marker

### 基础标记

```python
flc.LeafletMarker(
    id='my-marker',
    position={'lat': 39.9042, 'lng': 116.4074},
    title='北京'
)
```

### 自定义图标

```python
flc.LeafletMarker(
    position={'lat': 39.9042, 'lng': 116.4074},
    iconOptions={
        'iconUrl': '/assets/marker.png',
        'iconSize': [32, 32],
        'iconAnchor': [16, 32],
        'popupAnchor': [0, -32]
    }
)
```

### Div 图标

```python
flc.LeafletMarker(
    position={'lat': 39.9042, 'lng': 116.4074},
    divIconOptions={
        'html': '<div style="background: #1890ff; color: white; padding: 4px 8px; border-radius: 4px;">标签</div>',
        'iconSize': [60, 24],
        'iconAnchor': [30, 12]
    }
)
```

### 弹出框和提示

```python
flc.LeafletMarker(
    position={'lat': 39.9042, 'lng': 116.4074},
    children=[
        flc.LeafletPopup('这是弹出内容'),
        flc.LeafletTooltip('这是提示内容', permanent=True)
    ]
)
```

---

## 圆形标记 CircleMarker

```python
flc.LeafletCircleMarker(
    center={'lat': 39.9042, 'lng': 116.4074},
    radius=10,  # 像素半径
    pathOptions={
        'color': '#1890ff',
        'fillColor': '#1890ff',
        'fillOpacity': 0.5,
        'weight': 2
    }
)
```

---

## 折线 Polyline

### 基础折线

```python
flc.LeafletPolyline(
    positions=[
        {'lat': 39.9042, 'lng': 116.4074},
        {'lat': 31.2304, 'lng': 121.4737},
        {'lat': 23.1291, 'lng': 113.2644}
    ],
    pathOptions={
        'color': '#1890ff',
        'weight': 3,
        'opacity': 0.8
    }
)
```

### 多段线

```python
flc.LeafletPolyline(
    positions=[
        [  # 第一段
            {'lat': 39.9, 'lng': 116.4},
            {'lat': 31.2, 'lng': 121.5}
        ],
        [  # 第二段
            {'lat': 31.2, 'lng': 121.5},
            {'lat': 23.1, 'lng': 113.3}
        ]
    ]
)
```

---

## 多边形 Polygon

```python
flc.LeafletPolygon(
    positions=[
        {'lat': 39.9, 'lng': 116.3},
        {'lat': 39.9, 'lng': 116.5},
        {'lat': 39.8, 'lng': 116.5},
        {'lat': 39.8, 'lng': 116.3}
    ],
    pathOptions={
        'color': '#ff4d4f',
        'fillColor': '#ff4d4f',
        'fillOpacity': 0.3,
        'weight': 2
    }
)
```

---

## 圆形 Circle

```python
flc.LeafletCircle(
    center={'lat': 39.9042, 'lng': 116.4074},
    radius=5000,  # 米
    pathOptions={
        'color': '#52c41a',
        'fillColor': '#52c41a',
        'fillOpacity': 0.2
    }
)
```

---

## GeoJSON 图层

### 加载 GeoJSON

```python
import json

with open('data/china.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

flc.LeafletGeoJSON(
    data=geojson_data,
    style={
        'color': '#1890ff',
        'weight': 1,
        'fillColor': '#1890ff',
        'fillOpacity': 0.3
    },
    hoverStyle={
        'fillOpacity': 0.6
    }
)
```

### 动态样式

```python
flc.LeafletGeoJSON(
    data=geojson_data,
    featureStyleFunction='''
        (feature) => {
            const value = feature.properties.value;
            return {
                fillColor: value > 100 ? '#ff4d4f' : value > 50 ? '#faad14' : '#52c41a',
                fillOpacity: 0.6,
                color: '#fff',
                weight: 1
            };
        }
    '''
)
```

### 点击交互

```python
flc.LeafletGeoJSON(
    id='geojson-layer',
    data=geojson_data,
    featureIdField='name'  # 特征 ID 字段
)

@callback(
    Output('result', 'children'),
    Input('geojson-layer', 'clickFeature'),
    prevent_initial_call=True
)
def handle_click(feature):
    if feature:
        return f"点击: {feature['properties']['name']}"
    return ''
```

---

## 热力图 HeatMap

```python
flc.LeafletHeatMap(
    points=[
        {'lng': 116.4, 'lat': 39.9, 'weight': 100},
        {'lng': 116.45, 'lat': 39.95, 'weight': 80},
        {'lng': 116.35, 'lat': 39.85, 'weight': 60},
        # 更多点...
    ],
    radius=25,
    blur=15,
    max=100,  # 权重最大值
    minOpacity=0.3,
    gradient={
        0.4: 'blue',
        0.6: 'cyan',
        0.7: 'lime',
        0.8: 'yellow',
        1.0: 'red'
    }
)
```

---

## 蚂蚁线 AntPath

```python
flc.LeafletAntPath(
    positions=[
        {'lat': 39.9, 'lng': 116.4},
        {'lat': 31.2, 'lng': 121.5},
        {'lat': 23.1, 'lng': 113.3}
    ],
    pathOptions={
        'color': '#1890ff',
        'weight': 4,
        'opacity': 0.8
    },
    delay=400,      # 动画延迟
    dashArray=[10, 20],  # 虚线样式
    pulseColor='#fff'
)
```

---

## 图层组和控制

### 图层组

```python
flc.LeafletLayerGroup(
    id='markers-group',
    children=[
        flc.LeafletMarker(position={'lat': 39.9, 'lng': 116.4}),
        flc.LeafletMarker(position={'lat': 31.2, 'lng': 121.5}),
    ]
)
```

### 特征组

```python
flc.LeafletFeatureGroup(
    id='features-group',
    children=[...],
    fitBounds=True  # 自动调整视野
)
```

### 图层控制（底图切换）

使用 `LeafletTileSelect` 组件实现底图切换：

```python
from dash import callback, Input, Output

flc.LeafletMap(
    [
        flc.LeafletTileLayer(id='tile-layer'),
        flc.LeafletTileSelect(
            id='tile-select',
            urls=[
                {'url': 'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'},
                {'url': 'https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}'},
            ],
            center={'lng': 116.38, 'lat': 39.9},
            zoom=5
        )
    ],
    style={'height': '500px'}
)

@callback(
    Output('tile-layer', 'url'),
    Input('tile-select', 'selectedUrl')
)
def change_tile(url):
    return url
```

---

## 参考资源

- [feffery-leaflet-components 官方文档](https://flc.feffery.tech/)

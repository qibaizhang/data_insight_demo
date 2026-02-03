# FM Deck.gl 图层

> feffery-maplibre Deck.gl 高性能可视化图层
> 基于 deck.gl 的 WebGL 高性能渲染

---

## 图层概览

feffery-maplibre 集成了 **4 个** Deck.gl 高性能可视化图层：

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| `ArcLayer` | 弧线图层 | OD流向图、迁徙图、航线 |
| `GeoJsonLayer` | GeoJSON图层 | 矢量数据渲染、3D建筑 |
| `HeatmapLayer` | 热力图层 | 点密度热力、人口分布 |
| `TerrainLayer` | 地形图层 | 3D地形高程可视化 |

---

## ArcLayer 弧线图层

用于绘制起点终点之间的弧线，展示迁徙流向、航线等。

### 基础用法

```python
import feffery_maplibre as fm

fm.ArcLayer(
    id='arc-layer',
    data=[
        {
            'source': [116.4, 39.9],
            'target': [121.47, 31.23],
            'weight': 100
        }
    ],
    getSourcePosition='source',
    getTargetPosition='target',
    getSourceColor=[255, 100, 100, 200],
    getTargetColor=[100, 100, 255, 200],
    getWidth=2,
    pickable=True
)
```

### 主要参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 图层唯一标识 |
| `data` | list/string | 数据源或 URL |
| `getSourcePosition` | string/dict | 起点坐标字段 |
| `getTargetPosition` | string/dict | 终点坐标字段 |
| `getSourceColor` | list/dict | 起点颜色 [r,g,b,a] |
| `getTargetColor` | list/dict | 终点颜色 [r,g,b,a] |
| `getWidth` | number/dict | 弧线宽度 |
| `getHeight` | number | 弧线高度系数 (0-1) |
| `greatCircle` | boolean | 大圆弧线模式 |
| `pickable` | boolean | 启用交互 |
| `autoHighlight` | boolean | 自动高亮悬停 |

### 数据驱动方式

```python
# 1. 字段名直接引用
getSourcePosition='source'

# 2. 固定颜色值
getSourceColor=[255, 0, 0, 255]

# 3. 函数表达式
getWidth={'func': 'd => d.weight / 20'}
```

---

## GeoJsonLayer GeoJSON图层

渲染 GeoJSON 格式的矢量数据，支持点、线、面及 3D 拉伸。

### 主要参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 图层唯一标识 |
| `data` | dict/string | GeoJSON 数据或 URL |
| `filled` | boolean | 是否填充面 |
| `stroked` | boolean | 是否描边 |
| `extruded` | boolean | 是否3D拉伸 |
| `getFillColor` | list/dict | 填充颜色 |
| `getLineColor` | list/dict | 描边颜色 |
| `getLineWidth` | number/dict | 描边宽度 |
| `getElevation` | number/dict | 3D拉伸高度 |
| `pickable` | boolean | 启用交互 |

---

## HeatmapLayer 热力图层

将点数据渲染为热力密度图。

### 基础用法

```python
fm.HeatmapLayer(
    id='heatmap-layer',
    data=[
        {'position': [116.4, 39.9], 'weight': 1},
        {'position': [116.5, 39.95], 'weight': 2}
    ],
    getPosition='position',
    getWeight='weight',
    radiusPixels=30
)
```

### 主要参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | - | 图层唯一标识 |
| `data` | list/string | [] | 数据源或 URL |
| `getPosition` | string/dict | - | 位置坐标字段 |
| `getWeight` | number/dict | 1 | 权重字段 |
| `radiusPixels` | number | 30 | 热力点像素半径 |
| `colorRange` | list | - | 颜色渐变数组 |
| `intensity` | number | 1 | 热力强度系数 |
| `threshold` | number | 0.05 | 热力阈值 |
| `aggregation` | string | SUM | 聚合方式 SUM/MEAN |

---

## TerrainLayer 地形图层

3D 地形高程可视化。

### 主要参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 图层唯一标识 |
| `elevationData` | string | 高程瓦片 URL 模板 |
| `texture` | string | 纹理贴图 URL 模板 |
| `elevationDecoder` | dict | 高程解码参数 |
| `bounds` | list | 显示范围 [minLng, minLat, maxLng, maxLat] |

---

## 图层交互

### 点击事件

```python
from dash import callback, Input, Output

fm.ArcLayer(
    id='clickable-layer',
    data=data,
    pickable=True,
    autoHighlight=True,
    highlightColor=[255, 255, 0, 128]
)

@callback(
    Output('result', 'children'),
    Input('clickable-layer', 'clickEvent'),
    prevent_initial_call=True
)
def handle_click(event):
    if event:
        return f"点击: {event}"
    return ""
```

---

## 参考链接

- [Deck.gl ArcLayer](https://deck.gl/docs/api-reference/layers/arc-layer)
- [Deck.gl GeoJsonLayer](https://deck.gl/docs/api-reference/layers/geojson-layer)
- [Deck.gl HeatmapLayer](https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer)
- [Deck.gl TerrainLayer](https://deck.gl/docs/api-reference/geo-layers/terrain-layer)

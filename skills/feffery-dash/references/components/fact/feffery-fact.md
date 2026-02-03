# feffery-antd-charts (fact) 组件库

> feffery-antd-charts 图表组件库 Skill
> 组件数量: 36 | 官方文档: https://fact.feffery.tech/

当用户需要数据可视化图表时使用 fact 组件喵～

---

## 快速开始

```python
import feffery_antd_charts as fact
from dash import Dash, html

app = Dash(__name__)
app.layout = html.Div([
    fact.AntdLine(
        data=[
            {'date': '2020-01', 'value': 100},
            {'date': '2020-02', 'value': 120},
        ],
        xField='date',
        yField='value'
    )
])
```

---

## 图表分类速查

### 基础图表 → [详细文档](./basic_charts.md)

| 组件 | 中文名 | 必填参数 | 说明 |
|------|--------|----------|------|
| `AntdLine` | 折线图 | `data`, `xField`, `yField` | 趋势展示 |
| `AntdArea` | 面积图 | `data`, `xField`, `yField` | 趋势+量级 |
| `AntdColumn` | 柱状图 | `data`, `xField`, `yField` | 分类对比（垂直） |
| `AntdBar` | 条形图 | `data`, `xField`, `yField` | 分类对比（水平） |
| `AntdPie` | 饼图 | `data`, `angleField`, `colorField` | 占比分布 |
| `AntdScatter` | 散点图 | `data`, `xField`, `yField` | 分布关系 |

### 高级图表 → [详细文档](./special_charts.md)

| 组件 | 中文名 | 必填参数 | 说明 |
|------|--------|----------|------|
| `AntdDualAxes` | 双轴图 | `data`, `xField`, `yField` | 不同量级对比 |
| `AntdBidirectionalBar` | 双向条形图 | `data`, `xField`, `yField` | 对比分析 |
| `AntdHeatmap` | 热力图 | `data`, `xField`, `yField`, `colorField` | 二维数据密度 |
| `AntdRadar` | 雷达图 | `data`, `xField`, `yField` | 多维对比 |
| `AntdFunnel` | 漏斗图 | `data`, `xField`, `yField` | 转化漏斗 |
| `AntdSankey` | 桑基图 | `data`, `sourceField`, `targetField`, `weightField` | 数据流向 |
| `AntdTreemap` | 矩形树图 | `data`, `colorField` | 层级占比 |
| `AntdWaterfall` | 瀑布图 | `data`, `xField`, `yField` | 增减变化 |
| `AntdStock` | 股票图 | `data`, `xField`, `yField` | K线图 |
| `AntdRose` | 玫瑰图 | `data`, `xField`, `yField` | 极坐标柱状图 |
| `AntdChord` | 弦图 | `data`, `sourceField`, `targetField`, `weightField` | 关系流转 |
| `AntdWordCloud` | 词云图 | `data`, `wordField`, `weightField` | 文本分析 |
| `AntdVenn` | 韦恩图 | `data` | 集合关系 |
| `AntdSunburst` | 旭日图 | `data` | 层级环形 |
| `AntdRadialBar` | 玉珏图 | `data`, `xField`, `yField` | 极坐标条形 |

### 统计图表 → [详细文档](./statistical_charts.md)

| 组件 | 中文名 | 必填参数 | 说明 |
|------|--------|----------|------|
| `AntdHistogram` | 直方图 | `data`, `binField` | 数据分布 |
| `AntdBox` | 箱线图 | `data`, `xField`, `yField` | 统计分布 |
| `AntdViolin` | 小提琴图 | `data`, `xField`, `yField` | 分布密度 |

### 指标图表

| 组件 | 中文名 | 必填参数 | 说明 |
|------|--------|----------|------|
| `AntdGauge` | 仪表盘 | `percent` | 完成度展示 |
| `AntdLiquid` | 水波图 | `percent` | 百分比动画 |
| `AntdProgress` | 进度条 | `percent` | 线性进度 |
| `AntdRingProgress` | 环形进度条 | `percent` | 环形进度 |
| `AntdBullet` | 子弹图 | `data`, `measureField`, `rangeField`, `targetField` | 目标达成 |

### 迷你图表

| 组件 | 中文名 | 必填参数 | 说明 |
|------|--------|----------|------|
| `AntdTinyLine` | 迷你折线图 | `data` | 表格内嵌用 |
| `AntdTinyColumn` | 迷你柱状图 | `data` | 表格内嵌用 |
| `AntdTinyArea` | 迷你面积图 | `data` | 表格内嵌用 |

### 关系图表 → [详细文档](./relation_charts.md)

| 组件 | 中文名 | 必填参数 | 说明 |
|------|--------|----------|------|
| `AntdDecompositionTree` | 分解树 | `data` | 层级树形展示 |
| `AntdFundFlow` | 资金流向图 | `data` | 资金流动关系 |
| `AntdRadialTree` | 辐射树 | `data` | 放射状树形 |

---

## 通用配置

### 尺寸与布局

```python
fact.AntdLine(
    data=[...],
    xField='x',
    yField='y',
    width=600,           # 宽度
    height=400,          # 高度
    autoFit=True,        # 自适应父容器
    padding='auto',      # 内边距
)
```

### 坐标轴配置

```python
xAxis={
    'title': {'text': 'X轴标题'},
    'label': {'rotate': -45, 'autoRotate': True},
},
yAxis={
    'title': {'text': 'Y轴标题'},
    'min': 0,
    'max': 100,
},
```

### 图例配置

```python
legend={
    'position': 'top-right',  # 位置: 'top'|'top-left'|'top-right'|'left'|'right'|'bottom'
    'layout': 'horizontal',   # 布局: 'horizontal'|'vertical'
},
# legend=False  # 隐藏图例
```

### 信息框配置

```python
tooltip={
    'showTitle': True,
    'title': 'fieldName',
    'showMarkers': True,
    'shared': True,  # 合并展示
},
# tooltip=False  # 禁用信息框
```

### 标注配置

```python
annotations=[
    {
        'type': 'text',
        'position': ['50%', '50%'],
        'content': '标注文本',
    },
    {
        'type': 'line',
        'start': ['min', 100],
        'end': ['max', 100],
        'style': {'stroke': 'red', 'lineDash': [4, 4]},
    },
]
```

---

## 样式配置

### 通用图形样式

```python
{
    'fill': '#1890ff',        # 填充颜色
    'fillOpacity': 0.8,       # 填充透明度
    'stroke': '#000',         # 轮廓颜色
    'lineWidth': 1,           # 轮廓宽度
    'lineDash': [4, 4],       # 虚线配置
    'opacity': 1,             # 整体透明度
    'radius': 4,              # 圆角
}
```

### JS 函数配置

```python
# 格式化函数
formatter={'func': '(value) => value + "%"'}

# 样式函数
lineStyle={'func': '(datum) => ({stroke: datum.type === "A" ? "red" : "blue"})'}

# 颜色函数
color={'func': '(datum) => datum.value > 100 ? "#f00" : "#0f0"'}
```

---

## 回调交互

### 监听点击事件

```python
fact.AntdColumn(
    id='my-chart',
    data=[...],
    xField='type',
    yField='value',
)

@callback(
    Output('output', 'children'),
    Input('my-chart', 'recentlyColumnClickRecord')
)
def handle_click(record):
    if record:
        return f"点击了: {record['data']}"
    return ""
```

### 监听图例点击

```python
@callback(
    Output('output', 'children'),
    Input('my-chart', 'recentlyLegendInfo')
)
def handle_legend(info):
    if info:
        return f"图例: {info['triggerItemName']}"
    return ""
```

### 下载图表

```python
fact.AntdColumn(id='my-chart', ...),
fac.AntdButton('下载', id='download-btn'),

@callback(
    Output('my-chart', 'downloadTrigger'),
    Input('download-btn', 'nClicks'),
    prevent_initial_call=True
)
def download(n):
    import time
    return str(time.time())
```

---

## 参考资源

- [feffery-antd-charts 官方文档](https://fact.feffery.tech/)
- [Ant Design Charts 官方文档](https://charts.ant.design/)
- [G2Plot API 文档](https://g2plot.antv.vision/)

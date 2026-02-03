# FACT 基础图表

> feffery-antd-charts 基础图表类组件详解
> 折线图、柱状图、饼图、面积图、散点图

---

## 基础图表概览

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| AntdLine | 折线图 | 趋势展示 |
| AntdArea | 面积图 | 趋势+量级 |
| AntdColumn | 柱状图 | 分类对比 |
| AntdBar | 条形图 | 横向分类对比 |
| AntdPie | 饼图 | 占比分布 |
| AntdScatter | 散点图 | 分布关系 |

---

## 折线图 AntdLine

### 基础折线图

```python
fact.AntdLine(
    id='basic-line',
    data=[
        {'date': '2024-01', 'value': 100},
        {'date': '2024-02', 'value': 150},
        {'date': '2024-03', 'value': 120},
        {'date': '2024-04', 'value': 180},
    ],
    xField='date',
    yField='value'
)
```

### 多系列折线图

```python
fact.AntdLine(
    id='multi-line',
    data=[
        {'date': '2024-01', 'value': 100, 'type': '产品A'},
        {'date': '2024-01', 'value': 80, 'type': '产品B'},
        {'date': '2024-02', 'value': 150, 'type': '产品A'},
        {'date': '2024-02', 'value': 120, 'type': '产品B'},
        # ...
    ],
    xField='date',
    yField='value',
    seriesField='type',
    smooth=True,  # 平滑曲线
    point={'size': 4},  # 数据点
    legend={'position': 'top-right'}
)
```

### 常用配置

```python
fact.AntdLine(
    data=data,
    xField='date',
    yField='value',

    # 样式配置
    smooth=True,                    # 平滑曲线
    color=['#1890ff', '#52c41a'],   # 颜色
    lineStyle={'lineWidth': 2},     # 线条样式

    # 数据点
    point={
        'size': 4,
        'shape': 'circle',  # 'circle' | 'square' | 'diamond' | 'triangle'
        'style': {'fill': 'white', 'stroke': '#1890ff'}
    },

    # 坐标轴
    xAxis={
        'title': {'text': '日期'},
        'tickCount': 5
    },
    yAxis={
        'title': {'text': '销售额'},
        'min': 0
    },

    # 提示框
    tooltip={
        'showMarkers': True,
        'shared': True,  # 共享提示框
        'formatter': {'func': "datum => ({ name: datum.type, value: '¥' + datum.value })"}
    },

    # 图例
    legend={
        'position': 'top-right',
        'itemName': {'style': {'fontSize': 12}}
    },

    # 标注线
    annotations=[
        {
            'type': 'line',
            'start': ['min', 150],
            'end': ['max', 150],
            'style': {'stroke': '#ff4d4f', 'lineDash': [4, 4]},
            'text': {'content': '目标线', 'position': 'start'}
        }
    ]
)
```

---

## 面积图 AntdArea

### 基础面积图

```python
fact.AntdArea(
    data=data,
    xField='date',
    yField='value',
    smooth=True,
    areaStyle={'fill': 'l(270) 0:#ffffff 1:#1890ff'}  # 渐变填充
)
```

### 堆叠面积图

```python
fact.AntdArea(
    data=data,
    xField='date',
    yField='value',
    seriesField='type',
    isStack=True,  # 堆叠
    smooth=True
)
```

### 百分比面积图

```python
fact.AntdArea(
    data=data,
    xField='date',
    yField='value',
    seriesField='type',
    isPercent=True,  # 百分比
    smooth=True
)
```

---

## 柱状图 AntdColumn

### 基础柱状图

```python
fact.AntdColumn(
    id='basic-column',
    data=[
        {'category': '类别A', 'value': 100},
        {'category': '类别B', 'value': 150},
        {'category': '类别C', 'value': 80},
    ],
    xField='category',
    yField='value',
    color='#1890ff',
    columnWidthRatio=0.6,  # 柱子宽度比例
    label={'position': 'middle'}  # 标签位置
)
```

### 分组柱状图

```python
fact.AntdColumn(
    data=data,
    xField='category',
    yField='value',
    seriesField='type',
    isGroup=True,  # 分组
    color=['#1890ff', '#52c41a', '#faad14']
)
```

### 堆叠柱状图

```python
fact.AntdColumn(
    data=data,
    xField='category',
    yField='value',
    seriesField='type',
    isStack=True,  # 堆叠
    label={
        'position': 'middle',
        'layout': [
            {'type': 'interval-adjust-position'},
            {'type': 'interval-hide-overlap'},
            {'type': 'adjust-color'}
        ]
    }
)
```

### 百分比堆叠

```python
fact.AntdColumn(
    data=data,
    xField='category',
    yField='value',
    seriesField='type',
    isStack=True,
    isPercent=True
)
```

---

## 条形图 AntdBar

### 基础条形图

```python
fact.AntdBar(
    data=data,
    xField='value',  # 注意：条形图 x 和 y 相反
    yField='category',
    color='#1890ff',
    barWidthRatio=0.6
)
```

### 堆叠条形图

```python
fact.AntdBar(
    data=data,
    xField='value',
    yField='category',
    seriesField='type',
    isStack=True
)
```

---

## 饼图 AntdPie

### 基础饼图

```python
fact.AntdPie(
    id='basic-pie',
    data=[
        {'type': '分类A', 'value': 27},
        {'type': '分类B', 'value': 25},
        {'type': '分类C', 'value': 18},
        {'type': '分类D', 'value': 15},
        {'type': '其他', 'value': 15},
    ],
    angleField='value',
    colorField='type',
    radius=0.9
)
```

### 环形图

```python
fact.AntdPie(
    data=data,
    angleField='value',
    colorField='type',
    radius=0.9,
    innerRadius=0.6,  # 内环半径
    statistic={
        'title': {'content': '总计'},
        'content': {'content': '100'}
    }
)
```

### 玫瑰图

```python
fact.AntdPie(
    data=data,
    angleField='value',
    colorField='type',
    radius=0.9,
    innerRadius=0.3,
    isDonut=True  # 玫瑰图
)
```

### 标签配置

```python
fact.AntdPie(
    data=data,
    angleField='value',
    colorField='type',
    radius=0.9,
    label={
        'type': 'spider',  # 'inner' | 'outer' | 'spider'
        'content': '{name}: {percentage}'
    },
    legend={
        'position': 'right',
        'layout': 'vertical'
    }
)
```

---

## 散点图 AntdScatter

### 基础散点图

```python
fact.AntdScatter(
    data=[
        {'x': 10, 'y': 20},
        {'x': 15, 'y': 25},
        {'x': 20, 'y': 18},
        # ...
    ],
    xField='x',
    yField='y',
    size=5,
    color='#1890ff'
)
```

### 气泡图

```python
fact.AntdScatter(
    data=data,
    xField='x',
    yField='y',
    colorField='type',  # 按类型着色
    sizeField='value',  # 按值调整大小
    size=[4, 20],       # 大小范围
    shape='circle'
)
```

### 回归线

```python
fact.AntdScatter(
    data=data,
    xField='x',
    yField='y',
    regressionLine={
        'type': 'linear',  # 'linear' | 'exp' | 'loess' | 'log' | 'poly' | 'pow' | 'quad'
        'style': {'stroke': '#ff4d4f'}
    }
)
```

---

## 通用交互配置

### 点击事件

```python
fact.AntdColumn(
    id='click-chart',
    data=data,
    xField='category',
    yField='value'
)

@callback(
    Output('result', 'children'),
    Input('click-chart', 'recentlyColumnClickRecord'),
    prevent_initial_call=True
)
def handle_click(record):
    if record:
        return f"点击: {record['data']}"
    return dash.no_update
```

### 区域选择

```python
fact.AntdLine(
    id='brush-chart',
    data=data,
    xField='date',
    yField='value',
    brush={
        'enabled': True,
        'type': 'x-rect'  # 'x-rect' | 'y-rect' | 'rect' | 'path' | 'circle'
    }
)

@callback(
    Output('selected-range', 'children'),
    Input('brush-chart', 'recentlyBrushArea')
)
def handle_brush(area):
    if area:
        return f"选择范围: {area}"
    return ''
```

---

## 参考资源

- [feffery-antd-charts 官方文档](https://fact.feffery.tech/)
- [Ant Design Charts 官方文档](https://charts.ant.design/)

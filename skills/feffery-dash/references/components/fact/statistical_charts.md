# FACT 统计图表

> feffery-antd-charts 统计类图表组件详解
> 直方图、箱线图、热力图、雷达图等

---

## 统计图表概览

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| AntdHistogram | 直方图 | 数据分布 |
| AntdBox | 箱线图 | 统计分布 |
| AntdHeatmap | 热力图 | 二维数据分布 |
| AntdRadar | 雷达图 | 多维对比 |
| AntdWordCloud | 词云图 | 文本分析 |

---

## 直方图 AntdHistogram

### 基础直方图

```python
# 直方图用于展示数据分布
fact.AntdHistogram(
    id='histogram',
    data=[
        {'value': 10}, {'value': 15}, {'value': 20},
        {'value': 22}, {'value': 25}, {'value': 28},
        {'value': 30}, {'value': 35}, {'value': 40},
        # 更多数据...
    ],
    binField='value',
    binWidth=5,  # 柱宽（分组间隔）
    color='#1890ff'
)
```

### 分组直方图

```python
fact.AntdHistogram(
    data=data,
    binField='value',
    binWidth=10,
    stackField='type',  # 分组字段
    color=['#1890ff', '#52c41a']
)
```

---

## 箱线图 AntdBox

### 基础箱线图

```python
fact.AntdBox(
    id='box-plot',
    data=[
        {'x': '类别A', 'y': [10, 15, 20, 25, 30]},
        {'x': '类别B', 'y': [12, 18, 22, 28, 35]},
        {'x': '类别C', 'y': [8, 12, 18, 24, 28]},
    ],
    xField='x',
    yField='y',
    boxStyle={
        'stroke': '#1890ff',
        'fill': '#1890ff',
        'fillOpacity': 0.3
    }
)
```

### 分组箱线图

```python
fact.AntdBox(
    data=data,
    xField='x',
    yField='y',
    groupField='group',
    color=['#1890ff', '#52c41a']
)
```

---

## 热力图 AntdHeatmap

### 基础热力图

```python
# 日历热力图数据
data = [
    {'date': '2024-01-01', 'commits': 10},
    {'date': '2024-01-02', 'commits': 5},
    {'date': '2024-01-03', 'commits': 0},
    # ...
]

fact.AntdHeatmap(
    id='heatmap',
    data=data,
    xField='week',      # 横轴
    yField='day',       # 纵轴
    colorField='value', # 颜色映射字段
    color=['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'],
    shape='square',     # 'circle' | 'square' | 'rect'
    sizeRatio=0.9
)
```

### 矩阵热力图

```python
# 相关性矩阵
data = [
    {'x': 'A', 'y': 'A', 'value': 1},
    {'x': 'A', 'y': 'B', 'value': 0.8},
    {'x': 'A', 'y': 'C', 'value': 0.3},
    {'x': 'B', 'y': 'A', 'value': 0.8},
    {'x': 'B', 'y': 'B', 'value': 1},
    {'x': 'B', 'y': 'C', 'value': 0.5},
    # ...
]

fact.AntdHeatmap(
    data=data,
    xField='x',
    yField='y',
    colorField='value',
    color=['#f0f0f0', '#1890ff'],
    label={
        'style': {'fill': '#333', 'fontSize': 12}
    },
    tooltip={
        'formatter': {'func': "datum => ({ name: `${datum.x}-${datum.y}`, value: datum.value.toFixed(2) })"}
    }
)
```

---

## 雷达图 AntdRadar

### 基础雷达图

```python
fact.AntdRadar(
    id='radar',
    data=[
        {'item': '技术', 'score': 80},
        {'item': '设计', 'score': 70},
        {'item': '产品', 'score': 85},
        {'item': '运营', 'score': 60},
        {'item': '市场', 'score': 75},
    ],
    xField='item',
    yField='score',
    area={'style': {'fillOpacity': 0.3}},
    point={'size': 4},
    xAxis={
        'line': None,
        'tickLine': None
    },
    yAxis={
        'min': 0,
        'max': 100,
        'grid': {'line': {'style': {'lineDash': [4, 4]}}}
    }
)
```

### 多系列雷达图

```python
data = [
    {'item': '技术', 'score': 80, 'user': '用户A'},
    {'item': '设计', 'score': 70, 'user': '用户A'},
    {'item': '产品', 'score': 85, 'user': '用户A'},
    {'item': '技术', 'score': 90, 'user': '用户B'},
    {'item': '设计', 'score': 65, 'user': '用户B'},
    {'item': '产品', 'score': 75, 'user': '用户B'},
    # ...
]

fact.AntdRadar(
    data=data,
    xField='item',
    yField='score',
    seriesField='user',
    color=['#1890ff', '#52c41a'],
    area={'style': {'fillOpacity': 0.2}},
    point={'size': 3}
)
```

---

## 词云图 AntdWordCloud

### 基础词云

```python
fact.AntdWordCloud(
    id='wordcloud',
    data=[
        {'text': 'Python', 'value': 100},
        {'text': 'JavaScript', 'value': 80},
        {'text': 'Dash', 'value': 90},
        {'text': 'React', 'value': 70},
        {'text': '数据分析', 'value': 85},
        {'text': '可视化', 'value': 75},
        # 更多词汇...
    ],
    wordField='text',
    weightField='value',
    colorField='text',
    color=['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1'],
    wordStyle={
        'fontFamily': 'Microsoft YaHei',
        'fontSize': [16, 80],  # 字号范围
        'rotation': [-45, 0, 45, 90]  # 旋转角度
    },
    spiral='rectangular'  # 'archimedean' | 'rectangular'
)
```

### 形状词云

```python
fact.AntdWordCloud(
    data=data,
    wordField='text',
    weightField='value',
    imageMask='https://example.com/shape.png',  # 形状图片
    wordStyle={
        'fontSize': [12, 60]
    }
)
```

---

## 小型图表 (迷你图)

### 迷你折线图

```python
fact.AntdTinyLine(
    data=[100, 120, 90, 150, 130, 180, 160],
    smooth=True,
    height=60,
    width=200,
    autoFit=False
)
```

### 迷你柱状图

```python
fact.AntdTinyColumn(
    data=[100, 120, 90, 150, 130, 180, 160],
    height=60,
    width=200,
    autoFit=False,
    columnWidthRatio=0.5
)
```

### 迷你面积图

```python
fact.AntdTinyArea(
    data=[100, 120, 90, 150, 130, 180, 160],
    smooth=True,
    height=60,
    width=200,
    autoFit=False,
    areaStyle={'fill': 'l(270) 0:#ffffff 1:#1890ff'}
)
```

### 在表格中使用迷你图

```python
# 表格列中嵌入迷你图
columns = [
    {'title': '产品', 'dataIndex': 'product'},
    {'title': '趋势', 'dataIndex': 'trend', 'renderOptions': {'renderType': 'custom'}}
]

data = [
    {
        'product': '产品A',
        'trend': fact.AntdTinyLine(
            data=[10, 20, 15, 25, 30],
            smooth=True,
            height=30,
            width=100,
            autoFit=False
        )
    }
]
```

---

## 进度类图表

### 进度环

```python
fact.AntdRingProgress(
    percent=0.75,
    width=120,
    height=120,
    color=['#1890ff', '#e8e8e8'],
    statistic={
        'title': {'style': {'fontSize': 12, 'color': '#666'}},
        'content': {'style': {'fontSize': 24, 'color': '#1890ff'}}
    }
)
```

### 仪表盘

```python
fact.AntdGauge(
    percent=0.75,
    width=200,
    height=200,
    range={'color': ['#52c41a', '#faad14', '#ff4d4f']},
    indicator={
        'pointer': {'style': {'stroke': '#333'}},
        'pin': {'style': {'stroke': '#333'}}
    },
    statistic={
        'content': {
            'formatter': {'func': "datum => `${(datum.percent * 100).toFixed(0)}%`"}
        }
    }
)
```

---

## 参考资源

- [feffery-antd-charts 官方文档](https://fact.feffery.tech/)
- [Ant Design Charts 官方文档](https://charts.ant.design/)

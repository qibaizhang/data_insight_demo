# FACT 特殊图表

> feffery-antd-charts 特殊类图表组件详解
> 桑基图、漏斗图、瀑布图、双轴图、股票图等

---

## 特殊图表概览

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| AntdSankey | 桑基图 | 流量转化 |
| AntdFunnel | 漏斗图 | 转化漏斗 |
| AntdWaterfall | 瀑布图 | 增减变化 |
| AntdDualAxes | 双轴图 | 不同量级对比 |
| AntdBidirectionalBar | 双向条形图 | 对比分析 |
| AntdStock | 股票图 | K线图 |
| AntdTreemap | 矩形树图 | 层级占比 |
| AntdLiquid | 水波图 | 进度展示 |
| AntdBullet | 子弹图 | 目标达成 |
| AntdChord | 弦图 | 关系流转 |
| AntdRose | 玫瑰图 | 多维占比 |

---

## 桑基图 AntdSankey

### 基础桑基图

```python
fact.AntdSankey(
    id='sankey',
    data={
        'nodes': [
            {'id': '访问'},
            {'id': '注册'},
            {'id': '活跃'},
            {'id': '付费'},
            {'id': '流失'}
        ],
        'links': [
            {'source': '访问', 'target': '注册', 'value': 80},
            {'source': '访问', 'target': '流失', 'value': 20},
            {'source': '注册', 'target': '活跃', 'value': 60},
            {'source': '注册', 'target': '流失', 'value': 20},
            {'source': '活跃', 'target': '付费', 'value': 40},
            {'source': '活跃', 'target': '流失', 'value': 20},
        ]
    },
    sourceField='source',
    targetField='target',
    weightField='value',
    nodeWidthRatio=0.01,
    nodePaddingRatio=0.03,
    color=['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1']
)
```

### 配置节点样式

```python
fact.AntdSankey(
    data=data,
    sourceField='source',
    targetField='target',
    weightField='value',
    nodeStyle={
        'opacity': 1,
        'fillOpacity': 0.8,
        'lineWidth': 1,
        'stroke': '#fff'
    },
    edgeStyle={
        'fillOpacity': 0.5
    }
)
```

---

## 漏斗图 AntdFunnel

### 基础漏斗图

```python
fact.AntdFunnel(
    id='funnel',
    data=[
        {'stage': '访问', 'number': 5000},
        {'stage': '浏览', 'number': 3500},
        {'stage': '加购', 'number': 2000},
        {'stage': '下单', 'number': 1200},
        {'stage': '付款', 'number': 800},
    ],
    xField='stage',
    yField='number',
    dynamicHeight=True,  # 动态高度
    label={
        'formatter': {'func': "datum => "}
    }
)
```

### 对比漏斗图

```python
fact.AntdFunnel(
    data=data,
    xField='stage',
    yField='number',
    seriesField='type',  # 分组对比
    isTransposed=False,  # 垂直/水平
    compareField='type'
)
```

---

## 瀑布图 AntdWaterfall

### 基础瀑布图

```python
fact.AntdWaterfall(
    id='waterfall',
    data=[
        {'type': '期初', 'money': 10000},
        {'type': '收入', 'money': 5000},
        {'type': '营销', 'money': -2000},
        {'type': '研发', 'money': -1500},
        {'type': '运营', 'money': -1000},
        {'type': '期末', 'money': 10500},
    ],
    xField='type',
    yField='money',
    total={
        'label': '总计',
        'style': {'fill': '#1890ff'}
    },
    risingFill='#52c41a',   # 上涨颜色
    fallingFill='#ff4d4f',  # 下跌颜色
    label={
        'position': 'middle'
    }
)
```

---

## 双轴图 AntdDualAxes

### 折线+柱状图

```python
data = [
    {'date': '2024-01', 'sales': 1000, 'profit': 150},
    {'date': '2024-02', 'sales': 1200, 'profit': 180},
    {'date': '2024-03', 'sales': 1100, 'profit': 160},
    {'date': '2024-04', 'sales': 1400, 'profit': 220},
]

fact.AntdDualAxes(
    id='dual-axes',
    data=[data, data],  # 两组数据
    xField='date',
    yField=['sales', 'profit'],  # 两个 Y 字段
    geometryOptions=[
        {
            'geometry': 'column',  # 柱状图
            'color': '#1890ff',
            'columnWidthRatio': 0.4
        },
        {
            'geometry': 'line',    # 折线图
            'color': '#52c41a',
            'lineStyle': {'lineWidth': 2},
            'point': {'size': 4}
        }
    ],
    legend={
        'itemName': {
            'formatter': {'func': "(text, item) => item.value === 'sales' ? '销售额' : '利润'"}
        }
    }
)
```

### 双折线图

```python
fact.AntdDualAxes(
    data=[data1, data2],
    xField='date',
    yField=['value1', 'value2'],
    geometryOptions=[
        {'geometry': 'line', 'color': '#1890ff', 'smooth': True},
        {'geometry': 'line', 'color': '#52c41a', 'smooth': True}
    ]
)
```

---

## 双向条形图 AntdBidirectionalBar

```python
fact.AntdBidirectionalBar(
    id='bidirectional-bar',
    data=[
        {'age': '0-10', 'male': 100, 'female': 95},
        {'age': '10-20', 'male': 120, 'female': 115},
        {'age': '20-30', 'male': 150, 'female': 140},
        {'age': '30-40', 'male': 130, 'female': 125},
        {'age': '40-50', 'male': 110, 'female': 105},
    ],
    xField='age',
    yField=['male', 'female'],
    color=['#1890ff', '#f5222d'],
    legend={
        'itemName': {
            'formatter': {'func': "text => text === 'male' ? '男性' : '女性'"}
        }
    }
)
```

---

## 股票图 AntdStock

```python
fact.AntdStock(
    id='stock-chart',
    data=[
        {'date': '2024-01-01', 'open': 100, 'close': 105, 'high': 110, 'low': 98, 'volume': 50000},
        {'date': '2024-01-02', 'open': 105, 'close': 102, 'high': 108, 'low': 100, 'volume': 45000},
        # ...
    ],
    xField='date',
    yField=['open', 'close', 'high', 'low'],
    risingFill='#f5222d',   # 上涨颜色
    fallingFill='#52c41a',  # 下跌颜色
    tooltip={
        'fields': ['open', 'close', 'high', 'low', 'volume']
    }
)
```

---

## 矩形树图 AntdTreemap

```python
fact.AntdTreemap(
    id='treemap',
    data={
        'name': 'root',
        'children': [
            {
                'name': '分类A',
                'children': [
                    {'name': '子项1', 'value': 100},
                    {'name': '子项2', 'value': 80},
                ]
            },
            {
                'name': '分类B',
                'children': [
                    {'name': '子项3', 'value': 120},
                    {'name': '子项4', 'value': 60},
                ]
            }
        ]
    },
    colorField='name',
    color=['#1890ff', '#52c41a', '#faad14', '#f5222d'],
    label={
        'style': {'fill': '#fff'}
    },
    rectStyle={
        'lineWidth': 1,
        'stroke': '#fff'
    }
)
```

---

## 水波图 AntdLiquid

```python
fact.AntdLiquid(
    id='liquid',
    percent=0.65,
    width=200,
    height=200,
    outline={
        'border': 4,
        'distance': 4
    },
    wave={
        'length': 128
    },
    statistic={
        'content': {
            'formatter': {'func': "datum => "},
            'style': {'fontSize': 24}
        }
    }
)
```

---

## 子弹图 AntdBullet

```python
fact.AntdBullet(
    id='bullet',
    data=[
        {
            'title': '指标1',
            'ranges': [100],
            'measures': [80],
            'target': 90
        },
        {
            'title': '指标2',
            'ranges': [100],
            'measures': [60],
            'target': 75
        }
    ],
    measureField='measures',
    rangeField='ranges',
    targetField='target',
    xField='title',
    color={
        'range': '#e8e8e8',
        'measure': '#1890ff',
        'target': '#333'
    }
)
```

---

## 玫瑰图 AntdRose

```python
fact.AntdRose(
    id='rose',
    data=[
        {'type': '分类A', 'value': 27},
        {'type': '分类B', 'value': 25},
        {'type': '分类C', 'value': 18},
        {'type': '分类D', 'value': 15},
        {'type': '分类E', 'value': 10},
    ],
    xField='type',
    yField='value',
    seriesField='type',
    radius=0.9,
    color=['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1'],
    label={
        'offset': -15,
        'style': {'fill': '#fff'}
    }
)
```

---

## 参考资源

- [feffery-antd-charts 官方文档](https://fact.feffery.tech/)
- [Ant Design Charts 官方文档](https://charts.ant.design/)

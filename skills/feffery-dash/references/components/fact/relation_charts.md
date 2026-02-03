# FACT 关系图表

> feffery-antd-charts 关系类图表组件详解
> 分解树、资金流向图、辐射树

---

## 关系图表概览

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| AntdDecompositionTree | 分解树 | 层级数据树形展示 |
| AntdFundFlow | 资金流向图 | 资金流动关系 |
| AntdRadialTree | 辐射树 | 放射状树形结构 |

---

## 分解树 AntdDecompositionTree

### 基础分解树

```python
fact.AntdDecompositionTree(
    id='decomposition-tree',
    data={
        'id': 'root',
        'value': {'title': '总销售额', 'items': [{'text': '100万'}]},
        'children': [
            {
                'id': 'region-1',
                'value': {'title': '华北区', 'items': [{'text': '40万'}]},
                'children': [
                    {'id': 'city-1', 'value': {'title': '北京', 'items': [{'text': '25万'}]}},
                    {'id': 'city-2', 'value': {'title': '天津', 'items': [{'text': '15万'}]}},
                ]
            },
            {
                'id': 'region-2',
                'value': {'title': '华东区', 'items': [{'text': '60万'}]},
                'children': [
                    {'id': 'city-3', 'value': {'title': '上海', 'items': [{'text': '35万'}]}},
                    {'id': 'city-4', 'value': {'title': '杭州', 'items': [{'text': '25万'}]}},
                ]
            }
        ]
    },
    autoFit=True,
    nodeCfg={
        'title': {
            'style': {'fill': '#fff'}
        },
        'items': {
            'style': {'fill': '#fff'}
        },
        'style': {
            'fill': '#1890ff',
            'stroke': '#1890ff'
        }
    },
    markerCfg={
        'show': True,
        'collapsed': False
    }
)
```

### 常用配置

```python
fact.AntdDecompositionTree(
    data=data,

    # 布局配置
    layout='horizontal',  # 'horizontal' | 'vertical'

    # 节点配置
    nodeCfg={
        'title': {
            'style': {'fontSize': 14, 'fill': '#333'}
        },
        'items': {
            'style': {'fontSize': 12, 'fill': '#666'}
        },
        'style': {
            'fill': '#f0f0f0',
            'stroke': '#d9d9d9',
            'radius': 4
        },
        'padding': [10, 15]
    },

    # 边配置
    edgeCfg={
        'style': {
            'stroke': '#d9d9d9',
            'lineWidth': 1
        }
    },

    # 展开折叠标记
    markerCfg={
        'show': True,
        'collapsed': True,  # 默认折叠
        'position': 'right',  # 'left' | 'right' | 'top' | 'bottom'
        'style': {
            'fill': '#1890ff',
            'stroke': '#1890ff'
        }
    },

    # 行为配置
    behaviors=['drag-canvas', 'zoom-canvas']
)
```

---

## 资金流向图 AntdFundFlow

### 基础资金流向图

```python
fact.AntdFundFlow(
    id='fund-flow',
    data={
        'nodes': [
            {'id': 'node-0', 'value': {'title': '公司总部', 'items': [{'text': '1000万'}]}},
            {'id': 'node-1', 'value': {'title': '华北分公司', 'items': [{'text': '300万'}]}},
            {'id': 'node-2', 'value': {'title': '华东分公司', 'items': [{'text': '400万'}]}},
            {'id': 'node-3', 'value': {'title': '华南分公司', 'items': [{'text': '300万'}]}},
        ],
        'edges': [
            {'source': 'node-0', 'target': 'node-1', 'value': '300万'},
            {'source': 'node-0', 'target': 'node-2', 'value': '400万'},
            {'source': 'node-0', 'target': 'node-3', 'value': '300万'},
        ]
    },
    autoFit=True,
    nodeCfg={
        'title': {
            'style': {'fill': '#333'}
        },
        'items': {
            'style': {'fill': '#666'}
        },
        'style': {
            'fill': '#f5f5f5',
            'stroke': '#d9d9d9',
            'radius': 4
        }
    },
    edgeCfg={
        'label': {
            'style': {
                'fill': '#1890ff',
                'fontSize': 12
            }
        },
        'style': {
            'stroke': '#1890ff',
            'lineWidth': 1
        }
    }
)
```

### 带交互的资金流向图

```python
fact.AntdFundFlow(
    id='interactive-fund-flow',
    data=data,

    # 节点配置
    nodeCfg={
        'title': {
            'style': {'fill': '#333', 'fontSize': 14}
        },
        'items': {
            'style': {'fill': '#666', 'fontSize': 12}
        },
        'style': {'func': '''(node) => {
            return {
                fill: node.value.status === 'warning' ? '#ff4d4f' : '#1890ff',
                stroke: node.value.status === 'warning' ? '#ff4d4f' : '#1890ff',
            };
        }'''}
    },

    # 边配置
    edgeCfg={
        'style': {'func': '''(edge) => {
            return {
                stroke: edge.value > 500 ? '#ff4d4f' : '#52c41a',
                lineWidth: Math.log(edge.value) + 1,
            };
        }'''},
        'endArrow': True
    },

    # 行为
    behaviors=['drag-canvas', 'zoom-canvas', 'drag-node']
)
```

---

## 辐射树 AntdRadialTree

### 基础辐射树

```python
fact.AntdRadialTree(
    id='radial-tree',
    data={
        'id': 'root',
        'value': {'text': '中心节点'},
        'children': [
            {
                'id': 'child-1',
                'value': {'text': '分支1'},
                'children': [
                    {'id': 'leaf-1', 'value': {'text': '叶子1'}},
                    {'id': 'leaf-2', 'value': {'text': '叶子2'}},
                ]
            },
            {
                'id': 'child-2',
                'value': {'text': '分支2'},
                'children': [
                    {'id': 'leaf-3', 'value': {'text': '叶子3'}},
                    {'id': 'leaf-4', 'value': {'text': '叶子4'}},
                ]
            },
            {
                'id': 'child-3',
                'value': {'text': '分支3'},
                'children': [
                    {'id': 'leaf-5', 'value': {'text': '叶子5'}},
                ]
            }
        ]
    },
    autoFit=True,
    nodeCfg={
        'size': 30,
        'style': {
            'fill': '#1890ff',
            'stroke': '#1890ff'
        },
        'label': {
            'style': {'fill': '#333', 'fontSize': 12}
        }
    },
    edgeCfg={
        'style': {
            'stroke': '#d9d9d9',
            'lineWidth': 1
        }
    }
)
```

### 自定义辐射树样式

```python
fact.AntdRadialTree(
    data=data,

    # 布局配置
    layout={
        'type': 'compactBox',
        'direction': 'LR',  # 'LR' | 'RL' | 'TB' | 'BT' | 'H' | 'V'
        'radial': True
    },

    # 节点配置
    nodeCfg={
        'size': [80, 30],
        'type': 'rect',  # 'circle' | 'rect' | 'ellipse' | 'diamond' | 'triangle'
        'style': {'func': '''(node) => {
            const level = node.depth || 0;
            return {
                fill: ['#1890ff', '#52c41a', '#faad14', '#f5222d'][level % 4],
                stroke: ['#1890ff', '#52c41a', '#faad14', '#f5222d'][level % 4],
                radius: 4
            };
        }'''},
        'label': {
            'style': {'fill': '#fff', 'fontSize': 12}
        }
    },

    # 边配置
    edgeCfg={
        'type': 'polyline',  # 'line' | 'polyline' | 'cubic' | 'quadratic'
        'style': {
            'stroke': '#d9d9d9',
            'lineWidth': 1
        }
    },

    # 行为
    behaviors=['drag-canvas', 'zoom-canvas'],

    # 动画
    animate=True
)
```

---

## 通用交互回调

### 节点点击事件

```python
fact.AntdDecompositionTree(
    id='tree-chart',
    data=data,
    ...
)

@callback(
    Output('output', 'children'),
    Input('tree-chart', 'recentlyNodeClickRecord')
)
def handle_node_click(record):
    if record:
        return f"点击节点: {record['id']}"
    return ''
```

### 边点击事件

```python
@callback(
    Output('output', 'children'),
    Input('fund-flow-chart', 'recentlyEdgeClickRecord')
)
def handle_edge_click(record):
    if record:
        return f"点击边: {record['source']} -> {record['target']}"
    return ''
```

---

## 参考资源

- [feffery-antd-charts 官方文档](https://fact.feffery.tech/)
- [Ant Design Charts 官方文档](https://charts.ant.design/)

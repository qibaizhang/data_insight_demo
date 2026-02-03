# FAC 布局组件

> feffery-antd-components 布局类组件详解
> 网格、弹性布局、分割器、间距等

---

## 布局组件概览

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| AntdRow/AntdCol | 栅格布局 | 响应式页面布局 |
| AntdFlex | 弹性布局 | 灵活的弹性排列 |
| AntdSpace | 间距组件 | 元素间距控制 |
| AntdDivider | 分割线 | 内容分隔 |
| AntdLayout | 页面布局 | 整体页面结构 |
| AntdSplitter | 分割器 | 可拖拽分割面板 |
| AntdCenter | 居中组件 | 内容居中 |
| AntdCompact | 紧凑组件 | 表单组合 |

---

## 栅格布局 Row/Col

### 基础用法

```python
fac.AntdRow(
    [
        fac.AntdCol(html.Div('col-6'), span=6),
        fac.AntdCol(html.Div('col-6'), span=6),
        fac.AntdCol(html.Div('col-6'), span=6),
        fac.AntdCol(html.Div('col-6'), span=6),
    ],
    gutter=16  # 列间距
)
```

### 响应式布局

```python
fac.AntdRow(
    [
        fac.AntdCol(
            card_1,
            xs=24,   # <576px 全宽
            sm=12,   # ≥576px 半宽
            md=8,    # ≥768px 1/3
            lg=6,    # ≥992px 1/4
            xl=4,    # ≥1200px 1/6
            xxl=4    # ≥1600px 1/6
        ),
        # 更多列...
    ],
    gutter=[16, 16]  # [水平间距, 垂直间距]
)
```

### 偏移与推拉

```python
fac.AntdRow([
    # 偏移
    fac.AntdCol(content, span=6, offset=6),

    # 推拉（改变显示顺序）
    fac.AntdCol(content_a, span=6, push=6),   # 向右推
    fac.AntdCol(content_b, span=6, pull=6),   # 向左拉
])
```

### Flex 对齐

```python
# 水平对齐
fac.AntdRow(
    [...],
    justify='start'  # 'start' | 'center' | 'end' | 'space-around' | 'space-between' | 'space-evenly'
)

# 垂直对齐
fac.AntdRow(
    [...],
    align='middle'  # 'top' | 'middle' | 'bottom' | 'stretch'
)
```

---

## 弹性布局 Flex

### 基础用法

```python
fac.AntdFlex(
    [
        html.Div('Item 1'),
        html.Div('Item 2'),
        html.Div('Item 3'),
    ],
    gap='small',      # 间距: 'small' | 'middle' | 'large' | 数字
    wrap='wrap',      # 换行: 'nowrap' | 'wrap' | 'wrap-reverse'
    justify='center', # 主轴对齐
    align='center',   # 交叉轴对齐
    vertical=False    # 是否垂直排列
)
```

### 自适应填充

```python
fac.AntdFlex(
    [
        html.Div('固定宽度', style={'width': 200}),
        html.Div('自适应填充', style={'flex': 1}),
        html.Div('固定宽度', style={'width': 200}),
    ],
    gap='middle'
)
```

---

## 间距组件 Space

### 基础用法

```python
fac.AntdSpace(
    [
        fac.AntdButton('按钮1'),
        fac.AntdButton('按钮2'),
        fac.AntdButton('按钮3'),
    ],
    size='middle',     # 'small' | 'middle' | 'large' | 数字
    direction='horizontal',  # 'horizontal' | 'vertical'
    align='center',    # 'start' | 'center' | 'end' | 'baseline'
    wrap=True          # 是否自动换行
)
```

### 分隔符

```python
fac.AntdSpace(
    [
        fac.AntdButton('编辑'),
        fac.AntdButton('删除'),
        fac.AntdButton('更多'),
    ],
    split=fac.AntdDivider(direction='vertical')
)
```

---

## 分割线 Divider

```python
# 水平分割线
fac.AntdDivider()

# 带文字
fac.AntdDivider('分割标题', innerTextOrientation='center')

# 虚线
fac.AntdDivider(isDashed=True)

# 垂直分割线
fac.AntdDivider(direction='vertical')
```

---

## 页面布局 Layout

### 经典布局结构

```python
fac.AntdLayout(
    [
        # 顶部导航
        fac.AntdHeader(
            fac.AntdMenu(...),
            style={'background': '#001529'}
        ),

        fac.AntdLayout(
            [
                # 侧边栏
                fac.AntdSider(
                    fac.AntdMenu(...),
                    collapsible=True,
                    width=200
                ),

                # 内容区
                fac.AntdLayout(
                    [
                        fac.AntdContent(
                            [...],
                            style={'padding': 24, 'minHeight': 360}
                        ),
                        fac.AntdFooter(
                            '© 2024 My App',
                            style={'textAlign': 'center'}
                        )
                    ]
                )
            ]
        )
    ],
    style={'minHeight': '100vh'}
)
```

### 侧边栏折叠

```python
fac.AntdSider(
    fac.AntdMenu(...),
    id='sider',
    collapsible=True,
    collapsedWidth=80,
    width=200,
    theme='dark'
)

# 监听折叠状态
@callback(
    Output('menu', 'inlineCollapsed'),
    Input('sider', 'collapsed')
)
def sync_collapsed(collapsed):
    return collapsed
```

---

## 分割器 Splitter

### 水平分割

```python
fac.AntdSplitter(
    items=[
        {
            'children': html.Div('左侧面板'),
            'defaultSize': '30%',
            'min': '20%',
            'max': '50%',
            'collapsible': True
        },
        {
            'children': html.Div('右侧面板')
        }
    ]
)
```

### 垂直分割

```python
fac.AntdSplitter(
    items=[
        {'children': html.Div('上方面板'), 'defaultSize': '40%'},
        {'children': html.Div('下方面板')}
    ],
    layout='vertical',
    style={'height': 400}
)
```

### 嵌套分割

```python
fac.AntdSplitter(
    items=[
        {
            'children': html.Div('左侧'),
            'defaultSize': '25%'
        },
        {
            'children': fac.AntdSplitter(
                items=[
                    {'children': html.Div('右上'), 'defaultSize': '50%'},
                    {'children': html.Div('右下')}
                ],
                layout='vertical'
            )
        }
    ]
)
```

---

## 居中组件 Center

```python
fac.AntdCenter(
    fac.AntdSpin(size='large'),
    style={'height': '100vh'}
)
```

---

## 紧凑组合 Compact

```python
fac.AntdCompact(
    [
        fac.AntdSelect(
            options=[
                {'label': 'http://', 'value': 'http'},
                {'label': 'https://', 'value': 'https'},
            ],
            defaultValue='https',
            style={'width': 100}
        ),
        fac.AntdInput(
            placeholder='网站地址',
            style={'width': 300}
        ),
        fac.AntdButton('访问', type='primary')
    ]
)
```

---

## 布局最佳实践

### 1. 响应式仪表盘

```python
fac.AntdRow(
    [
        # KPI 卡片
        fac.AntdCol(kpi_card_1, xs=24, sm=12, xl=6),
        fac.AntdCol(kpi_card_2, xs=24, sm=12, xl=6),
        fac.AntdCol(kpi_card_3, xs=24, sm=12, xl=6),
        fac.AntdCol(kpi_card_4, xs=24, sm=12, xl=6),

        # 图表区域
        fac.AntdCol(chart_card_1, xs=24, xl=12),
        fac.AntdCol(chart_card_2, xs=24, xl=12),

        # 全宽区域
        fac.AntdCol(table_card, span=24),
    ],
    gutter=[18, 18]
)
```

### 2. 表单布局

```python
fac.AntdRow(
    [
        fac.AntdCol(
            fac.AntdFormItem(fac.AntdInput(), label='姓名'),
            span=12
        ),
        fac.AntdCol(
            fac.AntdFormItem(fac.AntdInput(), label='电话'),
            span=12
        ),
        fac.AntdCol(
            fac.AntdFormItem(fac.AntdTextArea(), label='备注'),
            span=24
        ),
    ],
    gutter=16
)
```

---

## 参考资源

- [feffery-antd-components 官方文档](https://fac.feffery.tech/)
- [Ant Design Layout 官方文档](https://ant.design/components/layout-cn)

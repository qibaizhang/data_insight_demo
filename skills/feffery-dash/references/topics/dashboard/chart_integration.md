# 仪表盘图表集成

> 仪表盘中图表组件的集成方式
> fact 图表与 fac 组件的联动

---

## 图表卡片封装

### 基础图表卡片

```python
from feffery_dash_utils.template_utils.dashboard_components import simple_chart_card

# 使用模板组件
simple_chart_card(
    title='销售趋势',
    extra=fac.AntdRadioGroup(...),
    children=fact.AntdLine(...)
)
```

### 自定义图表卡片

```python
def custom_chart_card(title, chart_id, extra_controls=None):
    return fac.AntdCard(
        [
            # 图表容器
            html.Div(
                fact.AntdLine(
                    id=chart_id,
                    data=[],
                    xField='date',
                    yField='value',
                    smooth=True,
                    height=300
                ),
                style={'minHeight': 300}
            )
        ],
        title=title,
        extra=extra_controls,
        bordered=False,
        headStyle={'borderBottom': 'none'},
        bodyStyle={'paddingTop': 0}
    )
```

---

## 图表与筛选联动

### 单图表联动

```python
# 布局
html.Div([
    fac.AntdCard([
        fac.AntdSpace([
            fac.AntdDateRangePicker(id='date-filter'),
            fac.AntdSelect(id='category-filter', options=[...])
        ])
    ], title='筛选'),

    fac.AntdCard([
        fact.AntdLine(id='main-chart', data=[], xField='date', yField='value')
    ], title='趋势图', style={'marginTop': 18})
])

# 回调
@callback(
    Output('main-chart', 'data'),
    Input('date-filter', 'value'),
    Input('category-filter', 'value')
)
def update_chart(date_range, category):
    df = load_data()

    if date_range:
        start, end = date_range
        df = df[(df['date'] >= start) & (df['date'] <= end)]

    if category:
        df = df[df['category'] == category]

    return df.to_dict('records')
```

### 多图表联动

```python
# 多个图表共享筛选器
@callback(
    Output('chart-1', 'data'),
    Output('chart-2', 'data'),
    Output('chart-3', 'data'),
    Input('global-filter', 'value')
)
def update_all_charts(filter_value):
    df = load_and_filter_data(filter_value)

    chart1_data = process_for_chart1(df)
    chart2_data = process_for_chart2(df)
    chart3_data = process_for_chart3(df)

    return chart1_data, chart2_data, chart3_data
```

---

## 图表点击下钻

### 基础下钻

```python
# 布局
html.Div([
    fac.AntdBreadcrumb(
        id='drill-breadcrumb',
        items=[{'title': '全部', 'key': 'all'}]
    ),
    fact.AntdColumn(
        id='drill-chart',
        data=[],
        xField='category',
        yField='value'
    )
])

# 回调
@callback(
    Output('drill-chart', 'data'),
    Output('drill-breadcrumb', 'items'),
    Input('drill-chart', 'recentlyColumnClickRecord'),
    Input('drill-breadcrumb', 'clickedItem'),
    State('drill-breadcrumb', 'items')
)
def handle_drill(click_record, breadcrumb_click, current_items):
    trigger = ctx.triggered_id

    if trigger == 'drill-chart' and click_record:
        # 图表点击，下钻
        clicked_category = click_record['data']['category']
        detail_data = get_detail_data(clicked_category)
        new_items = current_items + [{'title': clicked_category, 'key': clicked_category}]
        return detail_data, new_items

    elif trigger == 'drill-breadcrumb' and breadcrumb_click:
        # 面包屑点击，返回
        target_key = breadcrumb_click['itemKey']
        target_index = next(i for i, item in enumerate(current_items) if item['key'] == target_key)
        new_items = current_items[:target_index + 1]
        level_data = get_level_data(target_key)
        return level_data, new_items

    return dash.no_update, dash.no_update
```

---

## 图表与表格联动

### 图表选择更新表格

```python
# 布局
fac.AntdRow([
    fac.AntdCol(
        fac.AntdCard([
            fact.AntdPie(
                id='pie-chart',
                data=[...],
                angleField='value',
                colorField='type'
            )
        ], title='分类占比'),
        span=8
    ),
    fac.AntdCol(
        fac.AntdCard([
            fac.AntdTable(
                id='detail-table',
                columns=[...],
                data=[]
            )
        ], title='详细数据'),
        span=16
    )
])

# 回调
@callback(
    Output('detail-table', 'data'),
    Input('pie-chart', 'recentlyPieClickRecord')
)
def update_table_from_pie(click_record):
    if click_record:
        category = click_record['data']['type']
        detail_data = get_category_detail(category)
        return detail_data
    return []
```

### 表格行选择更新图表

```python
@callback(
    Output('trend-chart', 'data'),
    Input('product-table', 'selectedRowKeys'),
    State('product-table', 'data')
)
def update_chart_from_table(selected_keys, table_data):
    if selected_keys:
        selected_products = [row['product'] for row in table_data if row['key'] in selected_keys]
        chart_data = get_products_trend(selected_products)
        return chart_data
    return []
```

---

## 实时数据更新

### 定时刷新

```python
html.Div([
    dcc.Interval(id='refresh-interval', interval=5000),  # 5秒
    fact.AntdLine(id='realtime-chart', data=[], xField='time', yField='value')
])

@callback(
    Output('realtime-chart', 'data'),
    Input('refresh-interval', 'n_intervals'),
    State('realtime-chart', 'data')
)
def update_realtime(n, current_data):
    new_point = fetch_latest_point()

    # 使用 Patch 高效追加
    patched = Patch()
    patched.append(new_point)

    # 限制数据长度
    if len(current_data) > 50:
        patched.remove(0)

    return patched
```

### 数字动画

```python
import feffery_utils_components as fuc

# 配合 CountUp 实现数字滚动
@callback(
    Output('kpi-value', 'end'),
    Input('refresh-interval', 'n_intervals')
)
def update_kpi(n):
    return fetch_latest_kpi()

# 布局
fuc.FefferyCountUp(
    id='kpi-value',
    start=0,
    end=0,
    duration=1.5,
    prefix='¥'
)
```

---

## 图表导出

### 导出为图片

```python
import feffery_utils_components as fuc

html.Div([
    fuc.FefferyDom2Image(
        id='chart-screenshot',
        targetSelector='#chart-container',
        scale=2
    ),
    html.Div(
        fact.AntdLine(id='export-chart', ...),
        id='chart-container'
    ),
    fac.AntdButton('导出图片', id='export-btn')
])

@callback(
    Output('chart-screenshot', 'executeSnapshot'),
    Input('export-btn', 'nClicks'),
    prevent_initial_call=True
)
def trigger_screenshot(n):
    return True

@callback(
    Output('download', 'data'),
    Input('chart-screenshot', 'screenshotResult'),
    prevent_initial_call=True
)
def download_screenshot(result):
    if result:
        import base64
        img_data = base64.b64decode(result.split(',')[1])
        return dcc.send_bytes(img_data, 'chart.png')
    return dash.no_update
```

---

## 图表配置最佳实践

### 统一图表主题

```python
# 定义统一的图表配置
CHART_THEME = {
    'color': ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1'],
    'tooltip': {
        'showMarkers': True,
        'shared': True
    },
    'legend': {
        'position': 'top-right'
    },
    'xAxis': {
        'nice': True
    },
    'yAxis': {
        'nice': True,
        'min': 0
    }
}

# 使用
fact.AntdLine(
    data=data,
    xField='date',
    yField='value',
    **CHART_THEME
)
```

### 自适应高度

```python
fact.AntdLine(
    data=data,
    xField='date',
    yField='value',
    autoFit=True,  # 自适应容器
    height=None    # 不固定高度
)

# 容器设置高度
html.Div(
    fact.AntdLine(..., autoFit=True),
    style={'height': 300}
)
```

---

## 参考资源

- [feffery-antd-charts 官方文档](https://fact.feffery.tech/)
- [Ant Design Charts 官方文档](https://charts.ant.design/)

# dashboard

> 数据仪表盘开发专题 Skill
> Feffery 仪表盘范式：数据切换、导出、弹窗、全屏、实时更新、数据下钻

当用户需要开发数据仪表盘、大屏可视化或数据分析应用时使用。

---

## 技术栈与统一导入

```python


# 统一别名（强制）
import feffery_antd_components as fac
import feffery_antd_charts as fact
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    welcome_card, index_card, simple_chart_card, blank_card
)
```

---

## UI 与布局规范

### 基础布局

```python
# 外层容器：灰底白卡风格
html.Div(
    [...],
    style=style(
        padding=50,
        background="#f5f5f5",
        minHeight="100vh",
        boxSizing="border-box"
    )
)

# 网格系统
fac.AntdRow(
    [
        fac.AntdCol(kpi_card_1, xs=24, md=12, xl=6),
        fac.AntdCol(kpi_card_2, xs=24, md=12, xl=6),
        fac.AntdCol(chart_card_1, xs=24, xl=12),
        fac.AntdCol(chart_card_2, xs=24, xl=12),
    ],
    gutter=[18, 18]  # 水平垂直间距
)
```

### 响应式断点

| 组件类型 | xs (手机) | md (平板) | xl (桌面) |
|----------|-----------|-----------|-----------|
| KPI 卡片 | 24 | 12 | 6 |
| 小图表 | 24 | 24 | 12 |
| 大图表 | 24 | 24 | 16/24 |

---

## 全局单例组件

**必须放在根布局顶部：**

```python
app.layout = html.Div([
    # 全局消息提示
    fac.Fragment(id="message-target"),

    # 全局下载
    dcc.Download(id="global-download"),

    # 全局查看数据弹窗
    fac.AntdModal(
        id="view-data-modal",
        title="数据详情",
        width=800,
        visible=False
    ),

    # 全局全屏控制
    fuc.FefferyFullscreen(id="fullscreen-target"),

    # 全局截图导出
    fuc.FefferyDom2Image(
        id="export-dashboard-to-image",
        targetSelector="#dashboard-container",
        scale=2
    ),

    # 仪表盘内容
    html.Div(id="dashboard-container", children=[...])
])
```

---

## 回调设计原则

### 1. 使用 set_props 避免 Duplicate Output

```python
from dash import set_props

# 多个回调控制同一个全局组件时
@callback(Input('btn-1', 'nClicks'))
def handle_btn1(n):
    set_props('message-target', {
        'children': fac.AntdMessage(content='操作1成功', type='success')
    })

@callback(Input('btn-2', 'nClicks'))
def handle_btn2(n):
    set_props('message-target', {
        'children': fac.AntdMessage(content='操作2成功', type='success')
    })
```

### 2. 数据从 State 获取

```python
# 导出/查看数据时，数据从 State 取，不要作为 Input
@callback(
    Output('global-download', 'data'),
    Input('export-btn', 'nClicks'),
    State('my-chart', 'data'),  # 从 State 获取数据
    prevent_initial_call=True
)
def export_data(n, chart_data):
    df = pd.DataFrame(chart_data)
    return dcc.send_data_frame(df.to_excel, 'data.xlsx')
```

### 3. 双向同步防循环

```python
@callback(
    Output('chart', 'data'),
    Output('filter', 'value'),
    Input('chart', 'recentlyColumnClickRecord'),
    Input('filter', 'value'),
)
def sync_chart_filter(click_record, filter_value):
    trigger = ctx.triggered_id

    if trigger == 'chart':
        # 图表点击触发，更新筛选器
        new_filter = click_record['data']['category']
        return dash.no_update, new_filter
    else:
        # 筛选器触发，更新图表
        new_data = filter_data(filter_value)
        return new_data, dash.no_update
```

---

## 通用能力范式

### 1. 数据切换

```python
simple_chart_card(
    title='销售趋势',
    extra=fac.AntdRadioGroup(
        id='period-selector',
        options=[
            {'label': '日', 'value': 'day'},
            {'label': '周', 'value': 'week'},
            {'label': '月', 'value': 'month'},
        ],
        value='day',
        optionType='button',
        size='small'
    ),
    children=fact.AntdLine(id='trend-chart', data=[], xField='date', yField='value')
)

@callback(Output('trend-chart', 'data'), Input('period-selector', 'value'))
def update_trend(period):
    return get_trend_data(period)
```

### 2. 实时更新

```python
# 使用 dcc.Interval 定时刷新
dcc.Interval(id='refresh-interval', interval=5000)  # 5秒

# 使用 Patch 追加数据（高效）
@callback(
    Output('realtime-chart', 'data'),
    Input('refresh-interval', 'n_intervals'),
    State('realtime-chart', 'data')
)
def update_realtime(n, current_data):
    new_point = get_latest_data()

    patched = Patch()
    patched.append(new_point)

    # 限制数据长度
    if len(current_data) > 100:
        patched.remove(0)

    return patched

# 数字滚动动画
fuc.FefferyCountUp(
    id='kpi-value',
    start=0,
    end=12345,
    duration=1.5
)
```

### 3. 查看数据

```python
@callback(
    Input('view-data-btn', 'nClicks'),
    State('my-chart', 'data'),
    prevent_initial_call=True
)
def show_data_modal(n, data):
    df = pd.DataFrame(data)
    table = fac.AntdTable(
        columns=[{'title': col, 'dataIndex': col} for col in df.columns],
        data=df.to_dict('records'),
        pagination={'pageSize': 10}
    )
    set_props('view-data-modal', {'visible': True, 'children': table})
```

### 4. Excel 导出

```python
import io
import pandas as pd

@callback(
    Output('global-download', 'data'),
    Input('export-excel-btn', 'nClicks'),
    State('chart-1', 'data'),
    State('chart-2', 'data'),
    prevent_initial_call=True
)
def export_excel(n, data1, data2):
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        pd.DataFrame(data1).to_excel(writer, sheet_name='图表1', index=False)
        pd.DataFrame(data2).to_excel(writer, sheet_name='图表2', index=False)

    output.seek(0)
    return dcc.send_bytes(output.read(), '数据导出.xlsx')
```

### 5. 卡片全屏 (Pattern-Matching)

```python
import json
from dash import MATCH

# 卡片容器
fac.AntdCard(
    id={'type': 'chart-card', 'index': 'sales'},
    title='销售图表',
    extra=fac.AntdButton(
        icon=fac.AntdIcon(icon='antd-fullscreen'),
        id={'type': 'chart-card-toggle-fullscreen', 'index': 'sales'}
    ),
    children=[...]
)

# 全屏切换回调
@callback(
    Input({'type': 'chart-card-toggle-fullscreen', 'index': MATCH}, 'nClicks'),
    State({'type': 'chart-card-toggle-fullscreen', 'index': MATCH}, 'id'),
    prevent_initial_call=True
)
def toggle_fullscreen(n, btn_id):
    card_id = {'type': 'chart-card', 'index': btn_id['index']}
    set_props('fullscreen-target', {
        'targetId': json.dumps(card_id, separators=(',', ':')),
        'isFullscreen': True
    })
```

### 6. PDF 导出

```python
from fpdf import FPDF
import base64
from PIL import Image

@callback(
    Output('global-download', 'data'),
    Input('export-dashboard-to-image', 'screenshotResult'),
    prevent_initial_call=True
)
def export_pdf(screenshot):
    if not screenshot:
        return dash.no_update

    # base64 转图片
    img_data = base64.b64decode(screenshot.split(',')[1])
    img = Image.open(io.BytesIO(img_data))

    # 创建 PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.image(img, x=10, y=10, w=190)

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)

    return dcc.send_bytes(output.read(), '仪表盘报告.pdf')
```

### 7. 数据下钻

```python
# 图表点击触发下钻
@callback(
    Output('drill-chart', 'data'),
    Output('breadcrumb', 'items'),
    Input('drill-chart', 'recentlyColumnClickRecord'),
    Input('breadcrumb', 'clickedItem'),
    State('breadcrumb', 'items'),
)
def handle_drill(click_record, breadcrumb_click, current_items):
    trigger = ctx.triggered_id

    if trigger == 'drill-chart' and click_record:
        # 图表点击，下钻到下一级
        clicked_value = click_record['data']['category']
        new_data = get_drill_data(clicked_value)
        new_items = current_items + [{'title': clicked_value, 'key': clicked_value}]
        return new_data, new_items

    elif trigger == 'breadcrumb' and breadcrumb_click:
        # 面包屑点击，返回上级
        target_key = breadcrumb_click['itemKey']
        target_index = next(i for i, item in enumerate(current_items) if item['key'] == target_key)
        new_items = current_items[:target_index + 1]
        new_data = get_drill_data(target_key)
        return new_data, new_items

    return dash.no_update, dash.no_update
```

---

## 常用图表配置

### KPI 卡片

```python
fac.AntdStatistic(
    title='总销售额',
    value=1234567,
    prefix='¥',
    precision=2,
    valueStyle={'color': '#3f8600'}
)
```

### 折线图

```python
fact.AntdLine(
    data=data,
    xField='date',
    yField='value',
    seriesField='type',
    smooth=True,
    point={'size': 3},
    tooltip={'showMarkers': True}
)
```

### 柱状图

```python
fact.AntdColumn(
    data=data,
    xField='category',
    yField='value',
    color='#1890ff',
    label={'position': 'middle'},
    columnWidthRatio=0.6
)
```

### 饼图

```python
fact.AntdPie(
    data=data,
    angleField='value',
    colorField='type',
    radius=0.9,
    innerRadius=0.6,
    label={
        'type': 'spider',
        'content': '{name}: {percentage}'
    }
)
```

# 仪表盘数据绑定

> 仪表盘数据流和状态管理
> 数据获取、缓存、共享和更新策略

---

## 数据流架构

### 单向数据流

```
数据源 → 筛选器 → 数据处理 → 多个图表/表格
         ↑
       用户交互
```

### 推荐模式

```python
# 中心化数据存储
app.layout = html.Div([
    # 全局数据存储
    dcc.Store(id='raw-data-store'),
    dcc.Store(id='filtered-data-store'),

    # 筛选器
    filter_panel(),

    # 可视化组件
    charts_panel()
])

# 数据加载
@callback(
    Output('raw-data-store', 'data'),
    Input('url', 'pathname')  # 页面加载时触发
)
def load_raw_data(_):
    df = load_from_database()
    return df.to_dict('records')

# 数据筛选
@callback(
    Output('filtered-data-store', 'data'),
    Input('date-filter', 'value'),
    Input('category-filter', 'value'),
    State('raw-data-store', 'data')
)
def filter_data(date_range, category, raw_data):
    df = pd.DataFrame(raw_data)
    # 应用筛选...
    return df.to_dict('records')

# 图表更新（从筛选后的数据）
@callback(
    Output('chart-1', 'data'),
    Input('filtered-data-store', 'data')
)
def update_chart1(filtered_data):
    return process_for_chart1(filtered_data)
```

---

## 数据获取策略

### 初始化加载

```python
# 使用 dcc.Loading 显示加载状态
dcc.Loading(
    html.Div([
        fac.AntdRow([...])
    ]),
    type='circle'
)

# 初始化数据加载
@callback(
    Output('data-store', 'data'),
    Input('app-init', 'children'),  # 虚拟输入
    prevent_initial_call=False
)
def init_data(_):
    return fetch_initial_data()
```

### 懒加载

```python
# 标签页切换时加载
@callback(
    Output('tab-content', 'children'),
    Input('tabs', 'activeKey')
)
def load_tab_content(active_key):
    if active_key == 'overview':
        return load_overview_content()
    elif active_key == 'details':
        return load_details_content()  # 切换时才加载
    return dash.no_update
```

### 分页加载

```python
@callback(
    Output('table', 'data'),
    Output('table', 'pagination'),
    Input('table', 'pagination'),
    State('filter-store', 'data')
)
def load_page(pagination, filters):
    page = pagination['current']
    page_size = pagination['pageSize']

    # 只加载当前页数据
    data, total = fetch_page(page, page_size, filters)

    pagination['total'] = total
    return data, pagination
```

---

## 状态管理

### 使用 dcc.Store

```python
# 不同存储类型
dcc.Store(id='session-store', storage_type='session')   # 关闭标签页清除
dcc.Store(id='local-store', storage_type='local')       # 永久保存
dcc.Store(id='memory-store', storage_type='memory')     # 刷新页面清除

# 存储结构化数据
@callback(
    Output('filter-store', 'data'),
    Input('date-filter', 'value'),
    Input('category-filter', 'value'),
    Input('region-filter', 'value')
)
def save_filters(date_range, category, region):
    return {
        'date_range': date_range,
        'category': category,
        'region': region,
        'updated_at': datetime.now().isoformat()
    }
```

### 跨页面状态

```python
# 在多页面应用中共享状态
# app.py
app.layout = html.Div([
    dcc.Store(id='global-state', storage_type='session'),
    dash.page_container
])

# pages/page_a.py
@callback(
    Output('global-state', 'data'),
    Input('save-btn', 'nClicks'),
    State('form-data', 'value')
)
def save_to_global(n, data):
    return {'form_data': data}

# pages/page_b.py
@callback(
    Output('display', 'children'),
    Input('global-state', 'data')
)
def read_from_global(state):
    return f"共享数据: {state}"
```

---

## 缓存策略

### Flask-Caching

```python
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300  # 5分钟
})
cache.init_app(app.server)

@cache.memoize(timeout=60)
def expensive_query(filter_params):
    """缓存耗时查询"""
    return database.query(filter_params)

@callback(
    Output('chart', 'data'),
    Input('filters', 'value')
)
def update_chart(filters):
    # 自动使用缓存
    return expensive_query(tuple(filters.items()))
```

### 客户端缓存

```python
# 使用 Store 实现简单缓存
@callback(
    Output('data-cache', 'data'),
    Output('chart', 'data'),
    Input('refresh-btn', 'nClicks'),
    State('data-cache', 'data'),
    State('data-cache', 'modified_timestamp')
)
def smart_fetch(n, cached_data, cache_time):
    import time

    # 检查缓存是否过期（5分钟）
    if cached_data and cache_time:
        if time.time() - cache_time / 1000 < 300:
            # 使用缓存
            return dash.no_update, cached_data

    # 重新获取
    new_data = fetch_from_server()
    return new_data, new_data
```

---

## 高效更新

### 使用 Patch

```python
from dash import Patch

@callback(
    Output('table', 'data'),
    Input('add-row-btn', 'nClicks'),
    State('new-row-form', 'value'),
    prevent_initial_call=True
)
def add_row(n, new_row):
    # 高效追加，不替换整个数据
    patched = Patch()
    patched.append(new_row)
    return patched

@callback(
    Output('table', 'data'),
    Input('update-cell-trigger', 'data'),
    prevent_initial_call=True
)
def update_cell(trigger):
    row_index = trigger['row']
    field = trigger['field']
    value = trigger['value']

    # 只更新特定单元格
    patched = Patch()
    patched[row_index][field] = value
    return patched
```

### 批量更新

```python
# 多个输出一起更新
@callback(
    Output('kpi-1', 'children'),
    Output('kpi-2', 'children'),
    Output('kpi-3', 'children'),
    Output('kpi-4', 'children'),
    Output('chart-1', 'data'),
    Output('chart-2', 'data'),
    Input('refresh-interval', 'n_intervals')
)
def batch_update(n):
    # 一次查询获取所有数据
    data = fetch_all_dashboard_data()

    return (
        data['kpi_1'],
        data['kpi_2'],
        data['kpi_3'],
        data['kpi_4'],
        data['chart_1'],
        data['chart_2']
    )
```

---

## 错误处理

### 数据加载错误

```python
@callback(
    Output('chart', 'data'),
    Output('error-message', 'children'),
    Input('load-btn', 'nClicks'),
    prevent_initial_call=True
)
def load_with_error_handling(n):
    try:
        data = fetch_data()
        return data, None
    except ConnectionError:
        return dash.no_update, fac.AntdAlert(
            message='网络连接失败，请重试',
            type='error',
            showIcon=True
        )
    except Exception as e:
        return dash.no_update, fac.AntdAlert(
            message=f'数据加载失败: {str(e)}',
            type='error',
            showIcon=True
        )
```

### 数据验证

```python
@callback(
    Output('chart', 'data'),
    Input('data-store', 'data')
)
def validate_and_display(data):
    if not data:
        return []

    # 验证数据结构
    required_fields = ['date', 'value', 'category']
    if not all(field in data[0] for field in required_fields):
        raise dash.exceptions.PreventUpdate

    return data
```

---

## 性能优化

### 防抖

```python
# 输入防抖
fac.AntdInput(
    id='search-input',
    debounceWait=300  # 300ms 防抖
)

@callback(
    Output('search-results', 'children'),
    Input('search-input', 'debounceValue')  # 使用防抖值
)
def search(keyword):
    return perform_search(keyword)
```

### 条件更新

```python
@callback(
    Output('chart', 'data'),
    Input('filter', 'value'),
    State('chart', 'data')
)
def conditional_update(filter_value, current_data):
    # 只在必要时更新
    if not filter_value:
        raise dash.exceptions.PreventUpdate

    new_data = filter_data(filter_value)

    # 数据相同则不更新
    if new_data == current_data:
        raise dash.exceptions.PreventUpdate

    return new_data
```

---

## 参考资源

- [Plotly Dash 回调文档](https://dash.plotly.com/basic-callbacks)
- [feffery-antd-components 官方文档](https://fac.feffery.tech/)

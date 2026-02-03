# FAC 表格组件

> feffery-antd-components 表格类组件详解
> AntdTable 是 fac 最核心、功能最丰富的组件

---

## AntdTable 快速参考

> **AI快速参考**
> - **用途**: 展示行列数据，支持排序、筛选、分页、行选择等
> - **核心参数**: `columns`(列定义)、`data`(数据)、`pagination`(分页)、`rowSelectionType`(行选择)
> - **回调属性**: `selectedRowKeys`, `selectedRows`, `currentData`, `sorter`, `filter`
> - **快速使用**: `fac.AntdTable(columns=[{'title': '姓名', 'dataIndex': 'name'}], data=[{'name': '张三'}])`

---

## 基础结构

```python
fac.AntdTable(
    id='my-table',
    columns=[...],      # 列定义
    data=[...],         # 数据源
    pagination={...},   # 分页配置
    bordered=True,      # 边框
    size='small'        # 尺寸: 'small' | 'middle' | 'large'
)
```

---

## 列定义详解

```python
columns = [
    {
        'title': '姓名',           # 列标题
        'dataIndex': 'name',       # 数据字段名
        'key': 'name',             # 唯一标识（可选）
        'width': 120,              # 列宽
        'fixed': 'left',           # 固定列: 'left' | 'right'
        'align': 'center',         # 对齐: 'left' | 'center' | 'right'
        'ellipsis': True,          # 超长省略
        'editable': True,          # 可编辑
        'renderOptions': {...}     # 渲染配置
    }
]
```

### 完整列属性说明

| 属性 | 类型 | 说明 |
|------|------|------|
| title | string/component | 列标题 |
| dataIndex | string | 数据字段名 |
| width | number/string | 列宽 |
| minWidth | number/string | 最小列宽 |
| fixed | 'left'/'right' | 固定列 |
| align | 'left'/'center'/'right' | 内容对齐 |
| headerAlign | 'left'/'center'/'right' | 表头对齐 |
| ellipsis | bool | 超长省略 |
| hidden | bool | 隐藏列 |
| editable | bool | 可编辑 |
| editOptions | dict | 编辑选项 |
| group | string/list | 列分组 |
| renderOptions | dict | 渲染模式配置 |

---

## 列渲染模式

### 1. 按钮渲染 (button)

```python
{
    'title': '操作',
    'dataIndex': 'action',
    'renderOptions': {
        'renderType': 'button',
        'renderButtonPopConfirmProps': {
            'title': '确认删除吗？',
            'okText': '确认',
            'cancelText': '取消'
        }
    }
}

# 数据中定义按钮
data = [
    {
        'action': [
            {'content': '编辑', 'type': 'primary'},
            {'content': '删除', 'type': 'primary', 'danger': True, 'custom': {'id': 1}}
        ]
    }
]

# 回调
@callback(
    Output('result', 'children'),
    Input('table', 'nClicksButton'),
    State('table', 'recentlyButtonClickedRow'),
    State('table', 'clickedContent'),
    State('table', 'clickedCustom')
)
def handle_button(n, row, content, custom):
    return f"点击了 {content}，行数据: {row}，自定义数据: {custom}"
```

### 2. 链接渲染 (link)

```python
{
    'title': '链接',
    'dataIndex': 'link',
    'renderOptions': {
        'renderType': 'link',
        'renderLinkText': '查看详情'
    }
}

# 数据
data = [{'link': {'content': '点击', 'href': '/detail/1'}}]
```

### 3. 标签渲染 (tags)

```python
{
    'title': '状态',
    'dataIndex': 'status',
    'renderOptions': {'renderType': 'tags'}
}

# 数据
data = [
    {
        'status': [
            {'tag': '进行中', 'color': 'blue'},
            {'tag': '紧急', 'color': 'red'}
        ]
    }
]
```

### 4. 进度条渲染 (mini-progress)

```python
{
    'title': '完成度',
    'dataIndex': 'progress',
    'renderOptions': {
        'renderType': 'mini-progress',
        'progressShowPercent': True,
        'progressStrokeLinecap': 'round'
    }
}

# 数据（0-1之间的值）
data = [{'progress': 0.75}]
```

### 5. 图片渲染 (image)

```python
{
    'title': '头像',
    'dataIndex': 'avatar',
    'renderOptions': {
        'renderType': 'image',
        'renderImageHeight': 40
    }
}

# 数据
data = [{'avatar': {'src': '/assets/avatar.jpg', 'preview': True}}]
```

### 6. 状态徽章 (status-badge)

```python
{
    'title': '状态',
    'dataIndex': 'status',
    'renderOptions': {'renderType': 'status-badge'}
}

# 数据
data = [
    {'status': {'status': 'success', 'text': '已完成'}},
    {'status': {'status': 'processing', 'text': '进行中'}},
    {'status': {'status': 'error', 'text': '失败'}}
]
```

### 7. 开关渲染 (switch)

```python
{
    'title': '启用',
    'dataIndex': 'enabled',
    'renderOptions': {'renderType': 'switch'}
}

# 数据
data = [{'enabled': {'checked': True, 'checkedChildren': '开', 'unCheckedChildren': '关'}}]

# 回调
@callback(
    Output('result', 'children'),
    Input('table', 'recentlySwitchStatus'),
    State('table', 'recentlySwitchRow')
)
def handle_switch(status, row):
    return f"状态: {status}, 行: {row}"
```

### 8. 下拉选择渲染 (select)

```python
{
    'title': '类型',
    'dataIndex': 'type',
    'renderOptions': {'renderType': 'select'}
}

# 数据
data = [
    {
        'type': {
            'options': [
                {'label': '选项1', 'value': '1'},
                {'label': '选项2', 'value': '2'}
            ],
            'allowClear': True,
            'placeholder': '请选择'
        }
    }
]
```

### 9. 复选框渲染 (checkbox)

```python
{
    'title': '选择',
    'dataIndex': 'check',
    'renderOptions': {'renderType': 'checkbox'}
}

# 数据
data = [{'check': {'checked': True, 'label': '同意'}}]
```

### 10. 可编辑单元格

```python
{
    'title': '价格',
    'dataIndex': 'price',
    'editable': True,
    'editOptions': {
        'mode': 'number',  # 'default' | 'number' | 'text-area'
        'min': 0,
        'max': 10000,
        'placeholder': '请输入'
    }
}
```

---

## 交互功能

### 排序

```python
fac.AntdTable(
    columns=[...],
    data=[...],
    sortOptions={
        'sortDataIndexes': ['age', 'score'],  # 可排序的字段
        'multiple': True  # 多字段排序，'auto' 为自动组合
    }
)

# 后端排序回调
@callback(
    Output('table', 'data'),
    Input('table', 'sorter'),
    prevent_initial_call=True
)
def handle_sort(sorter):
    if sorter and sorter.get('columns'):
        columns = sorter['columns']  # 排序字段列表
        orders = sorter['orders']    # 'ascend' | 'descend'
        return sorted_data
    return original_data
```

### 筛选

```python
fac.AntdTable(
    columns=[...],
    data=[...],
    filterOptions={
        'status': {
            'filterMode': 'checkbox',  # 'checkbox' | 'keyword' | 'tree'
            'filterCustomItems': ['待处理', '进行中', '已完成'],
            'filterMultiple': True,
            'filterSearch': True
        },
        'name': {
            'filterMode': 'keyword'
        }
    }
)

# 筛选回调
@callback(
    Output('table', 'data'),
    Input('table', 'filter')
)
def handle_filter(filter_info):
    # filter_info: {'status': ['待处理', '进行中'], 'name': ['张']}
    return filtered_data
```

### 行选择

```python
fac.AntdTable(
    id='table',
    columns=[...],
    data=[...],
    rowSelectionType='checkbox',  # 'checkbox' | 'radio'
    rowSelectionWidth=50
)

@callback(
    Output('result', 'children'),
    Input('table', 'selectedRowKeys'),
    State('table', 'selectedRows')
)
def handle_selection(keys, rows):
    return f"选中 {len(keys)} 行: {rows}"
```

### 单元格点击

```python
fac.AntdTable(
    id='table',
    columns=[...],
    data=[...],
    enableCellClickListenColumns=['name', 'status']  # 启用点击监听的列
)

@callback(
    Output('result', 'children'),
    Input('table', 'nClicksCell'),
    State('table', 'recentlyCellClickColumn'),
    State('table', 'recentlyCellClickRecord')
)
def handle_cell_click(n, column, record):
    return f"点击了 {column} 列，行数据: {record}"
```

---

## 分页配置

```python
fac.AntdTable(
    columns=[...],
    data=[...],
    pagination={
        'current': 1,           # 当前页
        'pageSize': 10,         # 每页条数
        'total': 100,           # 总条数（服务端模式必填）
        'showSizeChanger': True,
        'pageSizeOptions': [10, 20, 50, 100],
        'showQuickJumper': True,
        'showTotal': True,
        'position': 'bottomRight',
        'hideOnSinglePage': False
    }
)
```

### 服务端分页

```python
fac.AntdTable(
    id='table',
    columns=[...],
    mode='server-side',
    pagination={
        'current': 1,
        'pageSize': 10,
        'total': 100
    }
)

@callback(
    Output('table', 'data'),
    Output('table', 'pagination'),
    Input('table', 'pagination')
)
def paginate(pagination):
    page = pagination['current']
    page_size = pagination['pageSize']

    # 从数据库获取分页数据
    data, total = fetch_page_data(page, page_size)

    return data, {**pagination, 'total': total}
```

---

## 高级功能

### 列分组

```python
columns = [
    {
        'title': '基本信息',
        'group': '基本信息',
        'dataIndex': 'name'
    },
    {
        'title': '年龄',
        'group': '基本信息',
        'dataIndex': 'age'
    },
    {
        'title': '电话',
        'dataIndex': 'phone'
    }
]

# 或使用多级分组
columns = [
    {
        'title': '字段1-1',
        'dataIndex': 'field1_1',
        'group': ['组1', '子组1']
    }
]
```

### 行展开

```python
fac.AntdTable(
    id='table',
    columns=[...],
    data=[
        {'key': 'row_1', ...},
        {'key': 'row_2', ...}
    ],
    expandedRowKeyToContent=[
        {'key': 'row_1', 'content': fac.AntdDescriptions(...)},
        {'key': 'row_2', 'content': html.Div('详细信息...')}
    ],
    expandRowByClick=True,
    defaultExpandedRowKeys=['row_1']
)
```

### 固定表头和列

```python
fac.AntdTable(
    columns=[
        {'title': 'ID', 'dataIndex': 'id', 'fixed': 'left', 'width': 80},
        # 中间列...
        {'title': '操作', 'dataIndex': 'action', 'fixed': 'right', 'width': 120}
    ],
    data=[...],
    maxHeight=400,  # 固定表头
    maxWidth=1200   # 横向滚动
)
```

### 合计行

```python
fac.AntdTable(
    columns=[...],
    data=[...],
    summaryRowContents=[
        {'content': '合计', 'colSpan': 2},
        {'content': '￥12,345.00'},
        {'content': '100 件'}
    ],
    summaryRowFixed=True
)
```

### 条件样式

```python
fac.AntdTable(
    columns=[...],
    data=[...],
    conditionalStyleFuncs={
        # 行样式
        'row': '''(record, index) => {
            if (record.status === 'error') {
                return {backgroundColor: '#fff1f0'};
            }
            return {};
        }''',
        # 单元格样式（按字段）
        'age': '''(record, index) => {
            if (record.age > 30) {
                return {color: 'red', fontWeight: 'bold'};
            }
            return {};
        }'''
    }
)
```

### 虚拟滚动

```python
fac.AntdTable(
    id='large-table',
    columns=[...],
    data=large_data,  # 大数据量
    virtual=True,
    maxHeight=600
)
```

### 嵌套数据

```python
data = [
    {
        'key': 'row-1',
        'name': '父节点1',
        'children': [
            {'key': 'row-1-1', 'name': '子节点1-1'},
            {'key': 'row-1-2', 'name': '子节点1-2'}
        ]
    }
]
```

---

## 关键回调属性速查

| 属性 | 说明 |
|------|------|
| `selectedRowKeys` | 选中行的 key 列表 |
| `selectedRows` | 选中行的完整数据 |
| `currentData` | 当前表格数据（含编辑后的更新） |
| `sorter` | 排序信息 {columns, orders} |
| `filter` | 筛选信息 {字段: 筛选值列表} |
| `pagination` | 分页信息 {current, pageSize, total} |
| `recentlyChangedRow` | 最近编辑的行数据 |
| `recentlyChangedColumn` | 最近编辑的列名 |
| `nClicksButton` | 按钮点击次数 |
| `recentlyButtonClickedRow` | 最近点击按钮所在行 |
| `clickedContent` | 点击的按钮内容 |
| `clickedCustom` | 点击按钮的自定义数据 |
| `recentlySwitchStatus` | 开关切换状态 |
| `recentlySwitchRow` | 开关切换所在行 |
| `expandedRowKeys` | 当前展开的行 key 列表 |

---

## 常用示例

### 完整 CRUD 表格

```python
fac.AntdTable(
    id='crud-table',
    columns=[
        {'title': 'ID', 'dataIndex': 'id', 'width': 60},
        {'title': '名称', 'dataIndex': 'name', 'editable': True},
        {'title': '状态', 'dataIndex': 'status', 'renderOptions': {'renderType': 'tags'}},
        {
            'title': '操作',
            'dataIndex': 'actions',
            'renderOptions': {
                'renderType': 'button',
                'renderButtonPopConfirmProps': {'title': '确认删除？'}
            }
        }
    ],
    data=[
        {
            'key': '1',
            'id': 1,
            'name': '项目A',
            'status': [{'tag': '进行中', 'color': 'blue'}],
            'actions': [
                {'content': '编辑', 'type': 'link'},
                {'content': '删除', 'type': 'link', 'danger': True}
            ]
        }
    ],
    rowSelectionType='checkbox',
    pagination={'pageSize': 10, 'showSizeChanger': True},
    bordered=True
)
```

---

## 参考资源

- [feffery-antd-components 官方文档](https://fac.feffery.tech/)
- [Ant Design Table 官方文档](https://ant.design/components/table-cn)

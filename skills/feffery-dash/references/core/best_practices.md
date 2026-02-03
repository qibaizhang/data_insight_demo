# Feffery-Dash 最佳实践

> 性能优化、错误处理、开发技巧

---

## 1. 性能优化

### 1.1 大数据表格：服务端模式

```python
# 大数据量时必须使用服务端模式
fac.AntdTable(
    id='big-table',
    columns=columns,
    data=[],  # 初始为空
    mode='server-side',  # 关键！
    pagination={
        'current': 1,
        'pageSize': 20,
        'total': 0,
        'showSizeChanger': True,
        'showQuickJumper': True,
    }
)

@app.callback(
    Output('big-table', 'data'),
    Output('big-table', 'pagination'),
    Input('big-table', 'pagination'),
    Input('big-table', 'sorter'),
    Input('big-table', 'filter'),
)
def update_table(pagination, sorter, filter_info):
    page = pagination['current']
    page_size = pagination['pageSize']

    # 数据库分页查询
    data, total = query_database(page, page_size, sorter, filter_info)

    return data, {**pagination, 'total': total}
```

### 1.2 防抖/节流

```python
import feffery_utils_components as fuc

# 输入防抖
fuc.FefferyDebounceProp(
    fac.AntdInput(id='search-input', placeholder='搜索'),
    id='debounced-search',
    propName='value',
    delay=500  # 500ms 防抖
)

# 窗口尺寸节流
fuc.FefferyThrottleProp(
    fuc.FefferyWindowSize(id='window-size-raw'),
    id='throttled-window',
    propName='width',
    interval=200  # 200ms 节流
)
```

### 1.3 懒加载

```python
# 懒加载重组件
fuc.FefferyLazyLoad(
    fac.AntdTable(...),  # 复杂表格
    height=400,
    once=True  # 只加载一次
)

# 虚拟列表
fuc.FefferyVirtualList(
    id='virtual-list',
    items=[{'content': f'项目{i}'} for i in range(10000)],
    itemHeight=50,
    height=400
)
```

### 1.4 高频交互用客户端回调

```python
# 适合：拖拽、动画、纯 UI 交互
app.clientside_callback(
    """
    function(n_clicks) {
        return !window.dash_clientside.callback_context.states['drawer.visible'];
    }
    """,
    Output('drawer', 'visible'),
    Input('toggle-btn', 'nClicks'),
    State('drawer', 'visible'),
    prevent_initial_call=True
)
```

### 1.5 Patch 局部更新

```python
from dash import Patch

# 添加项目时不传输全量数据
@app.callback(
    Output('list', 'children'),
    Input('add-btn', 'nClicks'),
)
def add_item(n):
    p = Patch()
    p.append(html.Div(f'新项目 {n}'))
    return p  # 只传输增量
```

---

## 2. 错误处理

### 2.1 全局错误处理

```python
import traceback
from dash import set_props

def global_error_handler(err):
    """全局错误处理器"""
    error_msg = str(err)
    print(f'回调错误: {traceback.format_exc()}')

    # 弹出错误提示
    set_props('global-message', {
        'children': fac.AntdMessage(
            content=f'操作失败: {error_msg}',
            type='error'
        )
    })

    return no_update

app = dash.Dash(__name__, on_error=global_error_handler)

# 在布局中添加消息容器
app.layout = html.Div([
    html.Div(id='global-message'),
    # ... 其他内容
])
```

### 2.2 局部错误处理

```python
def handle_db_error(err):
    """数据库操作错误处理"""
    if 'connection' in str(err).lower():
        return '数据库连接失败，请稍后重试'
    return f'数据操作失败: {err}'

@app.callback(
    Output('result', 'children'),
    Input('save-btn', 'nClicks'),
    on_error=handle_db_error
)
def save_data(n):
    # 可能抛出数据库异常
    db.save(data)
    return '保存成功'
```

### 2.3 空值保护

```python
@app.callback(...)
def callback(value, data):
    # 始终检查 None
    if value is None:
        return no_update

    # 安全的字典访问
    result = data.get('key', '默认值') if data else '默认值'

    # 列表安全访问
    items = data or []
    return process(items)
```

---

## 3. 组件使用技巧

### 3.1 Modal/Tabs 中的组件

```python
# 问题：Modal 未渲染时，内部组件 ID 不存在
# 解决：使用 forceRender
fac.AntdModal(
    fac.AntdForm(id='modal-form', ...),
    id='my-modal',
    forceRender=True  # 关键！
)

fac.AntdTabs(
    items=[
        {'key': '1', 'label': '标签1', 'children': 组件1, 'forceRender': True},
        {'key': '2', 'label': '标签2', 'children': 组件2, 'forceRender': True},
    ]
)
```

### 3.2 表单验证

```python
@app.callback(
    Output('username-item', 'validateStatus'),
    Output('username-item', 'help'),
    Output('submit-btn', 'disabled'),
    Input('username', 'value'),
)
def validate_username(value):
    if not value:
        return 'error', '用户名不能为空', True
    if len(value) < 3:
        return 'error', '用户名至少3个字符', True
    if not value.isalnum():
        return 'error', '只能包含字母和数字', True
    return 'success', None, False
```

### 3.3 动态组件 ID

```python
# 启用动态组件支持
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# 使用 allow_optional 处理可能不存在的组件
@app.callback(
    Output('dynamic-output', 'children'),
    Input('dynamic-input', 'value'),
    allow_optional=True  # 组件可能不存在
)
def handle_dynamic(value):
    if value is None:  # 组件不存在时为 None
        return no_update
    return process(value)
```

---

## 4. 数据处理

### 4.1 dcc.Store 客户端缓存

```python
app.layout = html.Div([
    # memory: 页面刷新清除
    # local: 持久化到 localStorage
    # session: 持久化到 sessionStorage
    dcc.Store(id='data-store', storage_type='memory'),
    ...
])

# 写入
@app.callback(Output('data-store', 'data'), Input(...))
def save_data(...):
    return {'key': 'value'}  # 必须 JSON 可序列化

# 读取
@app.callback(Output(...), Input('data-store', 'data'))
def use_data(stored):
    if stored:
        return stored.get('key')
```

### 4.2 datetime 处理

```python
# 数据库 datetime 返回前端时转字符串
@app.callback(Output('table', 'data'), Input(...))
def get_data(...):
    records = db.query()
    return [
        {
            **record,
            'created_at': record['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        }
        for record in records
    ]
```

### 4.3 大文件上传

```python
# 分片上传大文件
fuc.FefferyUploadChunks(
    id='chunk-upload',
    chunkSize=1024 * 1024 * 2,  # 2MB 分片
    apiUrl='/upload-chunk',     # 后端接口
)
```

---

## 5. 安全实践

### 5.1 生产环境配置

```python
# 禁用调试
app.run(debug=False)

# 使用环境变量
import os
app.server.secret_key = os.getenv('SECRET_KEY', 'fallback-key')

# 禁用开发者工具（可选）
# pip install dash-disable-devtool-plugin
```

### 5.2 敏感数据处理

```python
# 不要在回调中暴露敏感信息
@app.callback(...)
def login(username, password):
    if authenticate(username, password):
        return '登录成功'  # ✅
    return '用户名或密码错误'  # ✅ 不要说明具体哪个错误

# 不要在前端存储敏感数据
dcc.Store(id='user-data', data={
    'username': 'user',     # ✅
    # 'password': 'xxx',    # ❌ 绝对不要
    'role': 'admin',        # ✅
})
```

---

## 6. 调试技巧

### 6.1 浏览器开发工具

```python
# 开发模式下启用热重载
app.run(debug=True, dev_tools_hot_reload=True)
```

**浏览器端 API（控制台可用）：**

```javascript
// 获取组件的完整 props 与状态
dash_component_api.getLayout('component-id')
// 返回: {id: 'component-id', children: [...], ...}

// 将字典 ID 序列化为 DOM ID 字符串（用于 document.getElementById 等）
dash_component_api.stringifyId({type: 'btn', index: 0})
// 返回: '{"type":"btn","index":0}'

// 在 clientside_callback 中使用
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    myNamespace: {
        getComponentProps: function(componentId) {
            return dash_component_api.getLayout(componentId);
        }
    }
});
```

### 6.2 回调调试

```python
@app.callback(...)
def debug_callback(*args):
    print(f'触发源: {ctx.triggered_id}')
    print(f'所有输入: {ctx.inputs}')
    print(f'所有状态: {ctx.states}')

    # 断点调试
    import pdb; pdb.set_trace()

    return result
```

### 6.3 性能监控

```python
# pip install dash-performance-monitor-plugin
# 仅开发环境使用
if __name__ == '__main__':
    app.run(debug=True)
```

---

## 7. 代码组织

### 7.1 避免循环引用

```python
# ❌ 错误：在 app.py 中定义回调，又在回调文件中导入 app
# app.py
from callbacks import page1_c  # 导入回调

# callbacks/page1_c.py
from app import app  # 循环引用！

# ✅ 正确：使用 server.py 分离实例
# server.py
app = dash.Dash(__name__)

# app.py
from server import app
import callbacks.page1_c  # 只是导入触发注册

# callbacks/page1_c.py
from server import app  # 从 server 导入
```

### 7.2 回调注册

```python
# callbacks/__init__.py
# 通过导入触发所有回调注册
from . import page1_c
from . import page2_c
from . import common_c

# app.py
import callbacks  # 一行导入所有回调
```

### 7.3 公共组件

```python
# components/cards.py
def stat_card(title, value, icon=None):
    """统计卡片组件"""
    return fac.AntdCard(
        fac.AntdStatistic(title=title, value=value, prefix=icon),
        style={'borderRadius': 8}
    )

# 使用
from components.cards import stat_card
stat_card('销售额', 126560, icon='💰')
```

---

## 8. 部署检查清单

- [ ] `debug=False`
- [ ] 配置 `SECRET_KEY`
- [ ] 数据库连接池配置
- [ ] 静态资源 CDN
- [ ] 错误日志配置
- [ ] 健康检查接口
- [ ] 进程管理 (systemd/supervisor)
- [ ] 反向代理 (nginx)
- [ ] HTTPS 配置
- [ ] 备份策略

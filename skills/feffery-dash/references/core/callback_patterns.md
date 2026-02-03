# Feffery-Dash 回调模式大全

> 覆盖所有常用回调场景和最佳实践

---

## 1. 基础回调

### 1.1 标准回调结构

```python
from dash import Input, Output, State
from server import app

@app.callback(
    Output('output-id', 'children'),      # 输出
    Input('input-id', 'nClicks'),          # 触发输入
    State('state-id', 'value'),            # 状态（不触发）
    prevent_initial_call=True              # 阻止初始调用
)
def callback_function(n_clicks, state_value):
    return f'结果: {n_clicks}'
```

### 1.2 Input vs State

| 角色 | 作用 | 触发回调 |
|------|------|----------|
| **Input** | 提供数据 + 触发 | ✅ |
| **State** | 仅提供数据 | ❌ |

```python
# 典型场景：表单提交
@app.callback(
    Output('result', 'children'),
    Input('submit-btn', 'nClicks'),   # 点击触发
    State('input-field', 'value'),    # 读取但不触发
    prevent_initial_call=True
)
def submit_form(n_clicks, input_value):
    return f'提交: {input_value}'
```

---

## 2. 多输入/输出

### 2.1 多 Input

```python
@app.callback(
    Output('result', 'children'),
    Input('btn1', 'nClicks'),
    Input('btn2', 'nClicks'),
    Input('dropdown', 'value'),
)
def handle_multiple(n1, n2, dropdown_val):
    # 参数顺序与 Input 声明顺序一致
    return f'btn1: {n1}, btn2: {n2}, dropdown: {dropdown_val}'
```

### 2.2 多 Output

```python
@app.callback(
    Output('out1', 'children'),
    Output('out2', 'style'),
    Output('out3', 'disabled'),
    Input('btn', 'nClicks')
)
def multi_output(n):
    # 必须返回列表，长度与 Output 数量一致
    return [
        f'文本输出',
        {'color': 'red'},
        True
    ]
```

### 2.3 字典化写法（推荐复杂场景）

```python
@app.callback(
    output=dict(
        text=Output('out1', 'children'),
        style=Output('out2', 'style'),
    ),
    inputs=dict(
        clicks=Input('btn', 'nClicks'),
        value=Input('input', 'value'),
    ),
    state=dict(
        extra=State('extra', 'data'),
    )
)
def dict_callback(clicks, value, extra):
    return dict(
        text=f'点击 {clicks} 次',
        style={'color': 'blue'}
    )
```

---

## 3. 触发源判断 (ctx)

### 3.1 判断哪个 Input 触发

```python
from dash import ctx

@app.callback(
    Output('result', 'children'),
    Input('btn1', 'nClicks'),
    Input('btn2', 'nClicks'),
    prevent_initial_call=True
)
def handle_trigger(n1, n2):
    trigger_id = ctx.triggered_id

    if trigger_id == 'btn1':
        return '按钮1触发'
    elif trigger_id == 'btn2':
        return '按钮2触发'

    return no_update
```

### 3.2 ctx 常用属性

```python
ctx.triggered_id      # 触发组件的 ID
ctx.triggered         # 触发详情列表
ctx.inputs            # 所有 Input 值
ctx.states            # 所有 State 值
ctx.outputs_grouping  # Output 分组信息
```

---

## 4. 阻止更新

### 4.1 no_update（局部取消）

```python
from dash import no_update

@app.callback(
    Output('out1', 'children'),
    Output('out2', 'children'),
    Input('btn', 'nClicks')
)
def partial_update(n):
    if n % 2 == 0:
        return ['更新out1', no_update]  # out2 不更新
    return [no_update, '更新out2']      # out1 不更新
```

### 4.2 PreventUpdate（完全阻断）

```python
from dash.exceptions import PreventUpdate

@app.callback(...)
def callback(value):
    if value is None:
        raise PreventUpdate  # 完全不执行任何更新
    return process(value)
```

---

## 5. 高级更新模式

### 5.1 Patch 局部更新

```python
from dash import Patch

@app.callback(
    Output('items-list', 'children'),
    Input('add-btn', 'nClicks'),
    prevent_initial_call=True
)
def add_item(n):
    p = Patch()
    p.append(html.Div(f'新项目 {n}'))  # 追加到末尾
    return p
```

**Patch 支持的操作：**

```python
p.append(value)        # 末尾追加
p.prepend(value)       # 头部插入
p.insert(idx, value)   # 指定位置插入
p.extend(list)         # 批量追加
p.remove(value)        # 删除元素
p.clear()              # 清空
p[idx] = value         # 修改指定索引
p['key'] = value       # 修改字典键值
del p[idx]             # 删除指定索引
```

### 5.2 set_props 副作用更新

```python
from dash import set_props

@app.callback(
    Output('result', 'children'),
    Input('submit-btn', 'nClicks'),
    prevent_initial_call=True
)
def submit_data(n):
    result = process_data()

    # 副作用：弹出消息（无需在 Output 中声明）
    set_props('message-container', {
        'children': fac.AntdMessage(content='成功', type='success')
    })

    return result
```

---

## 6. 模式匹配回调

### 6.1 ALL 模式（批量收集）

```python
from dash.dependencies import ALL

# 布局：动态生成按钮
buttons = [
    fac.AntdButton(f'按钮{i}', id={'type': 'btn', 'index': i})
    for i in range(10)
]

# 回调：收集所有按钮的点击数
@app.callback(
    Output('output', 'children'),
    Input({'type': 'btn', 'index': ALL}, 'nClicks'),
    prevent_initial_call=True
)
def sum_clicks(n_clicks_list):
    # n_clicks_list 是列表
    total = sum(n for n in n_clicks_list if n)
    return f'总点击: {total}'
```

### 6.2 MATCH 模式（一对一）

```python
from dash.dependencies import MATCH

# 布局：每个按钮对应一个输出
items = [
    html.Div([
        fac.AntdButton(f'按钮{i}', id={'type': 'btn', 'index': i}),
        html.Span(id={'type': 'output', 'index': i})
    ])
    for i in range(10)
]

# 回调：只更新被点击按钮对应的输出
@app.callback(
    Output({'type': 'output', 'index': MATCH}, 'children'),
    Input({'type': 'btn', 'index': MATCH}, 'nClicks'),
    prevent_initial_call=True
)
def update_single(n):
    # n 是单个值，不是列表
    return f'点击 {n} 次'
```

### 6.3 ALLSMALLER 模式

```python
from dash.dependencies import ALLSMALLER

# 收集 index 小于当前的所有值
@app.callback(
    Output({'type': 'sum', 'index': MATCH}, 'children'),
    Input({'type': 'input', 'index': ALLSMALLER}, 'value'),
    Input({'type': 'input', 'index': MATCH}, 'value'),
)
def cumulative_sum(previous_values, current):
    # previous_values 是 index 小于当前的所有值
    total = sum(previous_values) + (current or 0)
    return f'累计: {total}'
```

---

## 7. 运行状态管理

### 7.1 running 参数

```python
@app.callback(
    Output('result', 'children'),
    Input('execute-btn', 'nClicks'),
    running=[
        # (Output, 运行时的值, 结束后的值)
        (Output('execute-btn', 'loading'), True, False),
        (Output('execute-btn', 'disabled'), True, False),
        (Output('execute-btn', 'children'), '执行中...', '执行'),
    ],
    prevent_initial_call=True
)
def long_task(n):
    import time
    time.sleep(3)  # 模拟耗时
    return f'完成，第 {n} 次'
```

### 7.2 progress 进度回调

```python
@app.callback(
    Output('result', 'children'),
    Input('start-btn', 'nClicks'),
    progress=[Output('progress-bar', 'percent')],
    prevent_initial_call=True
)
def task_with_progress(set_progress, n):
    for i in range(10):
        time.sleep(0.5)
        set_progress((i + 1) * 10)  # 更新进度
    return '任务完成'
```

---

## 8. 重复 Output

### 8.1 allow_duplicate

```python
# 多个回调更新同一个 Output
@app.callback(
    Output('shared', 'children', allow_duplicate=True),
    Input('btn1', 'nClicks'),
    prevent_initial_call=True  # 必须设置
)
def callback1(n):
    return f'按钮1: {n}'

@app.callback(
    Output('shared', 'children', allow_duplicate=True),
    Input('btn2', 'nClicks'),
    prevent_initial_call=True  # 必须设置
)
def callback2(n):
    return f'按钮2: {n}'
```

---

## 9. 浏览器端回调

### 9.1 内联 JavaScript

```python
app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            return true;
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('drawer', 'visible'),
    Input('open-btn', 'nClicks'),
    prevent_initial_call=True
)
```

### 9.2 外部 JS 文件

```javascript
// assets/callbacks.js
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    myNamespace: {
        openDrawer: function(n_clicks) {
            return n_clicks ? true : window.dash_clientside.no_update;
        },

        scrollToTop: function(n_clicks) {
            window.scrollTo({top: 0, behavior: 'smooth'});
            return window.dash_clientside.no_update;
        }
    }
});
```

```python
from dash.dependencies import ClientsideFunction

app.clientside_callback(
    ClientsideFunction(namespace='myNamespace', function_name='openDrawer'),
    Output('drawer', 'visible'),
    Input('open-btn', 'nClicks'),
    prevent_initial_call=True
)
```

### 9.3 set_props（客户端）

```javascript
// 在浏览器端直接更新组件
window.dash_clientside.set_props('component-id', {
    children: '新内容',
    style: {color: 'red'}
});
```

---

## 10. 无 Output 回调

```python
# 纯副作用，不更新任何组件
@app.callback(
    Input('log-btn', 'nClicks'),
    prevent_initial_call=True
)
def log_only(n):
    print(f'按钮点击: {n}')
    # 写入日志、发送邮件等
    # 不需要 return
```

---

## 11. 异步回调

```python
# 安装: pip install "dash[async]"

import asyncio

@app.callback(
    Output('result', 'children'),
    Input('btn', 'nClicks'),
    prevent_initial_call=True
)
async def async_callback(n):
    # 并行执行多个异步任务
    result1, result2 = await asyncio.gather(
        fetch_data1(),
        fetch_data2()
    )
    return f'{result1} + {result2}'
```

---

## 12. 错误处理

### 12.1 全局错误处理

```python
def global_error_handler(err):
    import traceback
    print(f'回调错误: {traceback.format_exc()}')
    return fac.AntdMessage(content='系统错误', type='error')

app = dash.Dash(__name__, on_error=global_error_handler)
```

### 12.2 局部错误处理

```python
def local_handler(err):
    return f'错误: {str(err)}'

@app.callback(
    Output('result', 'children'),
    Input('btn', 'nClicks'),
    on_error=local_handler
)
def risky_callback(n):
    # 可能抛出异常的代码
    pass
```

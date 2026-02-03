# FAC 反馈组件

> feffery-antd-components 反馈类组件详解
> 弹窗、抽屉、消息、通知、加载等用户交互反馈

---

## 反馈组件概览

| 组件 | 说明 | 适用场景 |
|------|------|----------|
| AntdModal | 模态框 | 确认、表单、详情 |
| AntdDrawer | 抽屉 | 侧边表单、详情 |
| AntdMessage | 全局消息 | 操作反馈 |
| AntdNotification | 通知提醒 | 系统通知 |
| AntdPopconfirm | 气泡确认 | 轻量确认 |
| AntdAlert | 警告提示 | 页面提示信息 |
| AntdSpin | 加载中 | 数据加载 |
| AntdSkeleton | 骨架屏 | 内容加载占位 |
| AntdProgress | 进度条 | 进度展示 |
| AntdResult | 结果页 | 操作结果 |

---

## 模态框 Modal

### 基础弹窗

```python
fac.AntdModal(
    id='my-modal',
    title='提示',
    children='确定要执行此操作吗？',
    visible=False,
    okText='确定',
    cancelText='取消',
    width=520
)

# 控制显示/隐藏
@callback(
    Output('my-modal', 'visible'),
    Input('open-btn', 'nClicks'),
    Input('my-modal', 'okCounts'),
    Input('my-modal', 'cancelCounts'),
    prevent_initial_call=True
)
def toggle_modal(open_click, ok, cancel):
    trigger = ctx.triggered_id
    if trigger == 'open-btn':
        return True
    return False
```

### 确认弹窗

```python
fac.AntdModal(
    id='confirm-modal',
    title='确认删除',
    children=[
        fac.AntdIcon(icon='antd-exclamation-circle', style={'color': '#faad14', 'marginRight': 8}),
        '此操作不可恢复，是否继续？'
    ],
    visible=False,
    okButtonProps={'danger': True},
    okText='删除',
    cancelText='取消'
)
```

### 表单弹窗

```python
fac.AntdModal(
    id='form-modal',
    title='新建用户',
    children=[
        fac.AntdForm(
            [
                fac.AntdFormItem(fac.AntdInput(id='modal-username'), label='用户名'),
                fac.AntdFormItem(fac.AntdInput(id='modal-email'), label='邮箱'),
            ],
            labelCol={'span': 6},
            wrapperCol={'span': 18}
        )
    ],
    visible=False,
    width=600,
    maskClosable=False  # 点击蒙层不关闭
)
```

### 全屏弹窗

```python
fac.AntdModal(
    id='fullscreen-modal',
    title='详情查看',
    children=[...],
    visible=False,
    width='100vw',
    style={'top': 0, 'paddingBottom': 0},
    bodyStyle={'height': 'calc(100vh - 110px)', 'overflow': 'auto'}
)
```

---

## 抽屉 Drawer

### 基础抽屉

```python
fac.AntdDrawer(
    id='my-drawer',
    title='详情',
    children=[...],
    visible=False,
    width=400,
    placement='right'  # 'right' | 'left' | 'top' | 'bottom'
)
```

### 多层抽屉

```python
fac.AntdDrawer(
    id='parent-drawer',
    title='一级抽屉',
    children=[
        html.Div('内容...'),
        fac.AntdButton('打开二级', id='open-child-drawer'),

        fac.AntdDrawer(
            id='child-drawer',
            title='二级抽屉',
            children='二级内容...',
            visible=False,
            width=350
        )
    ],
    visible=False,
    width=500
)
```

### 表单抽屉

```python
fac.AntdDrawer(
    id='form-drawer',
    title='编辑用户',
    children=[
        fac.AntdForm([...]),
    ],
    extra=fac.AntdSpace([
        fac.AntdButton('取消', id='drawer-cancel'),
        fac.AntdButton('保存', id='drawer-save', type='primary')
    ]),
    visible=False,
    width=600,
    maskClosable=False
)
```

---

## 全局消息 Message

### 使用 set_props 避免重复输出

```python
from dash import set_props

# 布局中放置消息容器
fac.Fragment(id='message-container')

# 触发消息
@callback(
    Input('save-btn', 'nClicks'),
    prevent_initial_call=True
)
def show_message(n):
    # 处理业务逻辑...
    set_props('message-container', {
        'children': fac.AntdMessage(
            content='保存成功',
            type='success'  # 'success' | 'error' | 'info' | 'warning'
        )
    })
```

### 消息类型

```python
# 成功
fac.AntdMessage(content='操作成功', type='success')

# 错误
fac.AntdMessage(content='操作失败', type='error')

# 警告
fac.AntdMessage(content='请注意', type='warning')

# 信息
fac.AntdMessage(content='提示信息', type='info')

# 加载中
fac.AntdMessage(content='处理中...', type='loading')
```

### 配置选项

```python
fac.AntdMessage(
    content='自定义消息',
    type='success',
    duration=3,         # 显示时长（秒），0 表示不自动关闭
    maxCount=3,         # 最大显示数量
    top=100             # 距离顶部距离
)
```

---

## 通知提醒 Notification

```python
fac.Fragment(id='notification-container')

@callback(
    Input('notify-btn', 'nClicks'),
    prevent_initial_call=True
)
def show_notification(n):
    set_props('notification-container', {
        'children': fac.AntdNotification(
            message='通知标题',
            description='这是通知的详细内容，可以包含更多信息。',
            type='info',  # 'success' | 'error' | 'info' | 'warning'
            placement='topRight',  # 位置
            duration=4.5
        )
    })
```

---

## 气泡确认 Popconfirm

```python
fac.AntdPopconfirm(
    fac.AntdButton('删除', danger=True),
    id='delete-confirm',
    title='确定删除吗？',
    description='此操作不可恢复',
    okText='确定',
    cancelText='取消'
)

@callback(
    Output('result', 'children'),
    Input('delete-confirm', 'confirmCounts'),
    prevent_initial_call=True
)
def handle_delete(n):
    # 执行删除
    return '已删除'
```

---

## 警告提示 Alert

```python
# 基础用法
fac.AntdAlert(message='提示信息', type='info')

# 带描述
fac.AntdAlert(
    message='警告',
    description='请检查您的输入是否正确',
    type='warning',
    showIcon=True,
    closable=True
)

# 横幅模式
fac.AntdAlert(
    message='系统维护通知',
    description='系统将于今晚 22:00 进行维护升级',
    type='info',
    banner=True
)
```

---

## 加载中 Spin

### 包裹内容

```python
fac.AntdSpin(
    html.Div(id='content-area'),
    id='loading-spin',
    spinning=False,
    tip='加载中...'
)

@callback(
    Output('loading-spin', 'spinning'),
    Output('content-area', 'children'),
    Input('load-btn', 'nClicks'),
    prevent_initial_call=True,
    running=[(Output('loading-spin', 'spinning'), True, False)]
)
def load_content(n):
    import time
    time.sleep(2)  # 模拟加载
    return False, '加载完成的内容'
```

### 独立使用

```python
fac.AntdSpin(
    size='large',  # 'small' | 'default' | 'large'
    indicator=fac.AntdIcon(icon='antd-loading', spin=True)
)
```

---

## 骨架屏 Skeleton

```python
fac.AntdSkeleton(
    id='skeleton',
    loading=True,
    children=[
        # 实际内容
        html.Div(id='actual-content')
    ],
    avatar=True,      # 显示头像占位
    paragraph={'rows': 4}  # 段落行数
)
```

---

## 进度条 Progress

### 线形进度条

```python
fac.AntdProgress(
    id='line-progress',
    percent=30,
    status='active',  # 'success' | 'exception' | 'active' | 'normal'
    strokeColor='#1890ff'
)
```

### 环形进度条

```python
fac.AntdProgress(
    id='circle-progress',
    percent=75,
    type='circle',
    width=120
)
```

### 仪表盘进度条

```python
fac.AntdProgress(
    id='dashboard-progress',
    percent=80,
    type='dashboard',
    gapDegree=30
)
```

### 动态更新

```python
dcc.Interval(id='progress-interval', interval=100)

@callback(
    Output('my-progress', 'percent'),
    Input('progress-interval', 'n_intervals'),
    State('my-progress', 'percent')
)
def update_progress(n, current):
    if current >= 100:
        return 100
    return current + 1
```

---

## 结果页 Result

```python
# 成功结果
fac.AntdResult(
    status='success',
    title='提交成功',
    subTitle='您的订单已提交，预计 3 天内送达',
    extra=[
        fac.AntdButton('返回首页', type='primary'),
        fac.AntdButton('查看订单')
    ]
)

# 错误结果
fac.AntdResult(
    status='error',
    title='提交失败',
    subTitle='请检查网络连接后重试',
    extra=fac.AntdButton('重试', type='primary')
)

# 自定义图标
fac.AntdResult(
    icon=fac.AntdIcon(icon='antd-smile', style={'color': '#1890ff', 'fontSize': 72}),
    title='欢迎使用',
    subTitle='开始您的体验之旅'
)
```

---

## 最佳实践

### 1. 统一消息处理

```python
# 全局消息容器
app.layout = html.Div([
    fac.Fragment(id='global-message'),
    fac.Fragment(id='global-notification'),
    # 页面内容
])

# 工具函数
def show_success(message):
    set_props('global-message', {
        'children': fac.AntdMessage(content=message, type='success')
    })

def show_error(message):
    set_props('global-message', {
        'children': fac.AntdMessage(content=message, type='error')
    })
```

### 2. 确认后操作

```python
@callback(
    Output('delete-confirm', 'visible'),
    Input('delete-btn', 'nClicks'),
    prevent_initial_call=True
)
def show_confirm(n):
    return True

@callback(
    Input('delete-confirm', 'confirmCounts'),
    prevent_initial_call=True
)
def do_delete(n):
    # 执行删除
    show_success('删除成功')
```

---

## 参考资源

- [feffery-antd-components 官方文档](https://fac.feffery.tech/)
- [Ant Design Feedback 官方文档](https://ant.design/components/message-cn)

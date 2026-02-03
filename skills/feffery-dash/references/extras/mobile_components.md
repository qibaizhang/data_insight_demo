# 移动端组件

> feffery-antd-mobile-components (famc) - 移动端组件库完整指南
> 基于 Ant Design Mobile 的 57 个专业移动端组件

---

## 组件库概述

**feffery-antd-mobile-components**（简称 `famc`）是基于 [Ant Design Mobile 5.x](https://mobile.ant.design/) 的 Plotly Dash 组件库，专为构建现代化移动端 Web 应用而设计。

### 基本信息

| 属性 | 值 |
|------|-----|
| 包名 | `feffery-antd-mobile-components` |
| 简称 | `famc` |
| 版本 | `0.1.0-rc3` |
| 依赖 | `Dash >= 3.1.0` |
| 基础框架 | Ant Design Mobile 5.x |
| GitHub | https://github.com/CNFeffery/feffery-antd-mobile-components |

### 安装

```bash
pip install feffery-antd-mobile-components
```

### 快速开始

```python
import dash
from dash import html
import feffery_antd_mobile_components as famc

app = dash.Dash(__name__)

app.layout = famc.Fragment([
    famc.MobileNavBar(
        children='我的应用',
        backArrow=True
    ),
    famc.MobileButton(
        '点击我',
        id='my-button',
        color='primary',
        block=True
    )
])

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 与桌面端 fac 的区别

| 特性 | feffery-antd-mobile-components (famc) | feffery-antd-components (fac) |
|------|-------------------------------|------------------------|
| 目标平台 | **移动端** | 桌面端 |
| UI 框架 | Ant Design Mobile 5.x | Ant Design 5.x |
| 组件数量 | 57 个 | 200+ 个 |
| 交互方式 | **触摸优先** | 鼠标优先 |
| 设计理念 | 触摸友好、手势支持 | 桌面交互 |

---

## 组件分类索引（57 个组件）

### 通用组件 (Common) - 2 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `MobileButton` | 按钮组件，支持多种颜色、尺寸、填充模式 | `color`, `fill`, `size`, `block`, `loading` |
| `MobileIcon` | 图标组件，基于 antd-mobile-icons | `icon`, `style` |

```python
# 按钮示例
famc.MobileButton('主要按钮', color='primary', fill='solid')
famc.MobileButton('次要按钮', color='default', fill='outline')
famc.MobileButton('危险按钮', color='danger', loading=True)
famc.MobileButton('全宽按钮', block=True)
```

---

### 数据展示 (Data Display) - 15 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `MobileAvatar` | 头像组件 | `src`, `size`, `fit` |
| `MobileCard` | 卡片容器 | `title`, `extra`, `headerStyle` |
| `MobileCollapse` | 折叠面板 | `accordion`, `activeKey` |
| `MobileEllipsis` | 文本省略 | `content`, `rows`, `expandText` |
| `MobileFloatingPanel` | 浮动面板 | `anchors`, `handleDraggingOfContent` |
| `MobileFooter` | 页脚组件 | `label`, `links`, `content` |
| `MobileImage` | 图片组件 | `src`, `lazy`, `placeholder`, `fallback` |
| `MobileImageViewer` | 图片查看器 | `image`, `visible`, `onClose` |
| `MobileInfiniteScroll` | 无限滚动 | `hasMore`, `threshold` |
| `MobileList` | 列表组件 | `header`, `mode` |
| `MobilePageIndicator` | 页码指示器 | `total`, `current`, `color` |
| `MobileSteps` | 步骤条 | `current`, `direction`, `items` |
| `MobileSwiper` | 走马灯/轮播 | `autoplay`, `loop`, `indicator` |
| `MobileTag` | 标签组件 | `color`, `fill`, `round` |
| `MobileWaterMark` | 水印组件 | `content`, `gapX`, `gapY` |

```python
# 卡片示例
famc.MobileCard(
    title='卡片标题',
    extra=famc.MobileIcon(icon='antd-right'),
    children='卡片内容'
)

# 图片懒加载
famc.MobileImage(
    src='https://example.com/image.jpg',
    lazy=True,
    placeholder='加载中...',
    width='100%'
)
```

---

### 数据输入 (Data Entry) - 12 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `MobileCascader` | 级联选择器 | `options`, `value`, `visible` |
| `MobileCascaderView` | 级联选择器视图 | `options`, `value` |
| `MobileCheckbox` | 复选框 | `checked`, `disabled`, `block` |
| `MobileCheckboxGroup` | 复选框组 | `value`, `options` |
| `MobileCheckList` | 复选列表 | `value`, `multiple` |
| `MobileForm` | 表单容器 | `layout`, `mode`, `requiredMarkStyle` |
| `MobileFormHeader` | 表单头部 | `title`, `description` |
| `MobileFormItem` | 表单项 | `label`, `name`, `rules`, `required` |
| `MobileInput` | 输入框 | `value`, `placeholder`, `clearable` |
| `MobilePickerView` | 选择器视图 | `columns`, `value` |
| `MobileSearchBar` | 搜索框 | `value`, `placeholder`, `showCancelButton` |
| `MobileStepper` | 步进器（数字输入） | `value`, `min`, `max`, `step` |

```python
# 表单示例
famc.MobileForm([
    famc.MobileFormItem(
        label='用户名',
        name='username',
        required=True,
        children=famc.MobileInput(placeholder='请输入用户名', clearable=True)
    ),
    famc.MobileFormItem(
        label='密码',
        name='password',
        children=famc.MobileInput(placeholder='请输入密码', type='password')
    ),
])

# 搜索框
famc.MobileSearchBar(
    placeholder='搜索商品',
    showCancelButton=True
)
```

---

### 反馈组件 (Feedback) - 12 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `MobileActionSheet` | 动作面板（底部弹出） | `visible`, `actions`, `cancelText` |
| `MobileCenterPopup` | 中心弹窗 | `visible`, `showCloseButton` |
| `MobileDialog` | 对话框 | `visible`, `title`, `content`, `actions` |
| `MobileErrorBlock` | 错误提示块 | `status`, `title`, `description` |
| `MobilePopover` | 气泡框 | `content`, `trigger`, `placement` |
| `MobilePopup` | 弹出层 | `visible`, `position`, `bodyStyle` |
| `MobileProgressCircle` | 圆形进度条 | `percent`, `children` |
| `MobilePullToRefresh` | 下拉刷新 | `pullingText`, `canReleaseText` |
| `MobileResult` | 结果反馈 | `status`, `title`, `description` |
| `MobileSkeleton` | 骨架屏 | `animated`, `paragraph`, `title` |
| `MobileSwipeAction` | 滑动操作 | `leftActions`, `rightActions` |
| `MobileToast` | 轻提示 | `content`, `duration`, `position` |

```python
# 对话框
famc.MobileDialog(
    visible=True,
    title='提示',
    content='确定要删除吗？',
    actions=[
        {'key': 'cancel', 'text': '取消'},
        {'key': 'confirm', 'text': '确定', 'danger': True}
    ]
)

# 下拉刷新
famc.MobilePullToRefresh(
    pullingText='下拉刷新',
    canReleaseText='释放立即刷新',
    refreshingText='正在刷新...',
    completeText='刷新成功',
    children=[...]  # 内容
)

# 骨架屏
famc.MobileSkeleton(
    animated=True,
    paragraph={'rows': 3}
)
```

---

### 布局组件 (Layout) - 6 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `MobileAutoCenter` | 自动居中 | - |
| `MobileDivider` | 分割线 | `contentPosition`, `direction` |
| `MobileGrid` | 栅格容器 | `columns`, `gap` |
| `MobileGridItem` | 栅格项 | `span` |
| `MobileSafeArea` | 安全区域（刘海屏适配） | `position` |
| `MobileSpace` | 间距组件 | `direction`, `wrap`, `justify` |

```python
# 栅格布局
famc.MobileGrid(
    columns=3,
    gap=8,
    children=[
        famc.MobileGridItem(famc.MobileCard('卡片1')),
        famc.MobileGridItem(famc.MobileCard('卡片2')),
        famc.MobileGridItem(famc.MobileCard('卡片3')),
    ]
)

# 安全区域适配（iPhone 刘海屏）
famc.MobileSafeArea(position='top')  # 顶部安全区
famc.MobileSafeArea(position='bottom')  # 底部安全区
```

---

### 导航组件 (Navigation) - 6 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `MobileCapsuleTabs` | 胶囊选项卡 | `activeKey`, `onChange` |
| `MobileJumboTabs` | 大选项卡 | `activeKey` |
| `MobileNavBar` | 导航栏 | `back`, `backArrow`, `left`, `right` |
| `MobileSideBar` | 侧边栏 | `activeKey`, `items` |
| `MobileTabBar` | 标签栏（底部导航） | `activeKey`, `items`, `safeArea` |
| `MobileTabs` | 标签页 | `activeKey`, `items` |

```python
# 顶部导航栏
famc.MobileNavBar(
    children='页面标题',
    backArrow=True,
    back='返回',
    right=famc.MobileIcon(icon='antd-search')
)

# 底部标签栏
famc.MobileTabBar(
    activeKey='home',
    items=[
        {'key': 'home', 'title': '首页', 'icon': 'antd-home'},
        {'key': 'search', 'title': '搜索', 'icon': 'antd-search'},
        {'key': 'user', 'title': '我的', 'icon': 'antd-user'},
    ],
    safeArea=True
)
```

---

### 其他组件 (Other) - 5 个

| 组件 | 说明 | 关键属性 |
|------|------|----------|
| `Fragment` | 空节点包装器（类似 React Fragment） | `children` |
| `MobileFloatingBubble` | 浮动气泡 | `icon`, `magnetic`, `offset` |
| `MobileMockPhone` | 虚拟手机框架（预览用） | `children` |
| `MobileResultPage` | 结果页面 | `status`, `title`, `description` |
| `MobileResultPageCard` | 结果页面卡片 | - |

```python
# 浮动气泡（类似微信悬浮窗）
famc.MobileFloatingBubble(
    icon='antd-message',
    magnetic='x',  # 自动吸附到边缘
    offset={'x': 20, 'y': -20}
)
```

---

## 回调示例

```python
from dash import Input, Output, callback

@callback(
    Output('output', 'children'),
    Input('my-button', 'nClicks')
)
def on_button_click(n_clicks):
    if n_clicks:
        return f'按钮被点击了 {n_clicks} 次'
    return '等待点击...'
```

---

## 通用属性说明

所有组件都支持以下通用属性：

| 属性 | 类型 | 说明 |
|------|------|------|
| `id` | `string` | 组件唯一标识符，用于回调 |
| `key` | `string` | 强制重绘时使用的键值 |
| `style` | `dict` | CSS 样式字典 |
| `className` | `string` | CSS 类名 |
| `children` | `Component` | 子组件或内容 |

---

## 移动端适配策略

### 响应式断点检测

使用 `fuc.FefferyResponsive` 检测设备类型：

```python
import feffery_utils_components as fuc

fuc.FefferyResponsive(id='responsive')

@callback(
    Output('content', 'children'),
    Input('responsive', 'breakpoint'),
    Input('responsive', 'width')
)
def adapt_layout(breakpoint, width):
    # breakpoint: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl'
    if breakpoint in ['xs', 'sm']:
        return mobile_layout()  # 使用 famc 组件
    return desktop_layout()     # 使用 fac 组件
```

### 断点定义

| 断点 | 宽度范围 | 典型设备 |
|------|----------|----------|
| xs | < 576px | 手机竖屏 |
| sm | ≥ 576px | 手机横屏 |
| md | ≥ 768px | 平板竖屏 |
| lg | ≥ 992px | 平板横屏/小屏电脑 |
| xl | ≥ 1200px | 桌面电脑 |
| xxl | ≥ 1600px | 大屏显示器 |

### 禁止页面缩放

```python
app = Dash(
    __name__,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'}
    ]
)
```

---

## 完整应用示例

```python
import dash
from dash import html, callback, Input, Output
import feffery_antd_mobile_components as famc

app = dash.Dash(
    __name__,
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
    ]
)

app.layout = famc.Fragment([
    # 顶部安全区
    famc.MobileSafeArea(position='top'),

    # 导航栏
    famc.MobileNavBar(
        children='我的应用',
        backArrow=False
    ),

    # 主内容区
    html.Div([
        famc.MobileSearchBar(
            id='search',
            placeholder='搜索内容',
            style={'padding': '12px'}
        ),

        famc.MobileCard(
            title='卡片标题',
            children=[
                famc.MobileButton('点击我', id='btn', color='primary', block=True)
            ],
            style={'margin': '12px'}
        ),

        html.Div(id='output', style={'padding': '12px'})
    ], style={'paddingBottom': '60px'}),  # 为底部导航留空间

    # 底部标签栏
    html.Div([
        famc.MobileTabBar(
            activeKey='home',
            items=[
                {'key': 'home', 'title': '首页', 'icon': 'antd-home'},
                {'key': 'list', 'title': '列表', 'icon': 'antd-unordered-list'},
                {'key': 'user', 'title': '我的', 'icon': 'antd-user'},
            ],
            safeArea=True
        )
    ], style={'position': 'fixed', 'bottom': 0, 'left': 0, 'right': 0})
])

@callback(
    Output('output', 'children'),
    Input('btn', 'nClicks')
)
def on_click(n):
    if n:
        return famc.MobileResult(
            status='success',
            title='操作成功',
            description=f'按钮被点击了 {n} 次'
        )
    return None

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 参考资源

- [Ant Design Mobile 官方文档](https://mobile.ant.design/)

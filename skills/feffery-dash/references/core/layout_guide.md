# Feffery-Dash 布局指南

> 掌握 fac 布局组件，构建专业界面

---

## 1. 布局组件概览

| 组件 | 用途 | 特点 |
|------|------|------|
| `AntdRow/AntdCol` | 栅格系统 | 24列响应式 |
| `AntdSpace` | 间距排列 | 水平/垂直间距 |
| `AntdCenter` | 居中容器 | 水平垂直居中 |
| `AntdFlex` | Flex 布局 | 灵活对齐 |
| `AntdLayout` | 页面骨架 | 后台布局 |
| `AntdCompact` | 紧凑排列 | 组件组合 |

---

## 2. 栅格系统 (Row/Col)

### 2.1 基础用法

```python
import feffery_antd_components as fac

# 24 栅格系统
fac.AntdRow([
    fac.AntdCol(html.Div('左侧'), span=12),   # 50%
    fac.AntdCol(html.Div('右侧'), span=12),   # 50%
])

# 三列布局
fac.AntdRow([
    fac.AntdCol(内容, span=8),   # 33.3%
    fac.AntdCol(内容, span=8),
    fac.AntdCol(内容, span=8),
])

# 侧边栏 + 内容
fac.AntdRow([
    fac.AntdCol(侧边栏, span=6),   # 25%
    fac.AntdCol(主内容, span=18),  # 75%
])
```

### 2.2 间距 gutter

```python
# 水平间距
fac.AntdRow([...], gutter=16)

# 水平 + 垂直间距
fac.AntdRow([...], gutter=[16, 16])

# 响应式间距
fac.AntdRow([...], gutter={'xs': 8, 'sm': 16, 'md': 24})
```

### 2.3 响应式布局

```python
fac.AntdCol(
    内容,
    xs=24,    # <576px: 100%
    sm=12,    # ≥576px: 50%
    md=8,     # ≥768px: 33.3%
    lg=6,     # ≥992px: 25%
    xl=4,     # ≥1200px: 16.7%
    xxl=3,    # ≥1600px: 12.5%
)
```

### 2.4 Flex 布局

```python
# 固定宽度 + 自适应
fac.AntdRow([
    fac.AntdCol('固定200px', flex='200px'),
    fac.AntdCol('自动填充', flex='auto'),
])

# 比例分配
fac.AntdRow([
    fac.AntdCol('1份', flex=1),
    fac.AntdCol('2份', flex=2),
    fac.AntdCol('1份', flex=1),
])
```

### 2.5 对齐方式

```python
# 水平对齐
fac.AntdRow(
    [...],
    justify='start'     # start/center/end/space-between/space-around/space-evenly
)

# 垂直对齐
fac.AntdRow(
    [...],
    align='top'         # top/middle/bottom/stretch
)
```

---

## 3. 间距容器 (Space)

### 3.1 水平排列（默认）

```python
fac.AntdSpace([
    fac.AntdButton('按钮1'),
    fac.AntdButton('按钮2'),
    fac.AntdButton('按钮3'),
])
```

### 3.2 垂直排列

```python
fac.AntdSpace(
    [组件1, 组件2, 组件3],
    direction='vertical',
    style={'width': '100%'}  # 垂直必须设置宽度
)
```

### 3.3 间距大小

```python
# 预设大小
fac.AntdSpace([...], size='small')   # small/middle/large

# 自定义大小（像素）
fac.AntdSpace([...], size=24)

# 不同方向不同间距
fac.AntdSpace([...], size=[16, 8])   # [水平, 垂直]
```

### 3.4 自动换行

```python
fac.AntdSpace(
    [标签1, 标签2, 标签3, ...],
    wrap=True,
    size=[8, 8]
)
```

---

## 4. 居中容器 (Center)

### 4.1 基础居中

```python
fac.AntdCenter(
    fac.AntdButton('居中按钮'),
    style={'height': '200px'}  # 需要设置高度
)
```

### 4.2 全屏居中

```python
fac.AntdCenter(
    fac.AntdCard(
        title='登录',
        children=[...]
    ),
    style={
        'height': '100vh',      # 全屏高度
        'background': '#f0f2f5'
    }
)
```

---

## 5. Flex 布局

### 5.1 基础用法

```python
fac.AntdFlex(
    [组件1, 组件2, 组件3],
    gap='small',              # small/middle/large 或数字
    justify='space-between',  # 主轴对齐
    align='center',           # 交叉轴对齐
)
```

### 5.2 垂直排列

```python
fac.AntdFlex(
    [组件1, 组件2],
    vertical=True,
    gap=16
)
```

### 5.3 自动换行

```python
fac.AntdFlex(
    [标签1, 标签2, ...],
    wrap='wrap',
    gap=[8, 8]
)
```

---

## 6. 页面骨架 (Layout)

### 6.1 经典后台布局

```python
fac.AntdLayout([
    # 顶部导航
    fac.AntdHeader(
        fac.AntdRow([
            fac.AntdCol(html.H2('Logo'), span=4),
            fac.AntdCol(fac.AntdMenu(...), span=20),
        ]),
        style={'background': '#001529', 'padding': '0 24px'}
    ),

    fac.AntdLayout([
        # 侧边栏
        fac.AntdSider(
            fac.AntdMenu(...),
            width=200,
            style={'background': '#fff'}
        ),

        # 主内容区
        fac.AntdContent(
            页面内容,
            style={'padding': 24, 'minHeight': 'calc(100vh - 64px)'}
        )
    ]),

    # 底部
    fac.AntdFooter(
        '© 2025 Company',
        style={'textAlign': 'center'}
    )
])
```

### 6.2 固定侧边栏

```python
fac.AntdSider(
    内容,
    collapsible=True,        # 可折叠
    collapsed=False,         # 折叠状态
    width=200,               # 展开宽度
    collapsedWidth=80,       # 折叠宽度
    style={
        'position': 'fixed',
        'left': 0,
        'top': 64,
        'bottom': 0,
        'overflow': 'auto'
    }
)
```

---

## 7. style 样式控制

### 7.1 常用样式属性

```python
html.Div(
    内容,
    style={
        # 尺寸
        'width': '100%',
        'height': 200,              # 数字默认 px
        'minHeight': '100vh',

        # 边距
        'padding': 20,              # 四周
        'padding': '10px 20px',     # 上下 左右
        'margin': '10px 20px 30px 40px',  # 上 右 下 左

        # 背景
        'background': '#f0f2f5',
        'backgroundColor': 'white',

        # 边框
        'border': '1px solid #d9d9d9',
        'borderRadius': 8,

        # 文字
        'fontSize': 16,
        'fontWeight': 'bold',
        'color': '#333',
        'textAlign': 'center',

        # 阴影
        'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',

        # 溢出
        'overflow': 'auto',
        'overflowX': 'hidden',
    }
)
```

### 7.2 使用 style 工具函数

```python
from feffery_dash_utils.style_utils import style

html.Div(
    内容,
    style=style(
        backgroundColor='#f0f0f0',
        fontSize=16,
        padding=20,
        borderRadius=8
    )
)
```

---

## 8. 定位布局

### 8.1 Fixed 固定定位

```python
# 右下角悬浮按钮
fac.AntdButton(
    '返回顶部',
    style={
        'position': 'fixed',
        'right': 20,
        'bottom': 20,
        'zIndex': 999
    }
)

# 顶部固定导航
fac.AntdHeader(
    导航内容,
    style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'right': 0,
        'zIndex': 1000
    }
)
```

### 8.2 Absolute 绝对定位

```python
html.Div(
    [
        # 相对定位的父容器
        html.Div(
            [
                # 绝对定位的子元素
                html.Div(
                    '角标',
                    style={
                        'position': 'absolute',
                        'top': -5,
                        'right': -5,
                    }
                )
            ],
            style={'position': 'relative'}
        )
    ]
)
```

---

## 9. 响应式设计

### 9.1 使用 FefferyWindowSize

```python
import feffery_utils_components as fuc

app.layout = html.Div([
    fuc.FefferyWindowSize(id='window-size'),
    html.Div(id='responsive-content')
])

@app.callback(
    Output('responsive-content', 'children'),
    Input('window-size', 'width')
)
def responsive_layout(width):
    if width < 768:
        return mobile_layout()
    elif width < 1200:
        return tablet_layout()
    return desktop_layout()
```

### 9.2 CSS 媒体查询

```css
/* assets/responsive.css */
.responsive-container {
    padding: 24px;
}

@media (max-width: 768px) {
    .responsive-container {
        padding: 12px;
    }
}
```

---

## 10. 常用布局模板

### 10.1 表单布局

```python
fac.AntdForm(
    [
        fac.AntdFormItem(
            fac.AntdInput(id='name'),
            label='姓名',
            required=True
        ),
        fac.AntdFormItem(
            fac.AntdSelect(id='type', options=[...]),
            label='类型'
        ),
        fac.AntdFormItem(
            fac.AntdButton('提交', type='primary', id='submit'),
        ),
    ],
    labelCol={'span': 4},
    wrapperCol={'span': 20},
)
```

### 10.2 卡片网格

```python
fac.AntdRow(
    [
        fac.AntdCol(
            fac.AntdCard(title=f'卡片{i}', children=[...]),
            xs=24, sm=12, md=8, lg=6
        )
        for i in range(8)
    ],
    gutter=[16, 16]
)
```

### 10.3 统计数据行

```python
fac.AntdRow(
    [
        fac.AntdCol(
            fac.AntdStatistic(title='总销售额', value=126560),
            span=6
        ),
        fac.AntdCol(
            fac.AntdStatistic(title='访问量', value=8846),
            span=6
        ),
        fac.AntdCol(
            fac.AntdStatistic(title='支付笔数', value=6560),
            span=6
        ),
        fac.AntdCol(
            fac.AntdStatistic(title='运营活动效果', value=78, suffix='%'),
            span=6
        ),
    ],
    gutter=16
)
```

### 10.4 搜索 + 表格布局

```python
html.Div([
    # 搜索区域
    fac.AntdCard(
        fac.AntdSpace([
            fac.AntdInput(id='search-input', placeholder='搜索'),
            fac.AntdSelect(id='filter-select', options=[...]),
            fac.AntdButton('查询', type='primary', id='search-btn'),
            fac.AntdButton('重置', id='reset-btn'),
        ]),
        style={'marginBottom': 16}
    ),

    # 表格区域
    fac.AntdCard(
        fac.AntdTable(id='data-table', columns=[...], data=[...])
    )
])
```

# 仪表盘布局模板

> 常用仪表盘布局模板和最佳实践
> 基于 fac 栅格系统的响应式布局

---

## 经典仪表盘布局

### 1. KPI + 图表布局

```python
from feffery_dash_utils.style_utils import style

def classic_dashboard_layout():
    return html.Div(
        [
            # KPI 指标行
            fac.AntdRow(
                [
                    fac.AntdCol(kpi_card('总销售额', 123456, '¥'), xs=24, sm=12, xl=6),
                    fac.AntdCol(kpi_card('订单数', 8520), xs=24, sm=12, xl=6),
                    fac.AntdCol(kpi_card('客户数', 3200), xs=24, sm=12, xl=6),
                    fac.AntdCol(kpi_card('转化率', 68, '%', suffix=True), xs=24, sm=12, xl=6),
                ],
                gutter=[18, 18]
            ),

            # 图表行
            fac.AntdRow(
                [
                    fac.AntdCol(trend_chart_card(), xs=24, xl=16),
                    fac.AntdCol(pie_chart_card(), xs=24, xl=8),
                ],
                gutter=[18, 18],
                style={'marginTop': 18}
            ),

            # 表格行
            fac.AntdRow(
                [
                    fac.AntdCol(data_table_card(), span=24),
                ],
                gutter=[18, 18],
                style={'marginTop': 18}
            )
        ],
        style=style(
            padding=24,
            background='#f5f5f5',
            minHeight='100vh'
        )
    )
```

### 2. 侧边筛选布局

```python
def filter_sidebar_layout():
    return fac.AntdLayout(
        [
            # 侧边筛选栏
            fac.AntdSider(
                fac.AntdCard(
                    [
                        fac.AntdFormItem(
                            fac.AntdDateRangePicker(id='date-range'),
                            label='日期范围'
                        ),
                        fac.AntdFormItem(
                            fac.AntdSelect(id='category-filter', options=[...]),
                            label='分类'
                        ),
                        fac.AntdFormItem(
                            fac.AntdSelect(id='region-filter', options=[...]),
                            label='地区'
                        ),
                        fac.AntdButton('查询', id='query-btn', type='primary', block=True)
                    ],
                    title='筛选条件'
                ),
                width=280,
                theme='light',
                style={'background': '#f5f5f5', 'padding': 18}
            ),

            # 主内容区
            fac.AntdContent(
                [
                    fac.AntdRow([...], gutter=[18, 18])
                ],
                style={'padding': 24}
            )
        ],
        style={'minHeight': '100vh'}
    )
```

### 3. 标签页分组布局

```python
def tabbed_dashboard_layout():
    return html.Div(
        [
            # 顶部 KPI
            fac.AntdRow(
                [fac.AntdCol(kpi_card(...), span=6) for _ in range(4)],
                gutter=[18, 18]
            ),

            # 标签页区域
            fac.AntdTabs(
                items=[
                    {
                        'key': 'overview',
                        'label': '概览',
                        'children': overview_content()
                    },
                    {
                        'key': 'sales',
                        'label': '销售分析',
                        'children': sales_content()
                    },
                    {
                        'key': 'users',
                        'label': '用户分析',
                        'children': users_content()
                    }
                ],
                # 切换时销毁未激活面板，重置图表动画
                destroyInactiveTabPane=True,
                style={'marginTop': 18}
            )
        ],
        style=style(padding=24, background='#f5f5f5')
    )
```

---

## 卡片组件模板

### KPI 卡片

```python
def kpi_card(title, value, prefix='', suffix=False, trend=None, trend_value=None):
    """KPI 指标卡片"""
    return fac.AntdCard(
        [
            fac.AntdStatistic(
                title=title,
                value=value,
                prefix=None if suffix else prefix,
                suffix=prefix if suffix else None,
                valueStyle={'fontSize': 28}
            ),
            # 趋势指示
            html.Div(
                [
                    fac.AntdIcon(
                        icon='antd-rise' if trend == 'up' else 'antd-fall',
                        style={'color': '#52c41a' if trend == 'up' else '#ff4d4f'}
                    ),
                    html.Span(
                        trend_value,
                        style={'color': '#52c41a' if trend == 'up' else '#ff4d4f', 'marginLeft': 4}
                    )
                ],
                style={'marginTop': 8}
            ) if trend else None
        ],
        bordered=False,
        bodyStyle={'padding': '20px 24px'}
    )
```

### 图表卡片

```python
def chart_card(title, chart_component, extra=None, actions=None):
    """带操作的图表卡片"""
    return fac.AntdCard(
        chart_component,
        title=title,
        extra=extra,  # 右上角操作区
        actions=actions,  # 底部操作栏
        bordered=False,
        bodyStyle={'padding': 16}
    )
```

### 带工具栏的卡片

```python
def toolbar_chart_card(title, chart_id, chart_data_id):
    """带完整工具栏的图表卡片"""
    return fac.AntdCard(
        fact.AntdLine(id=chart_id, data=[], xField='date', yField='value'),
        title=title,
        extra=fac.AntdSpace([
            # 周期切换
            fac.AntdRadioGroup(
                id=f'{chart_id}-period',
                options=[
                    {'label': '日', 'value': 'day'},
                    {'label': '周', 'value': 'week'},
                    {'label': '月', 'value': 'month'},
                ],
                value='day',
                optionType='button',
                size='small'
            ),
            # 更多操作
            fac.AntdDropdown(
                fac.AntdButton(fac.AntdIcon(icon='antd-more'), type='text'),
                menuItems=[
                    {'title': '查看数据', 'key': 'view'},
                    {'title': '导出 Excel', 'key': 'export'},
                    {'title': '全屏查看', 'key': 'fullscreen'},
                ],
                id=f'{chart_id}-actions'
            )
        ]),
        bordered=False
    )
```

---

## 响应式断点参考

### 断点阈值定义

| 断点参数 | 屏幕宽度范围 | 典型设备 |
|----------|--------------|----------|
| **xs** | < 576px | 手机竖屏 |
| **sm** | ≥ 576px | 手机横屏 / 小平板 |
| **md** | ≥ 768px | 平板竖屏 |
| **lg** | ≥ 992px | 桌面显示器 / 笔记本 |
| **xl** | ≥ 1200px | 大桌面显示器 |
| **xxl** | ≥ 1600px | 超大显示器 |

### 组件响应式配置推荐

| 组件类型 | xs | sm | md | lg | xl | xxl |
|----------|----|----|----|----|----|----|
| KPI 卡片 | 24 | 24 | 12 | 8 | 6 | 6 |
| 小图表 | 24 | 24 | 24 | 12 | 12 | 8 |
| 大图表 | 24 | 24 | 24 | 24 | 16 | 18 |
| 侧边表格 | 24 | 24 | 24 | 24 | 8 | 6 |

### 响应式配置代码示例

```python
# KPI 指标卡：大屏一行4个，平板2个，手机1个
fac.AntdCol(
    index_card(...),
    xs=24,   # 手机端独占一行
    sm=24,
    md=12,   # 平板端占一半
    lg=8,    # 笔记本一行3个
    xl=6     # 大屏一行4个
)

# 主图表：大屏占主要位置，小屏独占
fac.AntdCol(
    simple_chart_card(...),
    xs=24,
    sm=24,
    md=24,
    lg=24,
    xl=16    # 大屏占主要位置
)

# 侧边图表/表格：配合主图表
fac.AntdCol(
    simple_chart_card(...),
    xs=24,
    sm=24,
    md=24,
    lg=24,
    xl=8     # 大屏配合主图表
)
```

### 响应式 Gutter 配置

```python
# 固定间距
fac.AntdRow([...], gutter=[18, 18])

# 响应式间距：手机紧凑，大屏宽松
fac.AntdRow([...], gutter={'xs': 8, 'md': 16, 'xl': 24})
```

### 调试技巧

使用浏览器开发者工具 (F12) 拖动侧边栏改变视口宽度：
- 观察右上角显示的像素值（如 `768px`）
- 验证布局是否在预期断点发生变化

---

## 大屏布局

### 全屏大屏布局

```python
def fullscreen_dashboard():
    return html.Div(
        [
            # 顶部标题栏
            html.Div(
                fac.AntdTitle('数据监控大屏', level=2, style={'color': 'white'}),
                style=style(
                    height=60,
                    background='linear-gradient(90deg, #1a1a2e, #16213e)',
                    display='flex',
                    alignItems='center',
                    justifyContent='center'
                )
            ),

            # 主体区域
            html.Div(
                fac.AntdRow(
                    [
                        # 左侧列
                        fac.AntdCol(
                            [left_panel_1(), left_panel_2()],
                            span=6
                        ),
                        # 中央列
                        fac.AntdCol(
                            [center_main_chart(), center_bottom_row()],
                            span=12
                        ),
                        # 右侧列
                        fac.AntdCol(
                            [right_panel_1(), right_panel_2()],
                            span=6
                        )
                    ],
                    gutter=[12, 12],
                    style={'height': 'calc(100vh - 60px)', 'padding': 12}
                ),
                style={'background': '#0f0f23'}
            )
        ],
        style={'height': '100vh', 'overflow': 'hidden'}
    )
```

---

## 骨架屏加载

```python
def loading_skeleton():
    """加载骨架屏"""
    return html.Div([
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdSkeleton(active=True, paragraph={'rows': 2}),
                    span=6
                )
                for _ in range(4)
            ],
            gutter=[18, 18]
        ),
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdSkeleton(active=True, paragraph={'rows': 8}),
                    span=16
                ),
                fac.AntdCol(
                    fac.AntdSkeleton(active=True, paragraph={'rows': 8}),
                    span=8
                )
            ],
            gutter=[18, 18],
            style={'marginTop': 18}
        )
    ])
```

---

## 参考资源

- [feffery-antd-components 官方文档](https://fac.feffery.tech/)
- [Ant Design Layout 官方文档](https://ant.design/components/layout-cn)

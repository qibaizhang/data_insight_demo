# 仪表盘快捷组件参考

> feffery-dash-utils 仪表盘快捷组件详解
> 四大核心组件：welcome_card、index_card、simple_chart_card、blank_card

---

## 环境与依赖

```python
# 核心依赖版本
# feffery-dash-utils >= 0.2.1
# feffery-antd-components (fac)
# feffery-antd-charts (fact)

# 统一导入（强制）
import feffery_antd_components as fac
import feffery_antd_charts as fact
from feffery_dash_utils.style_utils import style
from feffery_dash_utils.template_utils.dashboard_components import (
    welcome_card,
    blank_card,
    index_card,
    simple_chart_card
)
```

---

## 1. Welcome Card (欢迎卡片)

用于页面顶部，展示用户信息和欢迎语。

### 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `title` | str | 主标题（如 "欢迎您，用户张三"） |
| `description` | str/Component | 副标题/描述，可嵌入组件 |
| `icon` | Component | 左侧图标/头像，推荐 `fac.AntdAvatar` |
| `extra` | Component | 右侧额外操作区 |

### 代码示例

```python
# 基础用法
fac.AntdCol(
    welcome_card(
        title="欢迎您，用户张三",
        description="今天是元气满满的一天...",
        icon=fac.AntdAvatar(
            icon="antd-user",
            size=72,
            style={'background': '#409eff'}
        ),
        extra=fac.AntdButton("更多", type="link")
    ),
    span=24
)

# 进阶用法：嵌入交互组件
welcome_card(
    title="欢迎访问本应用，用户：张三",
    description=fac.AntdText([
        "您有5个事项待处理，点击",
        html.A("此处", id="todo-link"),
        "查看。"
    ]),
    icon=fac.AntdAvatar(src="/assets/avatar.png", size=72),
    extra=fac.AntdButton("更多信息", type="link")
)
```

### 布局建议

- **栅格**: `span=24`（独占一行）
- **位置**: 页面顶部第一个组件

---

## 2. Index Card (指标卡片)

用于展示 KPI 关键业务指标。

### 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `index_name` | str | 指标名称（如 "销售额"） |
| `index_value` | str | 核心数值（如 "99.8%"） |
| `index_description` | str | 指标说明（Tooltip） |
| `extra_content` | Component | 右侧迷你图表（TinyArea/Progress等） |
| `footer_content` | Component/str | 底部辅助信息（如 "同比提升 10%"） |

### 代码示例

```python
# 模式A：迷你面积图
fac.AntdCol(
    index_card(
        index_name="今日访问量",
        index_description="该指标统计的是...",
        index_value="12,580",
        extra_content=fact.AntdTinyArea(
            data=[120, 150, 180, 200, 220, 250, 280],
            height=60,
            smooth=True
        ),
        footer_content="同比提升 10%"
    ),
    xs=24, md=12, xl=6
)

# 模式B：迷你柱状图
index_card(
    index_name="成交笔数",
    index_value="3,856",
    extra_content=fact.AntdTinyColumn(
        data=[50, 80, 120, 90, 150, 180, 200],
        height=60,
        color="#1890ff"
    ),
    footer_content=html.Div([
        fac.AntdIcon(icon="antd-rise", style={'color': '#52c41a'}),
        html.Span("12%", style={'color': '#52c41a', 'marginLeft': 4})
    ])
)

# 模式C：进度条
index_card(
    index_name="目标完成率",
    index_value="78%",
    extra_content=fac.AntdCenter(
        fac.AntdProgress(
            percent=78,
            strokeColor={"from": "#108ee9", "to": "#87d068"},
            type="line"
        )
    ),
    footer_content="距离目标还差 22%"
)

# 模式D：趋势箭头
index_card(
    index_name="转化率",
    index_value="5.8%",
    extra_content=html.Div([
        fac.AntdIcon(
            icon="antd-rise",
            style={'color': '#52c41a', 'fontSize': 24}
        )
    ]),
    footer_content="较上周提升 0.5%"
)
```

### 布局建议

- **栅格**: `xs=24, md=12, xl=6`（大屏一行4个）
- **位置**: 欢迎卡片下方

---

## 3. Simple Chart Card (简单图表卡片)

用于包裹主业务图表。

### 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `title` | str | 图表标题 |
| `description` | str/Component | 图表描述，可嵌入筛选器 |
| `chart` | Component | 图表组件 (fact 组件) |
| `extra` | Component | 标题栏右侧操作区 |
| `height` | int | 卡片高度（默认 300） |
| `root_id` | str/dict | 卡片容器 ID（用于全屏等功能） |

### 代码示例

```python
# 基础用法
fac.AntdCol(
    simple_chart_card(
        title="销售趋势",
        description="近30天销售数据",
        chart=fact.AntdLine(
            id="sales-trend-chart",
            data=demo_data,
            xField='date',
            yField='value',
            smooth=True
        ),
        height=400
    ),
    xs=24, xl=12
)

# 带数据切换的图表卡片
simple_chart_card(
    title="销售额类别占比",
    chart=fact.AntdPie(
        id="sales-pie-chart",
        data=[...],
        angleField="value",
        colorField="type",
        radius=0.8,
        innerRadius=0.6
    ),
    extra=fac.AntdRadioGroup(
        id="update-sales-pie-chart-data",
        options=["全部渠道", "线上", "门店"],
        value="全部渠道",
        optionType="button",
        size="small"
    )
)

# 嵌入筛选器到描述
simple_chart_card(
    title="流量转化情况",
    description=fac.AntdSpace(
        [
            "时间范围：",
            fac.AntdSelect(
                id="flow-conversion-filter",
                options=["当月", "上月"],
                value="当月",
                variant="filled",
                size="small"
            )
        ],
        size=0
    ),
    chart=fact.AntdColumn(
        id="flow-conversion-chart",
        data=[...],
        xField="action",
        yField="pv",
        conversionTag={}  # 开启转化率标注
    )
)

# 支持全屏的卡片
simple_chart_card(
    root_id={"type": "chart-card", "index": "sales"},
    title="销售图表",
    chart=fact.AntdLine(...),
    extra=fac.AntdButton(
        id={"type": "chart-card-toggle-fullscreen", "index": "sales"},
        icon=fac.AntdIcon(icon="antd-fullscreen"),
        type="text"
    )
)
```

### 布局建议

- **小图表**: `xs=24, xl=12`（大屏一行2个）
- **大图表**: `xs=24, xl=16`（占主要位置）

---

## 4. Blank Card (空白卡片)

通用容器，自带阴影、圆角和内边距。

### 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `children` | Component/List | 内部填充的内容 |

### 代码示例

```python
# 基础用法
fac.AntdCol(
    blank_card(
        html.Div("这是自定义内容，容器自带样式")
    ),
    span=12
)

# 用于页脚
blank_card(
    fac.AntdCenter(
        fac.AntdText([
            fac.AntdText("玩转Dash", italic=True),
            " 知识星球出品"
        ])
    )
)

# 嵌入表格
blank_card(
    fac.AntdTable(
        id="hot-content-table",
        columns=[
            {"title": "排名", "dataIndex": "rank"},
            {"title": "内容", "dataIndex": "content"},
            {"title": "浏览量", "dataIndex": "views"}
        ],
        data=[...]
    )
)
```

---

## 5. 组合使用范式

### 完整仪表盘布局

```python
def layout():
    return html.Div(
        [
            # 全局组件
            fac.Fragment(id="message-target"),
            dcc.Download(id="global-download"),

            fac.AntdRow(
                [
                    # 欢迎卡片
                    fac.AntdCol(welcome_card(...), span=24),

                    # KPI 指标行
                    fac.AntdCol(index_card(...), xs=24, md=12, xl=6),
                    fac.AntdCol(index_card(...), xs=24, md=12, xl=6),
                    fac.AntdCol(index_card(...), xs=24, md=12, xl=6),
                    fac.AntdCol(index_card(...), xs=24, md=12, xl=6),

                    # 图表行
                    fac.AntdCol(simple_chart_card(...), xs=24, xl=12),
                    fac.AntdCol(simple_chart_card(...), xs=24, xl=12),

                    # 底部表格
                    fac.AntdCol(simple_chart_card(chart=fac.AntdTable(...)), span=24),

                    # 页脚
                    fac.AntdCol(blank_card(...), span=24),
                ],
                gutter=[18, 18]
            )
        ],
        style=style(
            padding=50,
            background="#f5f5f5",
            minHeight="100vh",
            boxSizing="border-box"
        )
    )
```

# feffery-infographic (fi)

> feffery-infographic 信息图组件库 AI 辅助开发文档
> 组件数量: 1 | 模板数量: 59 | 版本: 0.1.5

基于 [AntV Infographic](https://github.com/antvis/infographic) 的 Plotly Dash 组件库，用于在 Python Web 应用中渲染声明式信息图。支持 LLM 流式生成、可编辑模式、PNG/SVG 导出。

**核心特性：**
- 声明式 DSL 语法定义信息图
- 支持 LLM 流式生成信息图
- 可编辑模式允许用户在线修改内容
- 支持 PNG/SVG 格式导出和下载
- 内置 LLM 提示词辅助生成

---

## 快速开始

```python
# 安装
pip install feffery-infographic -U

# 导入
import feffery_infographic as fi
from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    fi.Infographic(
        syntax="""
infographic list-grid-badge-card
data
  title 产品特性
  lists
    - label 高性能
      desc 毫秒级响应
      icon flash
    - label 易用性
      desc 开箱即用
      icon check
"""
    )
], style={'padding': 50})

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 核心概念

### 1. 组件概述

fi 组件库只有 **1 个核心组件**：`fi.Infographic`，但支持 **59 种信息图模板**。

### 2. 语法结构 (DSL)

信息图由三部分组成：

```plain
infographic <template-name>   # 入口：选择模板（必须）
data                          # 数据块（必须）
  title 标题
  desc 描述
  <data-field>                # 主数据字段
    - label 项目名称
      value 数值
      desc 说明文字
      icon 图标名称
theme                         # 主题块（可选）
  palette #color1 #color2     # 配色方案
```

### 3. 语法规则

1. **第一行必须是** `infographic <template-name>`
2. **使用两个空格缩进**表示层级关系
3. **键值对格式**: `键 空格 值`（如 `label 项目名称`）
4. **数组条目**: 使用 `-` 作为前缀（如 `- label Item`）

---

## Infographic 组件 API

### 属性列表

#### 必填属性

| 属性名 | 类型 | 说明 |
|-------|------|------|
| `syntax` | `string` | **必填**，信息图渲染语法字符串 |

#### 基础属性

| 属性名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `id` | `string` | - | 组件唯一标识符 |
| `key` | `string` | - | 更新此值可强制重绘 |
| `style` | `dict` | - | CSS 样式对象 |
| `className` | `string` | - | CSS 类名 |

#### 布局属性

| 属性名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `width` | `number/string` | - | 宽度，如 `800` 或 `'100%'` |
| `height` | `number/string` | - | 高度 |
| `padding` | `number/list` | - | 内边距，支持 `[top, right, bottom, left]` |

#### 功能属性

| 属性名 | 类型 | 默认值 | 说明 |
|-------|------|--------|------|
| `editable` | `boolean` | `False` | 可编辑模式 |
| `exportTrigger` | `dict` | - | 触发导出配置 |
| `exportEvent` | `dict` | - | 导出事件数据（只读） |

### exportTrigger 配置

```python
{
    'type': 'png' | 'svg',    # 导出格式
    'dpr': 1-4,               # PNG 像素比（仅 PNG 有效）
    'download': True | False, # 是否触发下载
    'fileName': 'my_chart'    # 文件名（不含后缀）
}
```

### exportEvent 结构

```python
{
    'timestamp': 1234567890,       # 事件时间戳
    'type': 'png' | 'svg',         # 图片格式
    'data': 'data:image/png;...'   # dataURL 数据
}
```

---

## 数据字段选择规则

根据模板前缀选择对应的主数据字段：

| 模板前缀 | 主数据字段 | 说明 |
|---------|-----------|------|
| `list-*` | `lists` | 列表类信息图 |
| `sequence-*` | `sequences` | 序列类，可加 `order asc/desc` |
| `compare-*` | `compares` | 对比类，支持 `children` 分组 |
| `hierarchy-structure` | `items` | 结构图，最多 3 层嵌套 |
| `hierarchy-*` (其他) | `root` | 树结构，通过 `children` 嵌套 |
| `relation-*` | `nodes` + `relations` | 关系图 |
| `chart-*` | `values` | 图表类，可选 `category` |
| 不确定时 | `items` | 兜底选项 |

---

## 信息图模板一览（59 种）

### 📊 图表类 (chart-*) - 8 种

| 模板名 | 说明 |
|-------|------|
| `chart-bar-plain-text` | 条形图 |
| `chart-column-simple` | 柱状图 |
| `chart-line-plain-text` | 折线图 |
| `chart-pie-compact-card` | 饼图（紧凑卡片） |
| `chart-pie-donut-pill-badge` | 环形图（胶囊徽章） |
| `chart-pie-donut-plain-text` | 环形图（纯文本） |
| `chart-pie-plain-text` | 饼图（纯文本） |
| `chart-wordcloud` | 词云 |

### ⚖️ 对比类 (compare-*) - 7 种

| 模板名 | 说明 |
|-------|------|
| `compare-binary-horizontal-badge-card-arrow` | 二元对比（徽章卡片箭头） |
| `compare-binary-horizontal-simple-fold` | 二元对比（简单折叠） |
| `compare-binary-horizontal-underline-text-vs` | 二元对比（下划线 VS） |
| `compare-hierarchy-left-right-circle-node-pill-badge` | 层级左右对比 |
| `compare-quadrant-quarter-circular` | 四象限（圆形） |
| `compare-quadrant-quarter-simple-card` | 四象限（简单卡片） |
| `compare-swot` | SWOT 分析 |

### 🏗️ 层级类 (hierarchy-*) - 6 种

| 模板名 | 说明 |
|-------|------|
| `hierarchy-mindmap-branch-gradient-capsule-item` | 思维导图（分支渐变） |
| `hierarchy-mindmap-level-gradient-compact-card` | 思维导图（层级渐变） |
| `hierarchy-structure` | 结构图 |
| `hierarchy-tree-curved-line-rounded-rect-node` | 树图（曲线圆角） |
| `hierarchy-tree-tech-style-badge-card` | 树图（科技风徽章） |
| `hierarchy-tree-tech-style-capsule-item` | 树图（科技风胶囊） |

### 📋 列表类 (list-*) - 12 种

| 模板名 | 说明 |
|-------|------|
| `list-column-done-list` | 竖向待办列表 |
| `list-column-simple-vertical-arrow` | 竖向简单箭头 |
| `list-column-vertical-icon-arrow` | 竖向图标箭头 |
| `list-grid-badge-card` | 网格徽章卡片 |
| `list-grid-candy-card-lite` | 网格糖果卡片 |
| `list-grid-ribbon-card` | 网格丝带卡片 |
| `list-row-horizontal-icon-arrow` | 横向图标箭头 |
| `list-sector-plain-text` | 扇形纯文本 |
| `list-zigzag-down-compact-card` | Z 形向下紧凑卡片 |
| `list-zigzag-down-simple` | Z 形向下简单 |
| `list-zigzag-up-compact-card` | Z 形向上紧凑卡片 |
| `list-zigzag-up-simple` | Z 形向上简单 |

### 🔗 关系类 (relation-*) - 4 种

| 模板名 | 说明 |
|-------|------|
| `relation-dagre-flow-tb-animated-badge-card` | 流程图（动画徽章卡片） |
| `relation-dagre-flow-tb-animated-simple-circle-node` | 流程图（动画圆形节点） |
| `relation-dagre-flow-tb-badge-card` | 流程图（徽章卡片） |
| `relation-dagre-flow-tb-simple-circle-node` | 流程图（简单圆形节点） |

### 📈 序列类 (sequence-*) - 21 种

| 模板名 | 说明 |
|-------|------|
| `sequence-ascending-stairs-3d-underline-text` | 3D 阶梯（下划线文本） |
| `sequence-ascending-steps` | 上升步骤 |
| `sequence-circular-simple` | 环形简单 |
| `sequence-color-snake-steps-horizontal-icon-line` | 彩色蛇形步骤 |
| `sequence-cylinders-3d-simple` | 3D 圆柱 |
| `sequence-filter-mesh-simple` | 过滤网格 |
| `sequence-funnel-simple` | 漏斗图 |
| `sequence-horizontal-zigzag-underline-text` | 横向 Z 形 |
| `sequence-mountain-underline-text` | 山峰图 |
| `sequence-pyramid-simple` | 金字塔 |
| `sequence-roadmap-vertical-plain-text` | 路线图（纯文本） |
| `sequence-roadmap-vertical-simple` | 路线图（简单） |
| `sequence-snake-steps-compact-card` | 蛇形步骤（紧凑卡片） |
| `sequence-snake-steps-simple` | 蛇形步骤（简单） |
| `sequence-snake-steps-underline-text` | 蛇形步骤（下划线） |
| `sequence-stairs-front-compact-card` | 正面阶梯（紧凑卡片） |
| `sequence-stairs-front-pill-badge` | 正面阶梯（胶囊徽章） |
| `sequence-timeline-rounded-rect-node` | 时间线（圆角矩形） |
| `sequence-timeline-simple` | 时间线（简单） |
| `sequence-zigzag-pucks-3d-simple` | 3D Z 形圆盘 |
| `sequence-zigzag-steps-underline-text` | Z 形步骤（下划线） |

---

## 模板选择建议

### 按内容类型选择

| 内容类型 | 推荐模板 |
|---------|---------|
| 流程/步骤 | `sequence-timeline-*`, `sequence-stairs-*`, `sequence-roadmap-*` |
| 时间线 | `sequence-timeline-simple`, `sequence-timeline-rounded-rect-node` |
| 观点列举 | `list-row-*`, `list-column-*` |
| 要点展示 | `list-grid-badge-card`, `list-grid-candy-card-lite` |
| 二元对比（利弊） | `compare-binary-*` |
| SWOT 分析 | `compare-swot` |
| 象限分析 | `compare-quadrant-*` |
| 组织结构 | `hierarchy-tree-*`, `hierarchy-structure` |
| 思维导图 | `hierarchy-mindmap-*` |
| 流程关系 | `relation-dagre-flow-*` |
| 数据统计 | `chart-column-simple`, `chart-bar-*`, `chart-pie-*` |
| 词云 | `chart-wordcloud` |
| 漏斗/金字塔 | `sequence-funnel-simple`, `sequence-pyramid-simple` |

### 按视觉风格选择

| 风格 | 推荐模板后缀 |
|-----|------------|
| 简约 | `*-simple`, `*-plain-text` |
| 卡片式 | `*-badge-card`, `*-compact-card` |
| 科技感 | `*-tech-style-*` |
| 3D 效果 | `*-3d-*` |
| 动画效果 | `*-animated-*` |

---

## 常用代码模式

### 1. 基础渲染

```python
import dash
from dash import html
import feffery_infographic as fi

app = dash.Dash(__name__)

app.layout = html.Div([
    fi.Infographic(
        syntax="""
infographic list-grid-badge-card
data
  title 功能特性
  lists
    - label 高性能
      desc 毫秒级响应
      icon flash
    - label 易用性
      desc 开箱即用
      icon check
"""
    )
], style={'padding': 50})
```

### 2. 可编辑模式

```python
fi.Infographic(
    editable=True,        # 启用可编辑模式
    syntax="...",
    padding=25,
    height=800
)
```

### 3. 导出图片

```python
from dash.dependencies import Input, Output

@app.callback(
    Output('my-infographic', 'exportTrigger'),
    Input('export-btn', 'nClicks'),
    prevent_initial_call=True
)
def export_image(n):
    return {'type': 'png', 'dpr': 2, 'download': True}
```

### 4. 监听导出事件

```python
@app.callback(
    Output('preview-image', 'src'),
    Input('my-infographic', 'exportEvent')
)
def show_preview(event):
    if event and event.get('data'):
        return event['data']  # dataURL 格式
    return dash.no_update
```

### 5. 时间线信息图

```python
fi.Infographic(
    syntax="""
infographic sequence-timeline-simple
data
  title 项目里程碑
  sequences
    - label 需求确认
      desc 完成需求分析文档
      time 2024-01
    - label 设计评审
      desc 完成 UI/UX 设计
      time 2024-02
    - label 开发完成
      desc 核心功能开发完毕
      time 2024-03
    - label 正式上线
      desc 产品发布运营
      time 2024-04
theme light
"""
)
```

### 6. SWOT 分析

```python
fi.Infographic(
    syntax="""
infographic compare-swot
data
  title 企业 SWOT 分析
  compares
    - label 优势 (Strengths)
      children
        - label 技术领先
        - label 品牌知名度
    - label 劣势 (Weaknesses)
      children
        - label 运营成本高
        - label 市场覆盖有限
    - label 机会 (Opportunities)
      children
        - label 新兴市场
        - label 政策支持
    - label 威胁 (Threats)
      children
        - label 竞争加剧
        - label 技术迭代快
theme dark
"""
)
```

### 7. 组织架构树

```python
fi.Infographic(
    syntax="""
infographic hierarchy-tree-tech-style-badge-card
data
  title 公司组织架构
  root
    label CEO
    children
      - label CTO
        children
          - label 研发部
          - label 测试部
      - label CFO
        children
          - label 财务部
          - label 审计部
"""
)
```

### 8. 流程图

```python
fi.Infographic(
    syntax="""
infographic relation-dagre-flow-tb-simple-circle-node
data
  title 用户认证流程
  nodes
    - id start
      label 用户请求
    - id auth
      label 身份验证
    - id success
      label 认证成功
    - id fail
      label 认证失败
  relations
    start - 提交凭证 -> auth
    auth - 验证通过 -> success
    auth - 验证失败 -> fail
"""
)
```

---

## LLM 提示词集成

### 导入内置提示词

```python
from feffery_infographic.prompts import base_prompt, base_prompt_en

# 中文提示词
print(base_prompt)

# 英文提示词
print(base_prompt_en)
```

### 与 LLM API 集成

```python
import openai
from feffery_infographic.prompts import base_prompt

def generate_infographic(user_request: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": user_request}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# 使用示例
syntax = generate_infographic("请帮我生成一个关于项目管理流程的时间线信息图")
```

### 流式生成 (SSE)

```python
import json
from flask import Response
import feffery_utils_components as fuc
from feffery_infographic.prompts import base_prompt

# SSE 端点
@app.server.route('/generate-stream/<path:prompt>')
def generate_stream(prompt):
    def stream():
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": base_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                data = json.dumps({
                    "syntax": content.replace('\n', '<换行>')
                }, ensure_ascii=False)
                yield f'data: {data}\n\n'
    return Response(stream(), mimetype='text/event-stream')

# 客户端回调实时更新
app.clientside_callback(
    """
(data, originSyntax) => {
    if (data) {
        data = JSON.parse(data);
        dash_clientside.set_props('stream-chart', {
            syntax: originSyntax + data.syntax.replaceAll('<换行>', '\\n')
        });
    }
}
""",
    Input('sse-source', 'data'),
    State('stream-chart', 'syntax'),
)
```

---

## 主题配置

### 基础主题

```plain
theme light   # 亮色主题
theme dark    # 暗色主题
```

### 自定义配色

```plain
theme
  palette
    - #3b82f6
    - #8b5cf6
    - #f97316
```

### 手绘风格

```plain
theme
  stylize rough
  base
    text
      font-family 851tegakizatsu
```

### 内置风格效果

| 风格 | 说明 |
|-----|------|
| `rough` | 手绘效果 |
| `pattern` | 图案填充 |
| `linear-gradient` | 线性渐变 |
| `radial-gradient` | 径向渐变 |

---

## 常见问题

### Q: 如何动态更新信息图？

```python
@app.callback(
    Output('my-chart', 'syntax'),
    Input('template-selector', 'value')
)
def update_chart(template):
    return f"infographic {template}\ndata\n  ..."
```

### Q: LLM 生成的语法渲染失败？

检查以下几点：
1. 确保语法以 `infographic <template-name>` 开头
2. 检查缩进是否正确（使用两个空格）
3. 确认模板名称存在于模板列表中
4. 移除可能的 Markdown 代码块标记

### Q: 如何处理 LLM 输出的代码块？

```python
import re

def extract_syntax(llm_output: str) -> str:
    match = re.search(r'```plain\s*(.*?)\s*```', llm_output, re.DOTALL)
    if match:
        return match.group(1).strip()
    if llm_output.strip().startswith('infographic'):
        return llm_output.strip()
    return llm_output
```

---

## 外部资源

- **语法参考**: https://infographic.antv.vision/learn/infographic-syntax
- **示例画廊**: https://infographic.antv.vision/gallery
- **GitHub**: https://github.com/HogaStack/feffery-infographic

---

*本文档用于 AI 辅助开发。如有疑问请参考 AntV Infographic 官方文档。*

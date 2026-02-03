# feffery-examples

> Feffery-Dash 案例库 Skill
> 案例数量: 390+ | 持续更新中

当用户需要参考示例代码、实现特定功能或学习最佳实践时使用。

---

## 案例库概述

案例库包含 390+ 个真实项目示例，覆盖 feffery 系列组件的各种使用场景。

**命名规则：** `YYYYMMDD-功能描述`

---

## 案例分类索引

### 🎨 UI 组件 (fac)

#### 表单输入
- `20240128-fac设置输入框自动聚焦`
- `20240111-针对选择卡片进行双向值同步+动态更新可选项`
- `20240114-AntdTreeSelect支持组件型树节点标题定义`
- `20240116-fac中为级联选择设置搜索字段目标`
- `20240117-fac新增可选择标签组件，可用于轻量选项选择`

#### 表格组件
- `20240125-AntdTable嵌套行记录控制父级与子级之间的选择联动行为`
- `20240126-AntdTable设置部分行不可选择`

#### 树形组件
- `20240113-AntdTree树节点搜索新增大小写不敏感支持`
- `20240114-AntdTree树节点搜索支持多关键词`
- `20240114-AntdTree支持组件型树节点标题定义`

#### 级联选择
- `20240114-fac级联选择组件支持组件型选项节点定义`
- `20240116-fac中为级联选择设置搜索字段目标`

#### 动态组件
- `20240116-基于fac+fuc实现带过渡动画的动态标签增删`
- `20240201-动态生成标签页之间独立运作相同的回调逻辑模式`

---

### 📊 图表组件 (fact)

#### 基础图表
- `20240111-基于fact批量生成直方图`
- `20240130-fact图表切换内置主题`
- `20240203-fact对图表图例进行自定义排序的快捷方式`
- `20240203-fact折线图灵活控制对指定线的着重展示`

#### 高级图表
- `20240204-fact新增热力图组件`
- `20240218-fact新增瀑布图组件AntdWaterfall`

#### 迷你图表
- `20240205-fact新增迷你面积图组件`
- `20240205-fact新增迷你柱状图组件`
- `20240206-fact新增进度条图、进度环图`

#### 图表联动
- `20240120-fact+fac实现图表数据联动的简单示例`

---

### 🛠️ 工具组件 (fuc)

#### 背景动效
- `20240118-fuc中新增BirdsBackground动效背景组件`
- `20240118-fuc中新增CloudsBackground动效背景组件`
- `20240118-fuc中新增FogBackground动效背景组件`
- `20240118-fuc中新增WavesBackground动效背景组件`
- `20240122-fuc中新增FefferyCellsBackground动效背景组件`
- `20240122-fuc中新增FefferyHaloBackground动效背景组件`
- `20240122-fuc中新增FefferyNetBackground动效背景组件`
- `20240122-fuc中新增FefferyRingsBackground动效背景组件`
- `20240122-fuc中新增FefferyTopologyBackground动效背景组件`
- `20240122-fuc中新增FefferyTrunkBackground动效背景组件`
- `20240122-fuc中新增GlobeBackground动效背景组件`

#### 文档预览
- `20240104-fuc中的excel文件预览组件`
- `20240106-fuc中的word文档预览组件`

#### 图片处理
- `20240102-fuc新增全景图片查看器`
- `20240102-基于fuc图片裁剪组件FefferyImageCropper实现头像裁剪`

#### 通信组件
- `20240131-基于fuc轻松实现与内嵌iframe双向通信`

#### 滚动组件
- `20240107-fuc预发布版本中的无缝滚动组件`

---

### 🗺️ 地图组件 (flc/fm)

#### 热力图
- `20240131-fm中新增热力图层组件`

#### 数据可视化
- `20240111-数据实时刷新的地图+图表可视化仪表盘简例`

---

### 📱 大屏与仪表盘

- `20240119-经典科技风格数据大屏模板`
- `20240111-数据实时刷新的地图+图表可视化仪表盘简例`

---

### 🤖 AI 应用

- `20240624-纯Dash开发的对话机器人项目DashChat版本v0.0.1`

---

### 🔧 Magic-Dash 框架

- `20250911-magic-dash多页面模板添加多级子菜单页面示例`
- `20250916-magic-dash多页面模板跨页面使用共享数据示例`
- `20251009-实现dify官网同款鼠标跟随指示功能`
- `20251130-magic-dash侧边菜单使用iconfont中的自定义图标库`

---

### 💡 技巧与模式

#### JS 交互
- `20240125-AntdButton按钮点击直接触发执行js程序，以全屏、退出全屏为例`
- `20240127-在dash应用中使用原生G2渲染图表`

#### 媒体处理
- `20240126-触发音频提示音播放`
- `20240127-在dash应用中显示数据库中的二进制图片，以svg、jpg、png格式为例`

---

## 案例代码模式

### 基础应用模式

```python
from dash import Dash, html
import feffery_antd_components as fac

app = Dash(__name__)

app.layout = fac.AntdConfigProvider(
    locale='zh-cn',
    children=[
        html.Div([
            fac.AntdButton('点击', id='btn', type='primary'),
            html.Div(id='output')
        ])
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
```

### 回调模式

```python
from dash import callback, Input, Output

@callback(
    Output('output', 'children'),
    Input('btn', 'nClicks'),
    prevent_initial_call=True
)
def handle_click(n):
    return f'点击了 {n} 次'
```

### 联动模式

```python
@callback(
    Output('chart', 'data'),
    Input('selector', 'value')
)
def update_chart(selected):
    # 根据选择更新图表数据
    return get_filtered_data(selected)
```

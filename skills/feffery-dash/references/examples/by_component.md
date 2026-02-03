# 案例按组件索引

> 按具体组件名检索相关案例
> 查找特定组件的使用示例

---

## FAC 组件案例索引

### 表单组件

| 组件 | 案例关键词 | 功能点 |
|------|-----------|--------|
| AntdInput | input, 输入框 | 基础输入、密码、搜索、防抖 |
| AntdSelect | select, 选择 | 单选、多选、远程搜索、分组 |
| AntdDatePicker | date, 日期 | 日期选择、范围、禁用日期 |
| AntdUpload | upload, 上传 | 文件上传、拖拽上传、图片预览 |
| AntdForm | form, 表单 | 表单布局、验证、动态表单 |

### 数据展示组件

| 组件 | 案例关键词 | 功能点 |
|------|-----------|--------|
| AntdTable | table, 表格 | 分页、排序、筛选、编辑、展开 |
| AntdTree | tree, 树形 | 树形选择、懒加载、拖拽 |
| AntdCard | card, 卡片 | 卡片布局、操作区 |
| AntdStatistic | statistic, 统计 | KPI 展示、数字动画 |
| AntdDescriptions | descriptions | 详情展示 |

### 布局组件

| 组件 | 案例关键词 | 功能点 |
|------|-----------|--------|
| AntdRow/Col | grid, 栅格 | 响应式布局 |
| AntdFlex | flex, 弹性 | 弹性布局 |
| AntdSpace | space, 间距 | 元素间距 |
| AntdSplitter | splitter, 分割 | 可拖拽分割 |
| AntdLayout | layout, 布局 | 页面整体布局 |

### 反馈组件

| 组件 | 案例关键词 | 功能点 |
|------|-----------|--------|
| AntdModal | modal, 弹窗 | 确认框、表单弹窗 |
| AntdDrawer | drawer, 抽屉 | 侧边抽屉 |
| AntdMessage | message, 消息 | 全局消息 |
| AntdNotification | notification | 通知提醒 |
| AntdSpin | spin, loading | 加载状态 |

---

## FUC 组件案例索引

### 背景动效

| 组件 | 案例关键词 |
|------|-----------|
| FefferyVantaBirds | vanta, birds, 飞鸟 |
| FefferyVantaWaves | vanta, waves, 波浪 |
| FefferyVantaNet | vanta, net, 网络 |
| FefferyVantaFog | vanta, fog, 雾气 |

### 工具组件

| 组件 | 案例关键词 |
|------|-----------|
| FefferyCookie | cookie, 存储 |
| FefferyLocalStorage | storage, 本地存储 |
| FefferyFullscreen | fullscreen, 全屏 |
| FefferyDom2Image | screenshot, 截图 |
| FefferyCountUp | countup, 数字动画 |
| FefferyShortcutKey | shortcut, 快捷键 |

---

## FACT 图表案例索引

### 基础图表

| 组件 | 案例关键词 |
|------|-----------|
| AntdLine | line, 折线图, 趋势 |
| AntdArea | area, 面积图 |
| AntdColumn | column, 柱状图 |
| AntdBar | bar, 条形图 |
| AntdPie | pie, 饼图, 环形图 |
| AntdScatter | scatter, 散点图 |

### 高级图表

| 组件 | 案例关键词 |
|------|-----------|
| AntdDualAxes | dual, 双轴图 |
| AntdSankey | sankey, 桑基图, 流量 |
| AntdFunnel | funnel, 漏斗图, 转化 |
| AntdWaterfall | waterfall, 瀑布图 |
| AntdRadar | radar, 雷达图 |
| AntdWordCloud | wordcloud, 词云 |
| AntdHeatmap | heatmap, 热力图 |

---

## 地图组件案例索引

### FLC (Leaflet)

| 组件 | 案例关键词 |
|------|-----------|
| LeafletMap | leaflet, map, 地图 |
| LeafletMarker | marker, 标记 |
| LeafletGeoJSON | geojson, 地理 |
| LeafletHeatMap | heatmap, 热力 |
| LeafletAntPath | antpath, 蚂蚁线 |

### FM (MapLibre)

| 组件 | 案例关键词 |
|------|-----------|
| MapLibre | maplibre, 地图 |
| MapLibreScatterplotLayer | scatter, deck |
| MapLibreArcLayer | arc, OD, 弧线 |
| MapLibreHexagonLayer | hexagon, 六边形 |
| MapLibreTripsLayer | trips, 轨迹, 动画 |

---

## 搜索示例

### 查找表格案例

```bash
# 在案例库中搜索 AntdTable
grep -r "AntdTable" --include="*.py" 案例库/
```

### 查找图表案例

```bash
# 搜索折线图
grep -r "AntdLine" --include="*.py" 案例库/
```

### 查找特定功能

```bash
# 搜索分页功能
grep -r "pagination" --include="*.py" 案例库/
```

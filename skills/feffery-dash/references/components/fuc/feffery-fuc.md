# feffery-fuc

> feffery-utils-components 工具组件库 Skill
> 组件数量: 128 | 官方文档: https://fuc.feffery.tech/

当用户需要性能优化、事件监听、动效、验证码等工具功能时使用 fuc 组件。

---

## 快速开始

```python
import feffery_utils_components as fuc
from dash import Dash, html

app = Dash(__name__)
app.layout = html.Div([
    fuc.FefferyDiv(
        children='Hello World',
        shadow='hover-shadow'
    )
])
```

---

## 组件分类速查

### 性能优化组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyDebounceProp` | 属性防抖 | `propName`, `delay` |
| `FefferyThrottleProp` | 属性节流 | `propName`, `interval` |
| `FefferyLazyLoad` | 懒加载 | `height`, `once` |
| `FefferyVirtualList` | 虚拟列表 | `items`, `itemHeight`, `height` |

### 容器组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyDiv` | 进阶 div | `shadow`, 事件监听 |
| `FefferyScrollbars` | 滚动条容器 | 自定义滚动条样式 |
| `FefferyPortal` | 传送门 | 渲染到指定 DOM |
| `FefferySticky` | 粘性布局 | 粘性定位 |
| `FefferyFixed` | 固定布局 | 固定定位 |

### 动效组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyAutoAnimate` | 自动动画 | 子元素过渡动画 |
| `FefferyMotion` | 动画编排 | framer-motion |
| `FefferyTiltHover` | 倾斜悬浮 | 3D 倾斜效果 |

### 3D 背景动效

| 组件 | 效果 |
|------|------|
| `FefferyBirdsBackground` | 飞鸟动画 |
| `FefferyCloudsBackground` | 云朵动画 |
| `FefferyCloudsTwoBackground` | 云朵变体 |
| `FefferyWavesBackground` | 波浪动画 |
| `FefferyNetBackground` | 网格动画 |
| `FefferyGlobeBackground` | 地球动画 |
| `FefferyFogBackground` | 雾气动画 |
| `FefferyHaloBackground` | 光环动画 |
| `FefferyRingsBackground` | 圆环动画 |
| `FefferyTopologyBackground` | 拓扑动画 |
| `FefferyCellsBackground` | 细胞动画 |
| `FefferyTrunkBackground` | 树干动画 |

### 监听器组件

| 组件 | 用途 | 监听属性 |
|------|------|----------|
| `FefferyWindowSize` | 窗口尺寸 | `width`, `height` |
| `FefferyEventListener` | 事件监听 | 通用 DOM 事件 |
| `FefferyKeyPress` | 按键监听 | `keys`, `pressedCounts` |
| `FefferyMousePosition` | 鼠标位置 | `x`, `y` |
| `FefferyInViewport` | 视口检测 | `isInViewport` |
| `FefferyIdle` | 空闲检测 | `isIdle` |
| `FefferyDeviceDetect` | 设备检测 | 设备类型 |
| `FefferyNetwork` | 网络状态 | `isOnline` |
| `FefferyGeolocation` | 地理定位 | 经纬度 |
| `FefferyDocumentVisibility` | 页面可见性 | `isVisible` |
| `FefferyMediaQuery` | 媒体查询 | 响应式断点 |
| `FefferyResponsive` | 响应式 | 断点检测 |
| `FefferyListenScroll` | 滚动监听 | 滚动位置 |
| `FefferyListenHover` | 悬停监听 | `isHovering` |
| `FefferyLongPress` | 长按监听 | 长按事件 |
| `FefferyTextSelection` | 文本选择 | 选中文本 |

### 工具组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyExecuteJs` | 执行 JS | `jsString` |
| `FefferyTimeout` | 定时器 | `delay`, `enabled` |
| `FefferyCountDown` | 倒计时 | `delay`, `countdown` |
| `FefferyFullscreen` | 全屏化 | `targetId`, `isFullscreen` |
| `FefferyReload` | 页面刷新 | 触发刷新 |
| `FefferyScroll` | 滚动控制 | 滚动到指定位置 |
| `FefferySetTitle` | 设置标题 | `title` |
| `FefferySetFavicon` | 设置图标 | `favicon` |
| `FefferyGuide` | 引导组件 | 新手引导 |

### 样式组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyStyle` | 样式注入 | `rawStyle` |
| `FefferyCssVar` | CSS 变量 | 动态 CSS 变量 |
| `FefferyHighlightWords` | 关键词高亮 | `keywords` |

### 存储组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyCookie` | Cookie | `cookieKey`, `value` |
| `FefferyLocalStorage` | localStorage | `data`, `initialSync` |
| `FefferySessionStorage` | sessionStorage | `data`, `initialSync` |
| `FefferyLocalLargeStorage` | IndexedDB | 大容量存储 |

### 验证码组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyCaptcha` | 图形验证码 | `captcha` |
| `FefferySliderCaptcha` | 滑块验证码 | `verified` |

### 颜色选择器

| 组件 | 风格 |
|------|------|
| `FefferyHexColorPicker` | 16 进制 |
| `FefferyRgbColorPicker` | RGB |
| `FefferyBlockColorPicker` | Block 风格 |
| `FefferyCircleColorPicker` | Circle 风格 |
| `FefferyGithubColorPicker` | Github 风格 |
| `FefferyTwitterColorPicker` | Twitter 风格 |
| `FefferyWheelColorPicker` | 色轮风格 |
| `FefferyEyeDropper` | 屏幕取色 |

### 拖拽组件

| 组件 | 用途 | 关键属性 |
|------|------|----------|
| `FefferyDraggable` | 可拖拽 | `position` |
| `FefferySortable` | 排序列表 | `items` |
| `FefferyRND` | 可调尺寸可拖拽 | `position`, `size` |
| `FefferyGrid` | 可拖拽网格 | 网格布局 |
| `FefferyResizable` | 可调尺寸 | `size` |

### 播放器组件

| 组件 | 用途 |
|------|------|
| `FefferyAPlayer` | 音频播放 |
| `FefferyDPlayer` | 视频播放 |
| `FefferyMusicPlayer` | 音乐播放 |

### 编辑器组件

| 组件 | 用途 |
|------|------|
| `FefferyMarkdownEditor` | Markdown 编辑器 |
| `FefferyRichTextEditor` | 富文本编辑器 |
| `FefferyVditor` | Vditor 编辑器 |

### 文档预览组件

| 组件 | 用途 |
|------|------|
| `FefferyExcelPreview` | Excel 预览 |
| `FefferyWordPreview` | Word 预览 |

### 图片处理组件

| 组件 | 用途 |
|------|------|
| `FefferyImageCropper` | 图片裁切 |
| `FefferyImageGallery` | 图片画廊 |
| `FefferyDom2Image` | DOM 转图片 |
| `FefferyAnimatedImage` | 动图播放 |
| `FefferyPhotoSphereViewer` | 全景图查看 |

### 数据展示组件

| 组件 | 用途 |
|------|------|
| `FefferyJsonViewer` | JSON 查看器 |
| `FefferyBarcode` | 条形码 |
| `FefferyQRCode` | 二维码 |
| `FefferyCountUp` | 数字动画 |
| `FefferySeamlessScroll` | 无缝滚动 |
| `FefferyCompareSlider` | 对比滑块 |

### 通信组件

| 组件 | 用途 |
|------|------|
| `FefferyHttpRequests` | HTTP 请求 |
| `FefferyWebSocket` | WebSocket |
| `FefferyEventSource` | SSE 通信 |
| `FefferyIframeMessenger` | iframe 通信 |
| `FefferyTabMessenger` | 标签页通信 |

### 外部资源组件

| 组件 | 用途 |
|------|------|
| `FefferyExternalCss` | 动态加载 CSS |
| `FefferyExternalJs` | 动态加载 JS |

### 安全组件

| 组件 | 用途 |
|------|------|
| `FefferyDebugGuardian` | 调试守卫 |

### 尺寸调整组件

| 组件 | 用途 |
|------|------|
| `FefferyAutoFit` | 大屏自适应 |

---

## 常用代码模式

### 输入防抖

```python
fuc.FefferyDebounceProp(
    fac.AntdInput(id='search-input', placeholder='搜索'),
    id='debounced-search',
    propName='value',
    delay=500
)

@callback(Output(...), Input('debounced-search', 'value'))
def search(value):
    # 防抖后的值
    pass
```

### 窗口尺寸监听

```python
fuc.FefferyWindowSize(id='window-size'),

@callback(Output(...), Input('window-size', 'width'))
def responsive(width):
    if width < 768:
        return mobile_layout()
    return desktop_layout()
```

### 动态样式注入

```python
fuc.FefferyStyle(id='dynamic-style'),

@callback(Output('dynamic-style', 'rawStyle'), Input('theme-switch', 'checked'))
def switch_theme(dark):
    if dark:
        return ':root { --bg-color: #000; --text-color: #fff; }'
    return ':root { --bg-color: #fff; --text-color: #000; }'
```

### 3D 背景

```python
fuc.FefferyWavesBackground(
    html.Div([...]),  # 页面内容
    color='#1890ff',
    style={'position': 'fixed', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'zIndex': -1}
)
```

### 大屏自适应

```python
fuc.FefferyAutoFit(
    html.Div(大屏内容),
    designWidth=1920,
    designHeight=1080
)
```

### 执行 JS

```python
fuc.FefferyExecuteJs(id='js-executor'),

@callback(Output('js-executor', 'jsString'), Input('btn', 'nClicks'))
def execute_js(n):
    return 'console.log("Hello from JS!");'
```

### 快捷键监听

```python
fuc.FefferyKeyPress(id='save-shortcut', keys='ctrl.s')

@callback(Output(...), Input('save-shortcut', 'pressedCounts'), prevent_initial_call=True)
def handle_save(n):
    # Ctrl+S 被按下
    save_data()
```

---

## 分类文档

- [背景动效组件](./background_effects.md) - 3D 背景动画详解
- [颜色选择器组件](./color_pickers.md) - 各种颜色选择器详解
- [实用工具组件](./utility_tools.md) - 存储、截图、全屏等工具

---

## 参考资源

- [feffery-utils-components 官方文档](https://fuc.feffery.tech/)

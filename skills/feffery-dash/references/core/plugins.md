# Dash 3.x 插件系统

> Feffery 生态插件使用指南
> 版本: 1.0 | 更新: 2025-12-19

Dash 3.x 引入了基于 hooks 的插件系统，允许开发者以"零侵入"或"低耦合"的方式注入功能。将错误处理、性能监控、资源加载等横切关注点从业务逻辑中剥离，极大地提升了代码的可维护性。

---

## 1. 插件概览

### 1.1 官方及 Feffery 生态插件

| 插件名称 | 功能 | 典型场景 | GitHub |
|----------|------|----------|--------|
| `dash-change-cdn-plugin` | CDN 切换 | 国内访问慢时切换到 npmmirror/jsdelivr | CNFeffery/dash-change-cdn-plugin |
| `dash-console-filter-plugin` | 控制台过滤 | 屏蔽冗余 React 警告 | CNFeffery/dash-console-filter-plugin |
| `dash-performance-monitor-plugin` | 性能监控 | 实时 FPS/内存监控 | CNFeffery/dash-performance-monitor-plugin |
| `dash-react-scan-plugin` | 渲染监控 | 组件重绘分析优化 | CNFeffery/dash-react-scan-plugin |
| `dash-disable-devtool-plugin` | 安全加固 | 禁用 F12/右键 | CNFeffery/dash-disable-devtool-plugin |
| `dash-offline-detect-plugin` | 断线检测 | 后端不可用时前端提示 | CNFeffery/dash-offline-detect-plugin |
| `dash-vite-plugin` | Vite 构建 | HMR 热更新加速开发 | HogaStack/dash-vite-plugin |
| `dash-tailwindcss-plugin` | Tailwind CSS | 实用优先的 CSS 样式 | HogaStack/dash-tailwindcss-plugin |

---

## 2. CDN 切换插件

### 2.1 安装与使用

```bash
pip install dash-change-cdn-plugin
```

```python
import dash
from dash_change_cdn_plugin import ChangeCDNPlugin

app = dash.Dash(
    __name__,
    serve_locally=False,  # 关键！必须关闭本地服务
    plugins=[ChangeCDNPlugin(cdn='npmmirror')]  # 或 'jsdelivr'
)
```

### 2.2 可用 CDN 选项

| CDN | 说明 | 适用场景 |
|-----|------|----------|
| `npmmirror` | 淘宝 NPM 镜像 | 国内访问，速度快 |
| `jsdelivr` | JSDelivr CDN | 全球加速，稳定性好 |
| `unpkg` | 默认 CDN | 国外访问 |

---

## 3. 控制台过滤插件

屏蔽开发环境中冗余的 React 警告或非关键错误。

```bash
pip install dash-console-filter-plugin
```

```python
from dash_console_filter_plugin import ConsoleFilterPlugin

app = dash.Dash(
    __name__,
    plugins=[ConsoleFilterPlugin(keywords=['warning', 'deprecated'])]
)
```

---

## 4. 性能监控插件

实时显示 FPS、内存占用，辅助定位卡顿（仅开发环境使用）。

```bash
pip install dash-performance-monitor-plugin
```

```python
from dash_performance_monitor_plugin import PerformanceMonitorPlugin

# 仅在开发环境启用
if __name__ == '__main__':
    app = dash.Dash(
        __name__,
        plugins=[PerformanceMonitorPlugin()]
    )
    app.run(debug=True)
```

---

## 5. 渲染监控插件

细粒度监控组件重绘（Re-render），优化渲染性能。

```bash
pip install dash-react-scan-plugin
```

```python
from dash_react_scan_plugin import ReactScanPlugin

app = dash.Dash(
    __name__,
    plugins=[ReactScanPlugin()]  # 开发阶段调优使用
)
```

---

## 6. 安全加固插件

禁用 F12、右键菜单、文本复制，防止简单爬虫和调试（生产环境部署时使用）。

```bash
pip install dash-disable-devtool-plugin
```

```python
from dash_disable_devtool_plugin import DisableDevtoolPlugin

# 仅在生产环境启用
import os
plugins = []
if os.getenv('ENV') == 'production':
    plugins.append(DisableDevtoolPlugin())

app = dash.Dash(__name__, plugins=plugins)
```

---

## 7. 断线检测插件

后端服务不可用时，在前端弹出自定义提示。

```bash
pip install dash-offline-detect-plugin
```

```python
from dash_offline_detect_plugin import OfflineDetectPlugin

app = dash.Dash(
    __name__,
    plugins=[OfflineDetectPlugin(message='服务器连接中断，请检查网络')]
)
```

---

## 8. Vite 构建插件

使用 Vite 作为开发服务器，加速启动并启用即时 HMR（热模块替换）。

```bash
pip install dash-vite-plugin
```

```python
from dash_vite_plugin import VitePlugin

app = dash.Dash(
    __name__,
    plugins=[VitePlugin()]  # 开发时启用
)
```

**特点：**
- 启动速度快（相比默认 webpack）
- 即时热更新
- 支持 ESM 模块

---

## 9. Tailwind CSS 插件

在 Python 中直接使用 Tailwind CSS 实用优先样式。

```bash
pip install dash-tailwindcss-plugin
```

```python
from dash_tailwindcss_plugin import TailwindCSSPlugin

app = dash.Dash(
    __name__,
    plugins=[TailwindCSSPlugin()]
)

# 使用 Tailwind 类名
app.layout = html.Div(
    "Hello Tailwind!",
    className='bg-blue-500 text-white p-4 rounded-lg shadow-md'
)
```

---

## 10. 多插件组合使用

```python
import dash
import os

# 根据环境动态配置插件
plugins = []

# 开发环境
if os.getenv('ENV') != 'production':
    from dash_performance_monitor_plugin import PerformanceMonitorPlugin
    from dash_react_scan_plugin import ReactScanPlugin
    plugins.extend([
        PerformanceMonitorPlugin(),
        ReactScanPlugin(),
    ])

# 生产环境
else:
    from dash_disable_devtool_plugin import DisableDevtoolPlugin
    from dash_offline_detect_plugin import OfflineDetectPlugin
    plugins.extend([
        DisableDevtoolPlugin(),
        OfflineDetectPlugin(message='服务暂时不可用'),
    ])

# 通用插件
from dash_change_cdn_plugin import ChangeCDNPlugin
plugins.append(ChangeCDNPlugin(cdn='npmmirror'))

app = dash.Dash(
    __name__,
    serve_locally=False,
    plugins=plugins
)
```

---

## 11. 注意事项

1. **CDN 插件需配合 `serve_locally=False`** 使用
2. **性能/渲染监控插件仅在开发环境使用**，生产环境会影响性能
3. **安全插件仅能防止简单调试**，不能替代服务端安全措施
4. **插件顺序一般不影响功能**，但建议将 CDN 插件放在前面

---

## 相关链接

- dash-change-cdn-plugin: https://github.com/CNFeffery/dash-change-cdn-plugin
- dash-console-filter-plugin: https://github.com/CNFeffery/dash-console-filter-plugin
- dash-performance-monitor-plugin: https://github.com/CNFeffery/dash-performance-monitor-plugin
- dash-react-scan-plugin: https://github.com/CNFeffery/dash-react-scan-plugin
- dash-disable-devtool-plugin: https://github.com/CNFeffery/dash-disable-devtool-plugin
- dash-offline-detect-plugin: https://github.com/CNFeffery/dash-offline-detect-plugin
- dash-vite-plugin: https://github.com/HogaStack/dash-vite-plugin
- dash-tailwindcss-plugin: https://github.com/HogaStack/dash-tailwindcss-plugin

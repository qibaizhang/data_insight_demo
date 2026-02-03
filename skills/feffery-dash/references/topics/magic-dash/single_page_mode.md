# simple-tool 单页面工具应用模板

> magic-dash 单页面工具应用开发模式
> 适用于快速构建"输入 -> 处理 -> 输出"类型的在线小工具

---

## 创建方式

```bash
magic-dash create --name simple-tool
```

---

## 项目结构

```
simple-tool/
├── app.py              # 应用主文件（唯一的 Python 文件）
└── requirements.txt    # 项目依赖信息
```

---

## 启动应用

```bash
pip install -r requirements.txt
python app.py
# 访问 http://127.0.0.1:8050
```

---

## 核心设计理念

该模式旨在快速构建**"输入 -> 处理 -> 输出"**类型的单页面工具应用。

- **视觉风格：** 页面内容居中，采用阴影卡片容器包裹，顶部带有加载进度条
- **交互体验：** 强调操作的实时反馈（Loading 状态、全局消息提示、错误结果页）

---

## 标准布局架构

页面由外向内分为四层结构：

1. **顶部进度条 (`fuc.FefferyTopProgress`):** 监听页面加载状态，提升 UX
2. **居中容器 (`fac.AntdCenter`):** 确保工具面板在页面正中央
3. **全局消息挂载点 (`fac.Fragment`):** 用于通过 `set_props` 触发全局提示
4. **卡片面板 (`fuc.FefferyDiv`):** 工具的主体，包含标题、说明、输入区、操作区和输出区

---

## 代码模板

```python
import dash
from dash import html, set_props
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from dash.dependencies import Input, Output, State

app = dash.Dash(
    __name__,
    update_title=None,
    suppress_callback_exceptions=True,
    title="我的工具",
)

app.layout = fuc.FefferyTopProgress(
    fac.AntdCenter(
        [
            # 1. 全局消息挂载点 (不可见)
            fac.Fragment(id="global-message"),

            # 2. 主面板 (卡片样式)
            fuc.FefferyDiv(
                [
                    # 标题区
                    fac.AntdSpace(
                        [
                            fac.AntdText(
                                "工具标题",
                                style=style(
                                    fontSize=25,
                                    borderLeft="5px solid #1677ff",
                                    paddingLeft=8,
                                ),
                            ),
                            fac.AntdText("工具操作说明...", type="secondary"),
                        ],
                        direction="vertical",
                        size=0,
                    ),
                    fac.AntdDivider(),

                    # 输入区 (根据业务需求替换)
                    fac.AntdInput(id="user-input", mode="text-area"),

                    # 操作区
                    fac.AntdButton(
                        "执行",
                        id="submit-btn",
                        type="primary",
                        block=True,
                        loadingChildren="计算中",
                    ),

                    fac.AntdDivider(),

                    # 结果展示区
                    fac.AntdSpin(
                        html.Div(id="result-container"),
                        text="计算中...",
                    ),
                ],
                # 卡片样式定义
                style=style(
                    border="1px solid #dedede",
                    borderRadius=20,
                    backgroundColor="#fff",
                    width="90vw",
                    boxShadow="50px 50px 100px 10px rgba(0,0,0,.1)",
                    minWidth=600,
                    maxWidth=1200,
                    minHeight="calc(100vh - 120px)",
                    boxSizing="border-box",
                    padding="35px 28px",
                ),
            ),
        ],
        style=style(
            backgroundColor="#fafafa",
            paddingTop=60,
            paddingBottom=60,
        ),
    ),
    listenPropsMode="include",
    includeProps=["result-container.children"],
    minimum=0.4,
)


# 回调函数
@app.callback(
    Output("result-container", "children"),
    Input("submit-btn", "nClicks"),
    State("user-input", "value"),
    running=[(Output("submit-btn", "loading"), True, False)],
    prevent_initial_call=True,
)
def process_input(n_clicks, user_input):
    """处理用户输入"""

    # 输入校验
    if not user_input:
        set_props(
            "global-message",
            {"children": fac.AntdMessage(content="请输入内容", type="error")},
        )
        return fac.AntdResult(
            title="处理失败",
            subTitle="请先完善各项输入值",
            status="error",
        )

    # 处理逻辑（替换为实际业务逻辑）
    result = user_input.upper()

    # 成功提示
    set_props(
        "global-message",
        {"children": fac.AntdMessage(content="处理完成", type="success")},
    )

    return fac.AntdResult(
        title="处理完成",
        subTitle=fac.AntdText(
            ["结果：", fac.AntdText(result, copyable=True)]
        ),
        status="success",
    )


if __name__ == "__main__":
    app.run(debug=True)
```

---

## 交互逻辑模式

### 1. 加载状态管理 (`running` 参数)

当用户点击按钮执行耗时操作时，利用 `@app.callback` 的 `running` 参数自动管理按钮的 `loading` 状态，防止重复点击。

```python
@app.callback(
    ...,
    # 运行时：按钮进入 loading 状态；结束后：恢复正常
    running=[(Output("submit-btn", "loading"), True, False)],
    prevent_initial_call=True
)
```

### 2. 全局消息反馈 (`set_props` + `AntdMessage`)

对于校验失败或操作成功的提示，使用 `set_props` 动态触发全局 Message。

```python
from dash import set_props

# 校验失败
if not valid_input:
    set_props(
        "global-message",
        {"children": fac.AntdMessage(content="参数错误", type="error")}
    )
    # 同时在结果区显示错误状态页
    return fac.AntdResult(status="error", title="计算失败")
```

### 3. 结果展示

- **成功：** 返回具体的组件（如 `fac.AntdResult` 或其他展示组件）
- **失败：** 返回 `fac.AntdResult` 组件，提供友好的错误说明

---

## 适用场景

单页应用模式适合：

1. **快速原型** - 验证想法
2. **简单工具** - 数据转换、编码解码、格式化工具
3. **小型仪表盘** - 单一数据视图
4. **演示 Demo** - 功能展示

---

## 开发规范

### 依赖库导入

```python
import dash
from dash import html, set_props
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style
from dash.dependencies import Input, Output, State
```

### 样式规范

- 标题左侧应带有蓝色竖线装饰 (`borderLeft="5px solid #1677ff"`)
- 面板宽度通常设为 600-1200px
- 使用 `style()` 函数统一管理样式

### 错误处理

回调函数必须包含输入校验逻辑，校验失败时**必须**通过 `set_props` 弹出错误提示。

---

## 何时升级到多页面

当你发现：

1. app.py 超过 500 行代码
2. 有 3 个以上独立的功能区域
3. 需要不同 URL 访问不同功能
4. 回调之间存在大量重复代码
5. 团队协作时频繁冲突

→ 考虑升级到 `magic-dash` 多页面模式

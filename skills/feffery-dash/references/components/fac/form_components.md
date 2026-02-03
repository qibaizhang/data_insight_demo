# FAC 表单组件

> feffery-antd-components 表单类组件详解
> 输入、选择、开关、上传等表单控件

---

## 表单组件概览

### 输入类组件

| 组件 | 说明 | 常用场景 |
|------|------|----------|
| AntdInput | 单行输入框 | 文本输入、搜索、密码 |
| AntdInputNumber | 数字输入框 | 数值输入 |
| AntdTextArea | 多行文本框 | 长文本输入 |
| AntdMentions | @提及输入框 | 评论、消息 |
| AntdOTP | 验证码输入框 | 短信验证、验证码 |

### 选择类组件

| 组件 | 说明 | 常用场景 |
|------|------|----------|
| AntdSelect | 下拉选择器 | 单选/多选 |
| AntdTreeSelect | 树形选择器 | 层级数据选择 |
| AntdCascader | 级联选择器 | 省市区等 |
| AntdRadioGroup | 单选按钮组 | 互斥选项 |
| AntdCheckbox | 复选框 | 单个勾选 |
| AntdCheckboxGroup | 多选框组 | 多选选项 |
| AntdSwitch | 开关 | 开启/关闭 |
| AntdSegmented | 分段控制器 | 视图切换 |

### 日期时间组件

| 组件 | 说明 | 常用场景 |
|------|------|----------|
| AntdDatePicker | 日期选择器 | 单日期选择 |
| AntdDateRangePicker | 日期范围选择器 | 时间段选择 |
| AntdTimePicker | 时间选择器 | 时分秒选择 |
| AntdTimeRangePicker | 时间范围选择器 | 时段选择 |
| AntdCalendar | 日历面板 | 日程展示 |

### 其他表单组件

| 组件 | 说明 | 常用场景 |
|------|------|----------|
| AntdSlider | 滑动条 | 数值范围 |
| AntdRate | 评分 | 星级评价 |
| AntdUpload | 上传组件 | 文件上传 |
| AntdDraggerUpload | 拖拽上传 | 大文件上传 |
| AntdPictureUpload | 图片上传 | 图片选择上传 |
| AntdTransfer | 穿梭框 | 数据转移 |
| AntdColorPicker | 颜色选择器 | 颜色选取 |
| AntdSegmentedColoring | 分段着色 | 数值区间着色 |

---

## AntdForm 表单容器

> **AI快速参考**
> - **用途**: 表单容器组件，支持批量值控制和校验管理
> - **核心参数**: `layout`（布局模式）、`labelCol/wrapperCol`（标签和控件布局）、`enableBatchControl`（批量控制）、`values`（表单值）
> - **回调属性**: `values`（需开启enableBatchControl）

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| id | string | - | 组件唯一id |
| children | Component | - | 内嵌 AntdFormItem 或表单组件 |
| layout | 'horizontal' \| 'vertical' \| 'inline' | 'horizontal' | 表单布局模式 |
| labelCol | dict | - | 标签部分布局，如 `{'span': 4}` |
| wrapperCol | dict | - | 控件部分布局，如 `{'span': 20}` |
| colon | bool | True | 标签末尾是否添加冒号 |
| labelAlign | 'left' \| 'right' | 'right' | 标签文本对齐方式 |
| labelWrap | bool | False | 超长标签是否换行 |
| enableBatchControl | bool | False | 是否启用批量控制 |
| values | dict | - | 表单值（需enableBatchControl=True） |
| validateStatuses | dict | - | 批量设置校验状态 |
| helps | dict | - | 批量设置帮助信息 |

### 基础用法

```python
fac.AntdForm(
    [
        fac.AntdFormItem(
            fac.AntdInput(id='username', placeholder='用户名'),
            label='用户名',
            required=True
        ),
        fac.AntdFormItem(
            fac.AntdInput(id='password', mode='password'),
            label='密码',
            required=True
        ),
        fac.AntdFormItem(
            fac.AntdButton('登录', type='primary', id='login-btn'),
            wrapperCol={'offset': 4}
        )
    ],
    labelCol={'span': 4},
    wrapperCol={'span': 20},
    style={'width': 400}
)
```

### 批量值控制

```python
fac.AntdForm(
    [
        fac.AntdFormItem(
            fac.AntdInput(name='username'),  # 注意使用 name 而非 id
            label='用户名'
        ),
        fac.AntdFormItem(
            fac.AntdInput(name='email'),
            label='邮箱'
        )
    ],
    id='my-form',
    enableBatchControl=True,
    values={'username': '默认用户名', 'email': 'test@example.com'}
)

# 监听表单值变化
@callback(
    Output('output', 'children'),
    Input('my-form', 'values')
)
def show_values(values):
    return f"当前表单值: {values}"
```

---

## AntdFormItem 表单项

> **AI快速参考**
> - **用途**: 表单项包装组件，提供标签、校验状态和帮助信息
> - **核心参数**: `label`（标签）、`required`（必填标识）、`validateStatus`（校验状态）、`help`（帮助信息）

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| children | Component | - | 内嵌的表单输入组件 |
| label | Component | - | 标签内容 |
| required | bool | False | 是否显示必填"*"标识 |
| labelCol | dict | - | 标签布局（覆盖Form设置） |
| wrapperCol | dict | - | 控件布局（覆盖Form设置） |
| colon | bool | - | 是否显示冒号 |
| tooltip | Component | - | 标签后的提示信息 |
| extra | Component | - | 额外提示信息 |
| validateStatus | 'success' \| 'warning' \| 'error' \| 'validating' | - | 校验状态 |
| hasFeedback | bool | False | 是否显示状态图标 |
| help | Component | - | 校验说明信息 |
| hidden | bool | False | 是否隐藏 |

### 表单验证

```python
# 带验证状态的表单项
fac.AntdFormItem(
    fac.AntdInput(id='phone'),
    label='手机号',
    id='phone-item',
    required=True,
    validateStatus='error',
    help='请输入正确的手机号格式',
    hasFeedback=True
)

# 回调验证
@callback(
    Output('phone-item', 'validateStatus'),
    Output('phone-item', 'help'),
    Input('phone', 'value')
)
def validate_phone(phone):
    if not phone:
        return 'error', '手机号不能为空'
    if not re.match(r'^1[3-9]\d{9}$', phone):
        return 'error', '手机号格式不正确'
    return 'success', None
```

---

## AntdInput 输入框

> **AI快速参考**
> - **核心参数**: `value`, `mode`, `placeholder`, `debounceValue`, `allowClear`
> - **回调属性**: `value`, `debounceValue`, `nSubmit`

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | string | - | 输入值 |
| defaultValue | string | - | 默认值 |
| mode | 'default' \| 'search' \| 'text-area' \| 'password' | 'default' | 输入框模式 |
| placeholder | string | - | 占位提示 |
| allowClear | bool | False | 允许清除 |
| maxLength | number | - | 最大长度 |
| showCount | bool | False | 显示字数 |
| disabled | bool | False | 禁用 |
| readOnly | bool | False | 只读 |
| addonBefore | Component | - | 前置标签 |
| addonAfter | Component | - | 后置标签 |
| prefix | Component | - | 前缀图标 |
| suffix | Component | - | 后缀图标 |
| debounceWait | number | 0 | 防抖延迟(ms) |

### 常用示例

```python
# 基础输入框
fac.AntdInput(
    id='my-input',
    placeholder='请输入...',
    allowClear=True,
    maxLength=100,
    showCount=True
)

# 密码输入框
fac.AntdInput(
    id='password-input',
    mode='password',
    placeholder='请输入密码'
)

# 搜索框
fac.AntdInput(
    id='search-input',
    mode='search',
    placeholder='搜索...'
)

# 前后缀
fac.AntdInput(
    id='url-input',
    addonBefore='https://',
    addonAfter='.com',
    placeholder='网站名'
)

# 防抖输入（减少回调频率）
fac.AntdInput(
    id='debounce-input',
    debounceWait=300,
    placeholder='输入后300ms触发回调'
)

@callback(
    Output('result', 'children'),
    Input('debounce-input', 'debounceValue')  # 使用 debounceValue
)
def handle_input(value):
    return f"输入: {value}"
```

---

## AntdSelect 选择器

> **AI快速参考**
> - **核心参数**: `value`, `options`, `mode`, `allowClear`, `placeholder`
> - **回调属性**: `value`, `searchValue`

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | any | - | 选中值 |
| options | list[dict] | - | 选项列表 |
| mode | 'multiple' \| 'tags' | - | 多选/标签模式 |
| placeholder | string | - | 占位提示 |
| allowClear | bool | False | 允许清除 |
| disabled | bool | False | 禁用 |
| maxTagCount | number \| 'responsive' | - | 最多显示标签数 |
| optionFilterProp | 'value' \| 'label' | 'value' | 搜索字段 |
| autoSpin | bool | False | 自动加载动画 |
| debounceWait | number | 0 | 搜索防抖(ms) |

### 常用示例

```python
# 基础选择
fac.AntdSelect(
    id='my-select',
    options=[
        {'label': '选项1', 'value': '1'},
        {'label': '选项2', 'value': '2'},
        {'label': '选项3', 'value': '3', 'disabled': True},
    ],
    placeholder='请选择',
    allowClear=True
)

# 多选模式
fac.AntdSelect(
    id='multi-select',
    options=[...],
    mode='multiple',
    maxTagCount=3,
    placeholder='请选择多个'
)

# 分组选项
fac.AntdSelect(
    id='grouped-select',
    options=[
        {
            'group': '水果',
            'options': [
                {'label': '苹果', 'value': 'apple'},
                {'label': '香蕉', 'value': 'banana'},
            ]
        },
        {
            'group': '蔬菜',
            'options': [
                {'label': '番茄', 'value': 'tomato'},
                {'label': '黄瓜', 'value': 'cucumber'},
            ]
        }
    ]
)

# 远程搜索
fac.AntdSelect(
    id='remote-select',
    options=[],
    mode='multiple',
    autoSpin=True,
    debounceWait=300
)

@callback(
    Output('remote-select', 'options'),
    Input('remote-select', 'searchValue'),
    prevent_initial_call=True
)
def search_options(keyword):
    # 远程搜索逻辑
    return fetch_options(keyword)
```

---

## AntdDatePicker 日期选择器

> **AI快速参考**
> - **核心参数**: `value`, `picker`, `format`, `showTime`, `disabledDatesStrategy`
> - **回调属性**: `value`

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| value | string | - | 选中日期 |
| picker | 'date' \| 'week' \| 'month' \| 'quarter' \| 'year' | 'date' | 选择器类型 |
| format | string | 'YYYY-MM-DD' | 日期格式 |
| showTime | bool \| dict | False | 显示时间选择 |
| placeholder | string | - | 占位提示 |
| allowClear | bool | True | 允许清除 |
| disabled | bool | False | 禁用 |
| disabledDatesStrategy | list[dict] | - | 禁用日期策略 |

### 常用示例

```python
# 基础日期选择
fac.AntdDatePicker(
    id='date-picker',
    placeholder='选择日期',
    locale='zh-cn'
)

# 带时间的日期选择
fac.AntdDatePicker(
    id='datetime-picker',
    showTime=True,
    format='YYYY-MM-DD HH:mm:ss'
)

# 日期范围选择
fac.AntdDateRangePicker(
    id='date-range',
    placeholder=['开始日期', '结束日期'],
    locale='zh-cn'
)

# 禁用日期（禁用今天之前的日期）
fac.AntdDatePicker(
    id='future-date',
    disabledDatesStrategy=[
        {'mode': 'lt', 'target': 'today'}
    ]
)

# 禁用特定日期
fac.AntdDatePicker(
    id='special-date',
    disabledDatesStrategy=[
        {'mode': 'in-enumerate-dates', 'value': ['2024-01-01', '2024-12-25']}
    ]
)
```

---

## AntdUpload 上传组件

> **AI快速参考**
> - **核心参数**: `apiUrl`, `fileTypes`, `fileMaxSize`, `multiple`
> - **回调属性**: `lastUploadTaskRecord`, `listUploadTaskRecord`

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| apiUrl | string | - | 上传接口地址 |
| fileTypes | list[string] | - | 允许的文件类型 |
| fileMaxSize | number | - | 最大文件大小(MB) |
| fileListMaxLength | number | - | 最大文件数量 |
| multiple | bool | False | 是否多选 |
| directory | bool | False | 是否上传目录 |
| buttonContent | Component | - | 上传按钮内容 |
| showUploadList | bool | True | 显示上传列表 |

### 常用示例

```python
# 基础上传
fac.AntdUpload(
    id='file-upload',
    apiUrl='/upload',
    fileTypes=['image/png', 'image/jpeg'],
    fileMaxSize=5,  # MB
    buttonContent='点击上传'
)

# 拖拽上传
fac.AntdDraggerUpload(
    id='dragger-upload',
    apiUrl='/upload',
    text='拖拽文件到此处',
    hint='支持 PNG、JPG 格式，最大 10MB'
)

# 图片上传
fac.AntdPictureUpload(
    id='picture-upload',
    apiUrl='/upload',
    fileTypes=['image/png', 'image/jpeg'],
    fileMaxSize=2,
    fileListMaxLength=5
)

# 上传回调处理
@callback(
    Output('upload-result', 'children'),
    Input('file-upload', 'lastUploadTaskRecord'),
    prevent_initial_call=True
)
def handle_upload(record):
    if record and record['taskStatus'] == 'success':
        return f"上传成功: {record['fileName']}"
    return "上传失败"
```

---

## 其他表单组件速查

### AntdSwitch 开关

```python
fac.AntdSwitch(
    id='my-switch',
    checked=False,
    checkedChildren='开',
    unCheckedChildren='关'
)
```

### AntdSlider 滑动条

```python
fac.AntdSlider(
    id='my-slider',
    min=0,
    max=100,
    value=50,
    marks={0: '0%', 50: '50%', 100: '100%'}
)

# 范围选择
fac.AntdSlider(
    id='range-slider',
    range=True,
    value=[20, 80]
)
```

### AntdRate 评分

```python
fac.AntdRate(
    id='my-rate',
    count=5,
    allowHalf=True,
    value=3.5
)
```

### AntdRadioGroup 单选组

```python
fac.AntdRadioGroup(
    id='my-radio',
    options=[
        {'label': '选项A', 'value': 'a'},
        {'label': '选项B', 'value': 'b'},
        {'label': '选项C', 'value': 'c'},
    ],
    value='a'
)
```

### AntdCheckboxGroup 多选组

```python
fac.AntdCheckboxGroup(
    id='my-checkbox',
    options=[
        {'label': '选项1', 'value': '1'},
        {'label': '选项2', 'value': '2'},
        {'label': '选项3', 'value': '3'},
    ],
    value=['1', '2']
)
```

### AntdTransfer 穿梭框

```python
fac.AntdTransfer(
    id='my-transfer',
    dataSource=[
        {'key': str(i), 'title': f'选项{i}'} for i in range(10)
    ],
    targetKeys=['1', '3', '5'],
    titles=['源列表', '目标列表']
)
```

### AntdColorPicker 颜色选择器

```python
fac.AntdColorPicker(
    id='my-color',
    value='#1890ff',
    format='hex'
)
```

---

## 表单数据收集

### 方式1：使用 State 批量获取

```python
@callback(
    Output('result', 'children'),
    Input('submit-btn', 'nClicks'),
    State('username', 'value'),
    State('email', 'value'),
    State('role', 'value'),
    prevent_initial_call=True
)
def submit_form(n, username, email, role):
    form_data = {
        'username': username,
        'email': email,
        'role': role
    }
    return f"提交数据: {form_data}"
```

### 方式2：使用 enableBatchControl

```python
fac.AntdForm(
    [...],
    id='my-form',
    enableBatchControl=True
)

@callback(
    Output('result', 'children'),
    Input('submit-btn', 'nClicks'),
    State('my-form', 'values'),
    prevent_initial_call=True
)
def submit_form(n, values):
    return f"提交数据: {values}"
```

---

## 参考资源

- [feffery-antd-components 官方文档](https://fac.feffery.tech/)
- [Ant Design Form 官方文档](https://ant.design/components/form-cn)

# magic-dash CLI 命令速查

> magic-dash 命令行工具速查表
> 快速创建 Dash 应用项目

---

## 安装

```bash
pip install magic-dash -U
```

---

## 核心命令

### 查看内置模板

```bash
magic-dash list
```

### 创建项目

```bash
# 基础语法
magic-dash create --name <模板名称>

# 指定目标路径创建
magic-dash create --name <模板名称> --path <目标路径>
```

### 三个内置模板

| 模板名称 | 命令 | 说明 |
|---------|------|------|
| `simple-tool` | `magic-dash create --name simple-tool` | 单页面工具应用 |
| `magic-dash` | `magic-dash create --name magic-dash` | 基础多页面应用 |
| `magic-dash-pro` | `magic-dash create --name magic-dash-pro` | 多页面+用户登录应用 |

---

## 创建项目示例

### 1. 单页面工具应用

```bash
# 创建单页面工具项目
magic-dash create --name simple-tool

# 进入项目并启动
cd simple-tool
pip install -r requirements.txt
python app.py
```

### 2. 多页面应用

```bash
# 创建多页面应用项目
magic-dash create --name magic-dash

# 进入项目并启动
cd magic-dash
pip install -r requirements.txt
python app.py
```

### 3. 多页面登录应用

```bash
# 创建带登录的多页面应用
magic-dash create --name magic-dash-pro

# 进入项目
cd magic-dash-pro

# 安装依赖
pip install -r requirements.txt

# 初始化数据库（必须步骤）
python -m models.init_db

# 启动应用
python app.py

# 默认管理员账号: admin / admin123
```

---

## 版本和帮助

```bash
# 查看版本
magic-dash --version

# 查看帮助
magic-dash --help
magic-dash list --help
magic-dash create --help
```

---

## 生产部署

```bash
# 使用 gunicorn 启动（推荐）
gunicorn server:server -b 0.0.0.0:8050 -w 4
```

---

## 常见问题

### Q: 创建失败怎么办？

1. 检查 Python 版本（需要 3.8 - 3.13）
2. 更新 magic-dash：`pip install magic-dash -U`
3. 检查目标路径是否已存在同名文件夹

### Q: 如何更新 magic-dash？

```bash
pip install magic-dash -U
```

### Q: 应用依赖版本要求？

magic-dash 模板要求以下依赖版本：
- `dash>=3.3.0,<4.0.0`
- `feffery_antd_components>=0.4.0,<0.5.0`
- `feffery_utils_components>=0.3.2,<0.4.0`
- `feffery_dash_utils>=0.2.6`

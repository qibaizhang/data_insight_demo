# DataInsight Demo - AI 数据分析助手

基于 feffery-dash 和 agno 构建的智能数据分析 Web 应用演示，支持自然语言数据查询、可视化和报告生成。

## 功能特性

### 核心功能

- **🤖 自然语言查询**：通过对话方式查询数据，AI 自动生成 SQL
- **📊 数据可视化**：支持多种图表类型（折线图、柱状图、饼图等）
- **📈 信息图生成**：使用 feffery-infographic 生成专业信息图
- **📝 分析报告**：自动生成 Markdown 格式的数据分析报告
- **💾 数据导出**：支持 CSV 数据导出和 Markdown 报告下载

### 技术特性

- **SQLite 演示数据库**：内置电商演示数据
- **流式响应**：基于 SSE 的实时流式输出
- **会话管理**：本地持久化的会话存储
- **Schema 管理**：自动发现 + 手动配置的混合模式
- **安全查询**：只读 SQL 验证，防止数据修改

## 技术栈

| 类别 | 技术 |
|------|------|
| 前端框架 | Dash + feffery-antd-components (fac) |
| UI 工具 | feffery-utils-components (fuc) |
| 数据图表 | feffery-antd-charts (fact) |
| 信息图 | feffery-infographic (fi) |
| AI 框架 | agno |
| LLM 支持 | OpenAI API (兼容协议) |
| 数据库 | SQLite |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

必需配置：

```env
# LLM 配置 (必填) 兼容openai协议的模型都可以
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=your-model-name
AVAILABLE_MODELS=model1,model2,model3

# 可选：记忆提取使用的模型（默认使用 DEFAULT_MODEL）
MEMORY_MODEL=
```

### 3. 初始化演示数据库

```bash
python init_database.py
```

### 4. 启动应用

```bash
python app.py
```

访问 http://localhost:8050

## 演示数据库

演示数据库包含以下表：

| 表名 | 描述 | 记录数 |
|------|------|--------|
| users | 用户信息表 | 10 |
| products | 商品表 | 15 |
| orders | 订单表 | 100 |
| order_items | 订单明细表 | ~200 |
| page_views | 页面访问表 | 500 |

## 功能演示指南

本应用支持四种主要输出类型，每种类型会在右侧对应的面板中展示：

### 📋 1. 数据表查询（激活「数据」面板）

直接查询数据，结果显示在右侧「数据」Tab 中。

**测试示例：**

```
查询所有用户信息
```

```
显示最近10笔订单
```

```
查看销量前5的商品
```

```
统计每个用户的订单数量
```

---

### 📊 2. 图表可视化（激活「图表」面板）

生成数据图表，结果显示在右侧「图表」Tab 中。

**测试示例：**

```
用折线图展示每日订单数量趋势
```

```
用柱状图展示各商品类别的销售额
```

```
用饼图展示订单状态分布
```

```
生成用户注册时间的趋势图
```

---

### 📝 3. Markdown 报告（激活「报告」面板）

生成结构化的 Markdown 分析报告，结果显示在右侧「报告」Tab 中。

**测试示例：**

```
生成一份销售数据分析报告
```

```
生成业务概览报告，包括用户、订单、商品等维度
```

```
做一份本月的数据洞察总结
```

```
生成一份 Markdown 格式的订单分析报告
```

---

### 📈 4. 信息图报告（激活「报告」面板）

生成可视化的信息图报告（类似 PPT 风格的卡片式展示），结果显示在右侧「报告」Tab 中。

**测试示例：**

```
用信息图展示销售数据概览
```

```
用信息图的方式展示关键业务指标
```

```
生成一个像PPT那样的数据概览卡片
```

```
用卡片式信息图展示用户和订单统计
```

---

## 输出类型对照表

| 用户意图 | 关键词 | 输出位置 | 展示形式 |
|----------|--------|----------|----------|
| 查询数据 | 查询、显示、查看、统计 | 数据 Tab | 表格 |
| 生成图表 | 折线图、柱状图、饼图、趋势图 | 图表 Tab | 交互式图表 |
| Markdown 报告 | 报告、洞察、总结、概览 | 报告 Tab | Markdown 渲染 |
| 信息图报告 | 信息图、像PPT、卡片式、可视化报告 | 报告 Tab | 信息图组件 |

## Schema 配置

在 `data/schema/sqlite.yaml` 中配置表和字段的描述信息：

```yaml
tables:
  users:
    description: "用户信息表"
    columns:
      - name: id
        type: INTEGER
        description: "用户唯一标识"
      - name: username
        type: TEXT
        description: "用户名"
```

## 数据导出

- 在「数据」Tab 点击「导出 CSV」下载查询结果
- 在「报告」Tab 点击「导出 Markdown」下载报告文档

## API 接口

### SSE 流式聊天

```
GET /api/chat/stream
```

参数：
- `message`: 用户消息（必需）
- `session_id`: 会话 ID
- `datasource`: 数据源类型（固定为 sqlite）
- `model`: 模型 ID

### 会话管理

```
GET  /api/chat/sessions          # 列出所有会话
GET  /api/chat/sessions/{id}     # 获取会话详情
DELETE /api/chat/sessions/{id}   # 删除会话
```

## 项目结构

```
DataInsight/
├── app.py                 # 应用入口
├── server.py              # Dash/Flask 服务器
├── config.py              # 配置管理
├── requirements.txt       # Python 依赖
├── .env.example          # 环境变量示例
│
├── api/                   # API 端点
│   └── chat_api.py       # SSE 聊天接口
│
├── views/                 # 视图组件
│   ├── main_layout.py    # 主布局
│   ├── chat_panel.py     # 聊天面板
│   ├── session_list.py   # 会话列表
│   └── display_panel.py  # 展示面板
│
├── callbacks/             # 回调函数
│   ├── chat_c.py         # 聊天回调
│   ├── session_c.py      # 会话回调
│   ├── display_c.py      # 展示回调
│   └── export_c.py       # 导出回调
│
├── agent/                 # AI Agent
│   ├── data_insight_agent.py  # Agent 定义
│   ├── tools/            # 工具集
│   │   ├── sql_query_tool.py  # SQL 查询
│   │   ├── chart_tool.py      # 图表生成
│   │   ├── report_tool.py     # 报告生成
│   │   └── export_tool.py     # 数据导出
│   └── prompts/          # 提示词
│       └── system_prompt.py
│
├── services/              # 业务服务
│   ├── database_service.py    # 数据库连接
│   ├── schema_service.py      # Schema 管理
│   └── session_service.py     # 会话管理
│
├── utils/                 # 工具函数
│   ├── sql_validator.py  # SQL 验证
│   └── helpers.py        # 辅助函数
│
├── assets/               # 静态资源
│   └── base.css         # 基础样式
│
└── data/                 # 数据目录
    ├── database.db      # SQLite 演示数据库
    ├── schema/          # Schema 配置
    │   └── sqlite.yaml
    └── sessions.db      # 会话存储
```

## 开发说明

### 添加新工具

1. 在 `agent/tools/` 中创建新的 Toolkit 类
2. 在 `data_insight_agent.py` 中注册工具

### 自定义图表

在 `agent/tools/chart_tool.py` 中扩展 `generate_chart_config` 方法支持更多图表类型。

## 许可证

MIT License

# 工具系统完整指南

## 目录

- [工具概述](#工具概述)
- [内置工具库](#内置工具库)
- [自定义工具](#自定义工具)
- [Toolkit 工具包](#toolkit-工具包)
- [工具配置选项](#工具配置选项)
- [工具调用控制](#工具调用控制)
- [实战示例](#实战示例)

## 工具概述

工具让 Agent 能够执行实际操作：获取数据、调用 API、执行代码等。Agno 提供 100+ 内置工具，同时支持自定义工具。

### 工具类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **Function** | 单个可调用函数 | 简单操作 |
| **Toolkit** | 相关工具集合 | 领域功能集 |

## 内置工具库

### 金融数据

```python
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[YFinanceTools(
        stock_price=True,           # 股价
        stock_fundamentals=True,    # 基本面
        analyst_recommendations=True,  # 分析师建议
        company_news=True,          # 公司新闻
        historical_prices=True      # 历史价格
    )]
)
```

### 网络搜索

```python
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools
from agno.tools.exa import ExaTools

agent = Agent(
    tools=[
        DuckDuckGoTools(),          # 免费搜索
        TavilyTools(),              # AI 优化搜索
        ExaTools(),                 # 语义搜索
    ]
)
```

### 网页处理

```python
from agno.tools.website import WebsiteTools
from agno.tools.firecrawl import FirecrawlTools

agent = Agent(
    tools=[
        WebsiteTools(),             # 基础网页读取
        FirecrawlTools(),           # 高级爬虫
    ]
)
```

### 代码执行

```python
from agno.tools.python import PythonTools
from agno.tools.shell import ShellTools

agent = Agent(
    tools=[
        PythonTools(),              # Python 执行
        ShellTools(),               # Shell 命令
    ]
)
```

### 数据库

```python
from agno.tools.sql import SqlTools
from agno.tools.postgres import PostgresTools
from agno.tools.duckdb import DuckDBTools

agent = Agent(
    tools=[
        SqlTools(db_url="sqlite:///data.db"),
        PostgresTools(connection_string="postgresql://..."),
        DuckDBTools(),
    ]
)
```

### 文件操作

```python
from agno.tools.file import FileTools
from agno.tools.csv import CsvTools
from agno.tools.json import JsonTools
from agno.tools.pdf import PdfTools

agent = Agent(
    tools=[
        FileTools(base_dir="./data"),
        CsvTools(),
        JsonTools(),
        PdfTools(),
    ]
)
```

### 通信

```python
from agno.tools.slack import SlackTools
from agno.tools.email import EmailTools
from agno.tools.discord import DiscordTools

agent = Agent(
    tools=[
        SlackTools(token="xoxb-..."),
        EmailTools(smtp_server="smtp.gmail.com"),
        DiscordTools(token="..."),
    ]
)
```

### 代码仓库

```python
from agno.tools.github import GithubTools
from agno.tools.gitlab import GitlabTools

agent = Agent(
    tools=[
        GithubTools(token="ghp_..."),
        GitlabTools(token="..."),
    ]
)
```

### AI 服务

```python
from agno.tools.openai import OpenAITools
from agno.tools.replicate import ReplicateTools

agent = Agent(
    tools=[
        OpenAITools(),              # DALL-E 图像生成
        ReplicateTools(),           # 各种 AI 模型
    ]
)
```

### 完整工具列表

| 类别 | 工具 |
|------|------|
| **金融** | YFinanceTools, AlphaVantageTools |
| **搜索** | DuckDuckGoTools, GoogleSearch, TavilyTools, ExaTools, SerpApiTools |
| **网页** | WebsiteTools, FirecrawlTools, Spider |
| **数据库** | SqlTools, PostgresTools, MySqlTools, DuckDBTools, MongoDbTools |
| **文件** | FileTools, CsvTools, JsonTools, PdfTools, ExcelTools |
| **代码** | PythonTools, ShellTools, GithubTools, GitlabTools |
| **通信** | SlackTools, EmailTools, DiscordTools, TelegramTools |
| **云服务** | AwsTools, GcpTools, AzureTools |
| **AI** | OpenAITools, ReplicateTools, HuggingFaceTools |
| **其他** | CalendarTools, WeatherTools, NewsTools |

## 自定义工具

### 使用装饰器

```python
from agno.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称

    Returns:
        天气描述
    """
    # 实际实现会调用天气 API
    return f"{city}: 晴朗，25°C"

@tool
def calculate_bmi(weight: float, height: float) -> dict:
    """计算 BMI 指数。

    Args:
        weight: 体重（公斤）
        height: 身高（米）

    Returns:
        包含 BMI 值和分类的字典
    """
    bmi = weight / (height ** 2)
    category = "正常" if 18.5 <= bmi < 24 else "偏高" if bmi >= 24 else "偏低"
    return {"bmi": round(bmi, 1), "category": category}

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[get_weather, calculate_bmi]
)
```

### 工具装饰器选项

```python
@tool(
    name="weather_lookup",           # 自定义名称
    show_result=True,                # 显示结果给用户
    requires_confirmation=True,      # 需要用户确认
    cache_results=True,              # 缓存结果
    cache_ttl=3600,                  # 缓存时间（秒）
)
def get_weather(city: str) -> str:
    """获取天气信息。"""
    return f"{city}: 晴朗"
```

### 异步工具

```python
import aiohttp

@tool
async def fetch_data(url: str) -> str:
    """异步获取 URL 数据。

    Args:
        url: 要获取的 URL

    Returns:
        响应内容
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### 使用 Function 类

```python
from agno.tools.function import Function

def search_knowledge(query: str, limit: int = 5) -> list:
    """搜索知识库"""
    return [{"title": "结果1", "content": "..."}]

search_function = Function(
    name="search_knowledge",
    description="搜索内部知识库获取相关信息",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索查询"},
            "limit": {"type": "integer", "default": 5, "description": "返回数量"}
        },
        "required": ["query"]
    },
    entrypoint=search_knowledge,
    requires_confirmation=False,
    show_result=True,
)

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[search_function]
)
```

## Toolkit 工具包

### 创建 Toolkit

```python
from agno.tools import Toolkit

class WeatherToolkit(Toolkit):
    def __init__(self, api_key: str):
        super().__init__(
            name="天气工具包",
            instructions="使用这些工具获取天气信息",
        )
        self.api_key = api_key

        # 注册工具
        self.register(self.get_current_weather)
        self.register(self.get_forecast)

    def get_current_weather(self, city: str) -> dict:
        """获取当前天气。

        Args:
            city: 城市名称

        Returns:
            天气数据字典
        """
        # API 调用
        return {"city": city, "temp": 25, "condition": "晴朗"}

    def get_forecast(self, city: str, days: int = 7) -> list:
        """获取天气预报。

        Args:
            city: 城市名称
            days: 预报天数

        Returns:
            预报数据列表
        """
        return [{"day": i, "temp": 20+i} for i in range(days)]

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[WeatherToolkit(api_key="...")]
)
```

### Toolkit 高级配置

```python
class TradingToolkit(Toolkit):
    def __init__(self, api_key: str, sandbox: bool = True):
        super().__init__(
            name="交易工具包",
            instructions="用于股票交易操作的工具",

            # 需要确认的危险操作
            requires_confirmation_tools=["execute_trade", "cancel_order"],

            # 需要外部执行的操作
            external_execution_required_tools=["submit_order"],
        )
        self.api_key = api_key
        self.sandbox = sandbox

        self.register(self.get_portfolio)
        self.register(self.execute_trade)
        self.register(self.cancel_order)

    def get_portfolio(self) -> dict:
        """获取当前持仓。"""
        return {"holdings": [...], "cash": 10000}

    def execute_trade(self, symbol: str, quantity: int, action: str) -> dict:
        """执行交易（需要确认）。

        Args:
            symbol: 股票代码
            quantity: 数量
            action: BUY 或 SELL
        """
        if self.sandbox:
            return {"status": "模拟交易成功", "order_id": "SIM001"}
        # 实际交易逻辑
        return {"status": "success", "order_id": "..."}

    def cancel_order(self, order_id: str) -> dict:
        """取消订单（需要确认）。"""
        return {"status": "cancelled", "order_id": order_id}
```

## 工具配置选项

### Agent 工具配置

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[...],

    # 工具调用限制
    tool_call_limit=10,              # 单次运行最多调用次数

    # 工具选择策略
    tool_choice="auto",              # auto/none/required/specific

    # 特殊工具
    read_chat_history=False,         # 读取聊天历史的工具
    search_knowledge=True,           # 搜索知识库的工具
    update_knowledge=False,          # 更新知识库的工具
    read_tool_call_history=False,    # 读取工具调用历史
)
```

### 工具选择策略

```python
# 自动选择（默认）
agent = Agent(tools=[...], tool_choice="auto")

# 禁止工具调用
agent = Agent(tools=[...], tool_choice="none")

# 必须调用工具
agent = Agent(tools=[...], tool_choice="required")

# 强制特定工具
agent = Agent(
    tools=[get_weather, calculate_bmi],
    tool_choice={"type": "function", "function": {"name": "get_weather"}}
)
```

## 工具调用控制

### 确认机制

```python
@tool(requires_confirmation=True)
def delete_file(path: str) -> str:
    """删除文件（危险操作）。"""
    import os
    os.remove(path)
    return f"已删除: {path}"

# 人工确认流程
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[delete_file],
)

response = agent.run("删除 temp.txt")
# Agent 会请求确认后再执行
```

### 外部执行

```python
class PaymentToolkit(Toolkit):
    def __init__(self):
        super().__init__(
            name="支付工具",
            external_execution_required_tools=["process_payment"]
        )
        self.register(self.process_payment)

    def process_payment(self, amount: float, recipient: str) -> dict:
        """处理支付（需要外部系统执行）。"""
        # 返回执行指令，由外部系统处理
        return {
            "action": "payment",
            "amount": amount,
            "recipient": recipient,
            "instructions": "请在支付系统中确认此交易"
        }
```

### 工具结果处理

```python
@tool(show_result=True)  # 向用户显示结果
def analyze_data(data: list) -> dict:
    """分析数据。"""
    return {"average": sum(data)/len(data), "count": len(data)}

@tool(show_result=False)  # 仅供 Agent 内部使用
def fetch_internal_config() -> dict:
    """获取内部配置。"""
    return {"api_endpoint": "...", "timeout": 30}
```

## 实战示例

### 研究助手

```python
from agno.agent import Agent
from agno.models.openai import OpenAI
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.website import WebsiteTools
from agno.tools import tool

@tool
def save_notes(topic: str, content: str) -> str:
    """保存研究笔记。

    Args:
        topic: 主题
        content: 笔记内容
    """
    with open(f"notes/{topic}.md", "w") as f:
        f.write(content)
    return f"笔记已保存: {topic}"

research_agent = Agent(
    name="研究助手",
    model=OpenAI(id="gpt-4o"),
    tools=[
        DuckDuckGoTools(),
        WebsiteTools(),
        save_notes
    ],
    instructions="""
    你是研究助手，帮助用户：
    1. 搜索相关信息
    2. 阅读和总结网页
    3. 保存研究笔记
    """,
    markdown=True
)

research_agent.print_response("研究一下 AI Agent 的最新发展趋势", stream=True)
```

### 数据分析助手

```python
from agno.tools.python import PythonTools
from agno.tools.csv import CsvTools
from agno.tools.file import FileTools

data_agent = Agent(
    name="数据分析师",
    model=OpenAI(id="gpt-4o"),
    tools=[
        PythonTools(),
        CsvTools(),
        FileTools(base_dir="./data")
    ],
    instructions="""
    你是数据分析师，能够：
    1. 读取 CSV 数据文件
    2. 使用 Python 进行数据分析
    3. 生成可视化图表
    4. 保存分析结果

    使用 pandas, matplotlib 进行分析和可视化。
    """
)

data_agent.print_response("分析 sales.csv 中的月度销售趋势", stream=True)
```

### 客服机器人

```python
from agno.tools import tool, Toolkit

class CustomerServiceToolkit(Toolkit):
    def __init__(self, db):
        super().__init__(name="客服工具")
        self.db = db
        self.register(self.lookup_order)
        self.register(self.check_inventory)
        self.register(self.create_ticket)

    def lookup_order(self, order_id: str) -> dict:
        """查询订单状态。"""
        return self.db.get_order(order_id)

    def check_inventory(self, product_id: str) -> dict:
        """检查库存。"""
        return self.db.get_inventory(product_id)

    def create_ticket(self, issue: str, priority: str = "normal") -> dict:
        """创建工单。"""
        return self.db.create_ticket(issue, priority)

service_agent = Agent(
    name="客服助手",
    model=OpenAI(id="gpt-4o"),
    tools=[CustomerServiceToolkit(db=customer_db)],
    instructions="""
    你是友好的客服助手，帮助客户：
    - 查询订单状态
    - 检查产品库存
    - 处理投诉和问题

    始终保持礼貌和专业。
    """
)
```

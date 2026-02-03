# Agent 核心配置详解

## 目录

- [Agent 初始化](#agent-初始化)
- [身份与角色](#身份与角色)
- [指令系统](#指令系统)
- [上下文管理](#上下文管理)
- [会话管理](#会话管理)
- [输入输出控制](#输入输出控制)
- [推理模式](#推理模式)
- [守卫与钩子](#守卫与钩子)
- [运行方法](#运行方法)
- [完整配置示例](#完整配置示例)

## Agent 初始化

### 基础配置

```python
from agno.agent import Agent
from agno.models.openai import OpenAI

agent = Agent(
    # 必需
    model=OpenAI(id="gpt-4o"),

    # 身份
    name="我的助手",
    id="agent-001",           # 唯一标识符
    user_id="default-user",   # 默认用户ID

    # 角色定义
    role="金融分析师",
    description="专业的金融市场分析专家",

    # 工具
    tools=[...],

    # 存储
    db=SqliteDb(db_file="agents.db"),
)
```

## 身份与角色

### 核心身份字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | str | Agent 名称，用于日志和显示 |
| `id` | str | 唯一标识符，用于持久化 |
| `role` | str | 角色描述，影响行为风格 |
| `description` | str | 详细描述，添加到系统提示 |

```python
agent = Agent(
    name="投资顾问",
    id="investment-advisor-v1",
    role="注册投资顾问",
    description="""
    你是一位经验丰富的投资顾问，具备：
    - CFA 认证
    - 10年市场分析经验
    - 专注于价值投资策略
    """
)
```

## 指令系统

### 指令配置

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),

    # 基础指令
    instructions="你是专业的数据分析师。",

    # 或使用列表形式
    instructions=[
        "你是专业的数据分析师",
        "使用清晰的结构化格式回复",
        "始终引用数据来源"
    ],

    # 额外指令（追加）
    additional_instructions="回复时使用 Markdown 格式",

    # 期望输出格式
    expected_output="""
    ## 分析结果
    - 关键发现
    - 数据支持
    - 建议行动
    """
)
```

### 指令最佳实践

```python
# 结构化指令示例
instructions = """
## 角色
你是专业的金融分析师。

## 工作流程
1. 理解用户查询
2. 使用工具获取数据
3. 分析并得出结论
4. 结构化呈现结果

## 输出规则
- 使用表格展示数值数据
- 标注数据时间戳
- 不提供具体投资建议

## 限制
- 仅使用提供的工具
- 缺失数据标记为 "N/A"
"""
```

## 上下文管理

### 时间与位置上下文

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),

    # 时间上下文
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",  # 时区

    # 位置上下文
    add_location_to_context=True,
)
```

### 历史上下文

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=SqliteDb(db_file="agents.db"),

    # 历史消息
    add_history_to_context=True,
    num_history_runs=5,              # 包含最近5次运行
    num_history_messages=20,         # 最多20条消息
    max_tool_calls_from_history=10,  # 历史工具调用数量限制

    # 会话摘要
    add_session_summary_to_context=True,
)
```

### 其他上下文选项

```python
agent = Agent(
    # 包含记忆
    add_memories_to_context=True,

    # 包含知识库结果
    add_knowledge_to_context=True,

    # 包含会话状态
    add_session_state_to_context=True,

    # 包含依赖信息
    add_dependencies_to_context=True,
)
```

## 会话管理

### 会话标识

```python
# 创建会话
response = agent.run(
    message="你好",
    session_id="chat-001",      # 会话标识
    user_id="user@example.com"  # 用户标识
)

# 同一会话继续对话
response = agent.run(
    message="我叫小明",
    session_id="chat-001",
    user_id="user@example.com"
)

# Agent 记住上下文
response = agent.run(
    message="我叫什么名字？",  # 会回答"小明"
    session_id="chat-001",
    user_id="user@example.com"
)
```

### 会话状态

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),

    # 初始会话状态
    session_state={
        "cart_items": [],
        "total": 0.0,
        "currency": "CNY"
    },

    # 包含状态到上下文
    add_session_state_to_context=True,

    # 允许 Agent 更新状态
    enable_agentic_state=True,
)

# 运行时更新状态
response = agent.run(
    message="添加 iPhone 到购物车",
    session_id="shopping-001",
    session_state={"cart_items": ["iPhone"], "total": 7999.0}
)

# 获取当前状态
state = agent.get_session_state(session_id="shopping-001")
```

### 会话操作

```python
# 获取会话
session = agent.get_session(session_id="chat-001")
print(session.messages)  # 所有消息

# 获取所有会话
sessions = agent.get_all_sessions(user_id="user@example.com")

# 删除会话
agent.delete_session(session_id="chat-001")
```

## 输入输出控制

### 结构化输出

```python
from pydantic import BaseModel, Field
from typing import Literal

class MarketAnalysis(BaseModel):
    """市场分析结果"""
    ticker: str = Field(..., description="股票代码")
    current_price: float = Field(..., description="当前价格")
    recommendation: Literal["BUY", "HOLD", "SELL"]
    confidence: float = Field(..., ge=0, le=1, description="置信度 0-1")
    reasons: list[str] = Field(..., description="分析理由")

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    output_schema=MarketAnalysis,
    parse_response=True,  # 解析为 Pydantic 对象
)

response = agent.run("分析苹果股票")
analysis = response.output  # MarketAnalysis 实例
print(f"建议: {analysis.recommendation}")
print(f"置信度: {analysis.confidence}")
```

### 输入验证

```python
class AnalysisRequest(BaseModel):
    ticker: str
    timeframe: Literal["1D", "1W", "1M", "1Y"]
    include_news: bool = False

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    input_schema=AnalysisRequest,
    output_schema=MarketAnalysis,
)
```

### 输出格式控制

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),

    # Markdown 格式
    markdown=True,

    # JSON 模式
    use_json_mode=False,

    # 原生结构化输出
    structured_outputs=True,

    # 保存响应到文件
    save_response_to_file="/tmp/response.json",
)
```

## 推理模式

### 启用推理

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),

    # 启用推理（思考过程）
    reasoning=True,

    # 可选：使用不同模型进行推理
    reasoning_model=Claude(id="claude-opus-4-5"),

    # 推理步骤控制
    reasoning_min_steps=1,
    reasoning_max_steps=10,
)

# 运行时启用
response = agent.run(
    message="复杂的数学问题",
    reasoning=True
)
```

### Claude 推理预算

```python
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(
        id="claude-opus-4-5",
        reasoning="enabled",
        reasoning_budget_tokens=10000,  # 推理 token 预算
    )
)
```

## 守卫与钩子

### 守卫（Guardrails）

```python
from agno.guardrails import PIIGuardrail, PromptInjectionGuardrail, BaseGuardrail

# 自定义守卫
class ContentGuardrail(BaseGuardrail):
    def check(self, run_input):
        if "恶意内容" in run_input.message:
            raise ValueError("检测到不当内容")

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    guardrails=[
        PIIGuardrail(),              # PII 检测
        PromptInjectionGuardrail(),  # 提示注入防护
        ContentGuardrail(),          # 自定义规则
    ]
)
```

### 钩子（Hooks）

```python
from agno.hooks import hook

@hook
def log_input(run_input, agent):
    """运行前钩子"""
    print(f"输入: {run_input.message}")

@hook(run_in_background=True)
def save_analytics(run_output, agent):
    """运行后钩子（后台执行）"""
    analytics.log(run_output)

@hook(run_in_background=True)
async def send_notification(run_output, agent):
    """异步钩子"""
    await notify_user(run_output)

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    pre_hooks=[log_input],
    post_hooks=[save_analytics, send_notification],
)
```

## 运行方法

### 同步运行

```python
response = agent.run(
    message="你好",
    session_id="chat-001",
    user_id="user@example.com",
    stream=False
)
print(response.content)
```

### 异步运行

```python
import asyncio

async def main():
    response = await agent.arun(
        message="分析市场",
        session_id="analysis-001"
    )
    print(response.content)

asyncio.run(main())
```

### 流式输出

```python
# 简单流式
agent.print_response("讲个故事", stream=True)

# 流式事件处理
for event in agent.run("讲个故事", stream=True):
    if event.type == "content":
        print(event.content, end="")
    elif event.type == "tool_call":
        print(f"\n工具调用: {event.tool_name}")
```

### 运行返回值

```python
response = agent.run("分析数据")

# 响应属性
response.content          # 文本内容
response.output           # 结构化输出（如果有 output_schema）
response.messages         # 所有消息
response.tool_calls       # 工具调用记录
response.metrics          # 性能指标
response.session_id       # 会话 ID
```

## 完整配置示例

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.tools.yfinance import YFinanceTools
from agno.guardrails import PIIGuardrail
from pydantic import BaseModel

# 数据库
db = SqliteDb(db_file="agents.db")

# 知识库
knowledge = Knowledge(
    name="公司文档",
    vector_db=ChromaDb(name="docs", path="./chromadb")
)

# 输出模式
class AnalysisResult(BaseModel):
    summary: str
    recommendations: list[str]
    confidence: float

# 完整 Agent 配置
agent = Agent(
    # 身份
    name="智能投资顾问",
    id="investment-advisor-v2",
    role="注册投资顾问",
    description="专业的投资分析和建议服务",

    # 模型
    model=Claude(id="claude-sonnet-4-5"),

    # 指令
    instructions="""
    你是专业的投资顾问，遵循以下原则：
    1. 基于数据做出分析
    2. 清晰说明风险
    3. 不做具体投资建议
    """,

    # 工具
    tools=[YFinanceTools()],
    tool_call_limit=10,

    # 存储
    db=db,

    # 记忆
    memory_manager=MemoryManager(
        model=Claude(id="claude-haiku-3-5"),
        db=db
    ),
    enable_agentic_memory=True,
    add_memories_to_context=True,

    # 知识库
    knowledge=knowledge,
    search_knowledge=True,
    add_knowledge_to_context=True,

    # 会话
    add_history_to_context=True,
    num_history_runs=5,
    session_state={"watchlist": []},
    enable_agentic_state=True,

    # 输出
    output_schema=AnalysisResult,
    parse_response=True,
    markdown=True,

    # 上下文
    add_datetime_to_context=True,
    timezone_identifier="Asia/Shanghai",

    # 安全
    guardrails=[PIIGuardrail()],

    # 调试
    debug_mode=True,
)

# 使用
response = agent.run(
    message="分析一下科技板块的投资机会",
    session_id="analysis-session",
    user_id="investor@example.com"
)

print(response.output.summary)
print(response.output.recommendations)
```

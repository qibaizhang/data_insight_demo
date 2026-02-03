# 生产最佳实践指南

## 目录

- [设计原则](#设计原则)
- [指令编写](#指令编写)
- [工具设计](#工具设计)
- [数据库选择](#数据库选择)
- [Memory 和 Storage 模式](#memory-和-storage-模式)
- [知识库优化](#知识库优化)
- [模型选择策略](#模型选择策略)
- [错误处理](#错误处理)
- [性能优化](#性能优化)
- [安全实践](#安全实践)
- [生产部署](#生产部署)
- [常见反面模式](#常见反面模式)

## 设计原则

### 从简单开始

```python
# ✅ 从最简单的配置开始
agent = Agent(model=OpenAI(id="gpt-4o"))

# 需要时逐步添加功能
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    tools=[...],                    # 需要工具时添加
    db=db,                          # 需要持久化时添加
    memory_manager=...,             # 需要记忆时添加
    knowledge=...,                  # 需要 RAG 时添加
)
```

### 重用 Agent 实例

```python
# ✅ 正确：全局创建一次，多次使用
agent = Agent(model=OpenAI(id="gpt-4o"), db=db)

def handle_request(user_id: str, message: str):
    return agent.run(message, user_id=user_id, session_id=f"chat-{user_id}")

# ❌ 错误：在循环中重复创建
for query in queries:
    agent = Agent(model=OpenAI(id="gpt-4o"))  # 每次创建很慢！
    agent.run(query)
```

### 使用结构化输出

```python
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    """分析结果模型"""
    summary: str = Field(..., description="分析摘要")
    score: float = Field(..., ge=0, le=1, description="评分 0-1")
    risks: list[str] = Field(default_factory=list, description="风险列表")
    recommendation: str = Field(..., description="建议")

# ✅ 使用结构化输出获得可靠结果
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    output_schema=AnalysisResult,
    parse_response=True,
)

response = agent.run("分析这个投资机会")
result = response.output  # 类型化的 AnalysisResult
print(f"评分: {result.score}")
print(f"建议: {result.recommendation}")
```

## 指令编写

### 结构化指令

```python
# ❌ 模糊的指令
instructions = "是一个有帮助的助手"

# ✅ 清晰、结构化的指令
instructions = """
## 角色
你是专业的金融分析师，具备 CFA 资质。

## 工作流程
1. 理解用户查询意图
2. 使用工具获取实时数据
3. 分析数据并得出结论
4. 结构化呈现结果

## 输出规则
- 使用表格展示数值数据
- 所有数据标注时间戳
- 不提供具体投资建议
- 始终说明数据来源

## 限制
- 仅使用提供的工具
- 缺失数据标记为 "N/A"
- 不确定时明确说明
"""
```

### 角色定义

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    name="智能财务顾问",
    role="注册财务规划师",
    description="""
    你是一位经验丰富的财务顾问：
    - 10年财务规划经验
    - 专注于个人理财和退休规划
    - 风格：专业但易于理解
    """,
    instructions="""
    ## 核心职责
    帮助用户进行财务规划和投资决策。

    ## 沟通风格
    - 专业但友好
    - 避免过度技术性术语
    - 用类比解释复杂概念
    """
)
```

## 工具设计

### 清晰的 Docstring

```python
from agno.tools import tool

# ✅ 完整的 docstring
@tool
def fetch_stock_data(ticker: str, period: str = "1mo") -> dict:
    """获取股票历史数据。

    使用 Yahoo Finance API 获取指定股票的历史价格数据。

    Args:
        ticker: 股票代码（如 "AAPL", "GOOGL"）
        period: 时间周期，可选值：1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

    Returns:
        包含以下字段的字典：
        - prices: 价格列表
        - volume: 成交量列表
        - dates: 日期列表

    Raises:
        ValueError: 如果 ticker 无效
    """
    # 实现...
```

### 错误处理

```python
@tool
def query_database(sql: str) -> str:
    """执行 SQL 查询。

    Args:
        sql: SQL 查询语句（仅支持 SELECT）
    """
    try:
        # 验证
        if not sql.strip().upper().startswith("SELECT"):
            return "错误：仅支持 SELECT 查询"

        # 执行
        results = db.execute(sql)
        return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        return f"查询错误：{str(e)}"
```

### 敏感操作确认

```python
@tool(requires_confirmation=True)
def delete_file(path: str) -> str:
    """永久删除文件。

    警告：此操作不可撤销！

    Args:
        path: 文件路径
    """
    import os
    os.remove(path)
    return f"已删除：{path}"

@tool(requires_confirmation=True)
def send_email(to: str, subject: str, body: str) -> str:
    """发送邮件。

    Args:
        to: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
    """
    # 发送邮件...
```

## 数据库选择

### 环境匹配

| 环境 | 推荐数据库 | 原因 |
|------|------------|------|
| 开发 | SQLite | 零配置，便于调试 |
| 测试 | SQLite (内存) | 快速、隔离 |
| 生产 | PostgreSQL | 可扩展、健壮 |
| 无服务器 | DynamoDB | AWS 原生 |
| 高速缓存 | Redis | 低延迟 |

### 生产配置

```python
import os
from agno.db.postgres import PostgresDb

# 生产数据库配置
prod_db = PostgresDb(
    host=os.environ["DB_HOST"],
    port=int(os.environ.get("DB_PORT", 5432)),
    database=os.environ["DB_NAME"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],

    # 连接池
    pool_size=10,
    max_overflow=20,
)

# 开发数据库
dev_db = SqliteDb(db_file="dev_agents.db")

# 环境切换
db = prod_db if os.environ.get("ENV") == "production" else dev_db
```

## Memory 和 Storage 模式

### 用户数据隔离

```python
def handle_chat(user_email: str, message: str, conversation_id: str = None):
    """处理用户聊天，确保数据隔离"""

    # 用户标识（用于记忆）
    user_id = f"user-{hash(user_email) % 1000000}"

    # 会话标识（用于历史）
    session_id = f"{user_id}-{conversation_id or 'default'}"

    return agent.run(
        message=message,
        user_id=user_id,          # 用户级记忆
        session_id=session_id     # 会话级历史
    )
```

### 历史长度控制

```python
# 聊天助手：保持足够上下文
chat_agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    num_history_runs=10,          # 10 轮对话
)

# 任务执行：关注当前任务
task_agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,           # 3 轮足够
)

# ❌ 避免过多历史
bad_agent = Agent(
    num_history_runs=100,         # 太多！浪费 token
)
```

### 记忆模式选择

```python
# 高效模式：Agent 自主决定
efficient_agent = Agent(
    memory_manager=memory_manager,
    enable_agentic_memory=True,    # Agent 决定何时存储
)

# 保证模式：每次都更新
guaranteed_agent = Agent(
    memory_manager=memory_manager,
    update_memory_on_run=True,     # 每次运行后更新
)

# 推荐：大多数场景用 agentic 模式
```

## 知识库优化

### 搜索类型选择

```python
from agno.vectordb.base import SearchType

# 文档问答：混合搜索（推荐）
docs_kb = Knowledge(
    vector_db=ChromaDb(
        name="docs",
        search_type=SearchType.hybrid,
    )
)

# 语义搜索：概念性查询
semantic_kb = Knowledge(
    vector_db=ChromaDb(
        name="semantic",
        search_type=SearchType.vector,
    )
)

# 精确匹配：关键词查询
keyword_kb = Knowledge(
    vector_db=ChromaDb(
        name="keyword",
        search_type=SearchType.keyword,
    )
)
```

### 分块大小优化

```python
from agno.knowledge.chunking import RecursiveChunking

# Q&A 文档：小块更精准
qa_kb = Knowledge(
    chunking_strategy=RecursiveChunking(
        chunk_size=500,
        overlap=100,
    )
)

# 长文分析：大块更多上下文
analysis_kb = Knowledge(
    chunking_strategy=RecursiveChunking(
        chunk_size=1500,
        overlap=300,
    )
)

# 代码文档：中等大小
code_kb = Knowledge(
    chunking_strategy=RecursiveChunking(
        chunk_size=800,
        overlap=150,
        separators=["\n\nclass ", "\n\ndef ", "\n\n", "\n"],
    )
)
```

## 模型选择策略

### 按场景选择

```python
from agno.models.openai import OpenAI
from agno.models.anthropic import Claude

# 复杂推理
reasoning_agent = Agent(
    model=OpenAI(id="o1"),           # 或 Claude Opus
    reasoning=True,
)

# 通用任务
general_agent = Agent(
    model=OpenAI(id="gpt-4o"),       # 性价比
)

# 快速响应
fast_agent = Agent(
    model=OpenAI(id="gpt-4o-mini"),  # 快速便宜
)

# 长文档
long_doc_agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),  # 200K 上下文
)
```

### 成本优化

```python
# 主模型用强大的，辅助用便宜的
agent = Agent(
    model=OpenAI(id="gpt-4o"),              # 主要推理
    memory_manager=MemoryManager(
        model=OpenAI(id="gpt-4o-mini"),     # 记忆提取用便宜模型
        db=db,
    ),
)

# 按复杂度路由
def get_agent_for_task(complexity: str):
    if complexity == "high":
        return Agent(model=OpenAI(id="gpt-4o"))
    else:
        return Agent(model=OpenAI(id="gpt-4o-mini"))
```

## 错误处理

### 优雅的错误处理

```python
import logging

logger = logging.getLogger(__name__)

def safe_agent_call(agent, message: str, **kwargs):
    """安全的 Agent 调用"""
    try:
        response = agent.run(message, **kwargs)
        return response.content

    except TimeoutError:
        logger.warning(f"Agent 超时: {message[:50]}")
        return "请求超时，请稍后重试。"

    except Exception as e:
        logger.error(f"Agent 错误: {e}", exc_info=True)
        return "抱歉，处理您的请求时出现问题。"
```

### 超时处理

```python
import asyncio

async def run_with_timeout(agent, message: str, timeout: int = 30):
    """带超时的异步运行"""
    try:
        return await asyncio.wait_for(
            agent.arun(message),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        return "请求超时，请尝试更简单的查询。"
```

### 重试机制

```python
import tenacity

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(min=1, max=10),
    retry=tenacity.retry_if_exception_type(Exception),
)
def reliable_agent_call(agent, message: str):
    """带重试的可靠调用"""
    return agent.run(message)
```

## 性能优化

### 异步处理

```python
import asyncio

async def process_batch(agent, messages: list[str]):
    """并行处理多个请求"""
    tasks = [agent.arun(msg) for msg in messages]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# 使用
responses = asyncio.run(process_batch(agent, ["问题1", "问题2", "问题3"]))
```

### 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(query_hash: str):
    """缓存常见查询的响应"""
    return agent.run(query_hash)

# 或使用 Redis 缓存
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_or_cache_response(query: str, ttl: int = 3600):
    cache_key = f"agent:response:{hash(query)}"
    cached = cache.get(cache_key)

    if cached:
        return cached.decode()

    response = agent.run(query)
    cache.setex(cache_key, ttl, response.content)
    return response.content
```

### 流式响应

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat/stream")
async def chat_stream(message: str):
    async def generate():
        async for event in agent.arun(message, stream=True):
            if event.type == "content":
                yield f"data: {event.content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

## 安全实践

### 输入验证

```python
from agno.guardrails import PIIGuardrail, PromptInjectionGuardrail

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    guardrails=[
        PIIGuardrail(),              # PII 检测
        PromptInjectionGuardrail(),  # 提示注入防护
    ]
)
```

### 敏感信息保护

```python
import os

# ✅ 使用环境变量
agent = Agent(
    model=OpenAI(
        id="gpt-4o",
        api_key=os.environ["OPENAI_API_KEY"],
    )
)

# ❌ 不要硬编码密钥
agent = Agent(
    model=OpenAI(
        id="gpt-4o",
        api_key="sk-xxxxx",  # 危险！
    )
)
```

### 权限控制

```python
def check_user_permission(user_id: str, action: str) -> bool:
    """检查用户权限"""
    # 实现权限检查逻辑
    return True

@tool(requires_confirmation=True)
def sensitive_operation(data: str) -> str:
    """敏感操作（需要确认）"""
    # ...
```

## 生产部署

### AgentOS 部署

```python
from agno.os import AgentOS

# 注册所有 Agent
agent_os = AgentOS(
    id="Production-System",
    agents=[finance_agent, support_agent],
    teams=[research_team],
    workflows=[content_pipeline],
    tracing=True,                    # 启用追踪
)

# 获取 FastAPI 应用
app = agent_os.get_app()

# 启动服务
if __name__ == "__main__":
    agent_os.serve(app="main:app", reload=False)
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产检查清单

- [ ] 使用 PostgreSQL（非 SQLite）
- [ ] 设置速率限制
- [ ] 配置连接池
- [ ] 添加错误处理
- [ ] 设置监控和日志
- [ ] 使用真实数据测试
- [ ] 审查 token 使用和成本
- [ ] 使用环境变量管理密钥
- [ ] 配置健康检查端点
- [ ] 设置自动扩展策略

## 常见反面模式

### 避免这些做法

```python
# ❌ 在循环中创建 Agent
for query in queries:
    agent = Agent(model=OpenAI(id="gpt-4o"))
    agent.run(query)

# ❌ 生产环境使用 SQLite
prod_agent = Agent(db=SqliteDb(db_file="prod.db"))

# ❌ 工具缺少类型提示
@tool
def bad_tool(x, y):  # 没有类型提示！
    return x + y

# ❌ 模糊的指令
agent = Agent(instructions="帮助用户")

# ❌ 硬编码密钥
agent = Agent(model=OpenAI(api_key="sk-xxx"))

# ❌ 忽略错误
response = agent.run(message)  # 没有 try-except

# ❌ 过多的历史
agent = Agent(num_history_runs=100)

# ❌ 不限制工具调用
agent = Agent(tools=[...])  # 没有 tool_call_limit
```

### 正确做法

```python
# ✅ 重用 Agent
agent = Agent(model=OpenAI(id="gpt-4o"))
for query in queries:
    agent.run(query)

# ✅ 生产用 PostgreSQL
prod_agent = Agent(db=PostgresDb(...))

# ✅ 完整的类型提示
@tool
def good_tool(x: float, y: float) -> float:
    """计算两数之和。"""
    return x + y

# ✅ 清晰的指令
agent = Agent(instructions="""
## 角色
你是专业的数据分析师。

## 工作流程
1. 理解用户需求
2. 分析数据
3. 输出结论
""")

# ✅ 环境变量
agent = Agent(model=OpenAI())  # 自动使用 OPENAI_API_KEY

# ✅ 错误处理
try:
    response = agent.run(message)
except Exception as e:
    logger.error(f"Error: {e}")
    return "服务暂时不可用"

# ✅ 适度的历史
agent = Agent(num_history_runs=5)

# ✅ 限制工具调用
agent = Agent(tools=[...], tool_call_limit=10)
```

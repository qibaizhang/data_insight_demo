# 内存与存储系统指南

## 目录

- [核心概念](#核心概念)
- [数据库配置](#数据库配置)
- [会话存储 (Storage)](#会话存储-storage)
- [用户记忆 (Memory)](#用户记忆-memory)
- [会话状态 (Session State)](#会话状态-session-state)
- [实战模式](#实战模式)

## 核心概念

### Memory vs Storage 区别

| 特性 | Storage（存储） | Memory（记忆） |
|------|-----------------|----------------|
| **存储内容** | 对话历史消息 | 用户偏好、事实、目标 |
| **范围** | 单个会话 | 跨所有会话 |
| **标识符** | session_id | user_id |
| **更新频率** | 每条消息自动 | 按需或每次运行 |
| **用途** | 上下文连续性 | 个性化体验 |

```
用户 Alice (user_id: alice@example.com)
├── 会话 1 (session_id: chat-001)  ← Storage
│   ├── 消息 1: "你好"
│   ├── 消息 2: "我叫 Alice"
│   └── 消息 3: "我喜欢科技股"
├── 会话 2 (session_id: chat-002)  ← Storage
│   ├── 消息 1: "推荐股票"        ← 可以使用 Memory 中的偏好
│   └── ...
└── 用户记忆                       ← Memory
    ├── 名字: Alice
    ├── 偏好: 科技股
    └── 风险: 中等
```

## 数据库配置

### 支持的数据库

| 数据库 | 用途 | 安装 |
|--------|------|------|
| SQLite | 开发/测试 | 内置 |
| PostgreSQL | 生产环境 | `pip install "agno[postgres]"` |
| MongoDB | 文档存储 | `pip install "agno[mongo]"` |
| MySQL | 传统关系型 | `pip install "agno[mysql]"` |
| DynamoDB | AWS 无服务器 | `pip install "agno[dynamodb]"` |
| Redis | 高速缓存 | `pip install "agno[redis]"` |
| Firestore | Google Cloud | `pip install "agno[firestore]"` |

### SQLite（开发推荐）

```python
from agno.db.sqlite import SqliteDb

db = SqliteDb(
    db_file="agents.db",        # 数据库文件路径
    table_name="agno_sessions", # 表名（可选）
)

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,
)
```

### PostgreSQL（生产推荐）

```python
from agno.db.postgres import PostgresDb

db = PostgresDb(
    host="localhost",
    port=5432,
    database="agents_prod",
    user="postgres",
    password="secure-password",
    schema="public",
)

# 或使用连接字符串
db = PostgresDb(
    connection_string="postgresql://user:pass@host:5432/db"
)

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,
)
```

### 异步 PostgreSQL

```python
from agno.db.async_postgres import AsyncPostgresDb

async_db = AsyncPostgresDb(
    connection_string="postgresql://user:pass@host:5432/db"
)

# 使用异步 API
response = await agent.arun(message="你好")
```

### MongoDB

```python
from agno.db.mongo import MongoDb

db = MongoDb(
    connection_string="mongodb://localhost:27017",
    database="agents",
    collection="sessions",
)

agent = Agent(model=OpenAI(id="gpt-4o"), db=db)
```

### DynamoDB

```python
from agno.db.dynamo import DynamoDb

db = DynamoDb(
    table_name="agno_sessions",
    region="us-east-1",
)

agent = Agent(model=OpenAI(id="gpt-4o"), db=db)
```

### Redis

```python
from agno.db.redis import RedisDb

db = RedisDb(
    host="localhost",
    port=6379,
    password="...",
    db=0,
)

agent = Agent(model=OpenAI(id="gpt-4o"), db=db)
```

## 会话存储 (Storage)

### 基础使用

```python
from agno.agent import Agent
from agno.models.openai import OpenAI
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="agents.db")

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,
    add_history_to_context=True,  # 将历史添加到上下文
    num_history_runs=5,           # 包含最近5次运行
)

# 会话 1：建立上下文
response = agent.run(
    message="我叫小明，我是一名程序员",
    session_id="chat-001",
    user_id="xiaoming@example.com"
)

# 会话 1 继续：Agent 记住上下文
response = agent.run(
    message="我叫什么名字？我是做什么的？",
    session_id="chat-001",
    user_id="xiaoming@example.com"
)
# Agent 会回答："你叫小明，你是一名程序员"
```

### 历史配置选项

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,

    # 历史消息
    add_history_to_context=True,
    num_history_runs=5,               # 最近几次运行
    num_history_messages=20,          # 最大消息数
    max_tool_calls_from_history=10,   # 历史工具调用数量

    # 会话摘要
    add_session_summary_to_context=True,
)
```

### 会话管理 API

```python
# 获取会话
session = agent.get_session(session_id="chat-001")
print(session.messages)      # 所有消息
print(session.created_at)    # 创建时间

# 获取用户所有会话
sessions = agent.get_all_sessions(user_id="xiaoming@example.com")
for s in sessions:
    print(f"会话: {s.session_id}, 消息数: {len(s.messages)}")

# 删除会话
agent.delete_session(session_id="chat-001")
```

## 用户记忆 (Memory)

### 基础配置

```python
from agno.memory import MemoryManager

db = SqliteDb(db_file="agents.db")

# 记忆管理器
memory_manager = MemoryManager(
    model=OpenAI(id="gpt-4o-mini"),  # 用便宜模型提取记忆
    db=db,
    additional_instructions="""
    捕捉用户的：
    - 姓名和基本信息
    - 兴趣爱好和偏好
    - 重要目标和计划
    - 投资风险偏好
    """
)

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,
    memory_manager=memory_manager,

    # 记忆模式（二选一）
    enable_agentic_memory=True,       # Agent 自主决定何时存储
    # update_memory_on_run=True,      # 每次运行后自动更新

    add_memories_to_context=True,     # 在上下文中包含记忆
)
```

### 记忆模式对比

| 模式 | 设置 | 特点 | 适用场景 |
|------|------|------|----------|
| **Agentic** | `enable_agentic_memory=True` | Agent 决定何时存储，更高效 | 通用场景 |
| **自动** | `update_memory_on_run=True` | 每次运行后更新，保证捕获 | 关键信息场景 |

### 记忆使用示例

```python
user_id = "investor@example.com"

# 第一次对话：存储偏好
agent.run(
    "我叫王大明，我喜欢科技股，风险承受能力中等，投资目标是长期增值",
    user_id=user_id,
    session_id="chat-001"
)

# 新会话：记忆仍然有效
agent.run(
    "根据我的偏好，推荐一些股票",
    user_id=user_id,
    session_id="chat-002"  # 不同会话
)
# Agent 会根据记忆中的偏好（科技股、中等风险、长期增值）推荐

# 查看存储的记忆
memories = agent.get_user_memories(user_id=user_id)
for memory in memories:
    print(f"记忆: {memory.content}")
```

### 记忆管理 API

```python
# 获取用户记忆
memories = agent.get_user_memories(user_id="investor@example.com")

# 手动添加记忆
agent.add_user_memory(
    user_id="investor@example.com",
    memory="用户偏好：长线投资"
)

# 删除特定记忆
agent.delete_user_memory(
    user_id="investor@example.com",
    memory_id="mem-001"
)

# 清空用户所有记忆
agent.clear_user_memories(user_id="investor@example.com")
```

## 会话状态 (Session State)

### 基础使用

```python
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=db,

    # 初始状态
    session_state={
        "cart_items": [],
        "total": 0.0,
        "currency": "CNY",
        "discount_code": None
    },

    add_session_state_to_context=True,  # 上下文包含状态
    enable_agentic_state=True,          # Agent 可更新状态
)
```

### 购物车示例

```python
# 添加商品
response = agent.run(
    "添加一台 iPhone 15 Pro 到购物车",
    session_id="shopping-001"
)

# Agent 更新状态
# session_state: {"cart_items": ["iPhone 15 Pro"], "total": 8999.0, ...}

# 继续购物
response = agent.run(
    "再加一个 AirPods Pro",
    session_id="shopping-001"
)

# 获取当前状态
state = agent.get_session_state(session_id="shopping-001")
print(f"购物车: {state['cart_items']}")
print(f"总价: {state['total']}")
```

### 状态管理 API

```python
# 获取状态
state = agent.get_session_state(session_id="shopping-001")

# 更新状态
agent.update_session_state(
    session_id="shopping-001",
    state={"discount_code": "SUMMER20", "discount": 0.2}
)

# 运行时传入状态
response = agent.run(
    message="结算",
    session_id="shopping-001",
    session_state={"payment_method": "alipay"}
)
```

## 实战模式

### 完整的个性化助手

```python
from agno.agent import Agent
from agno.models.openai import OpenAI
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

# 数据库
db = SqliteDb(db_file="assistant.db")

# 记忆管理器
memory_manager = MemoryManager(
    model=OpenAI(id="gpt-4o-mini"),
    db=db,
    additional_instructions="""
    记住用户的：
    - 姓名和称呼偏好
    - 工作领域和专业背景
    - 兴趣爱好
    - 沟通风格偏好（正式/随意）
    - 重要日期（生日等）
    """
)

# 个性化助手
assistant = Agent(
    name="个人助手",
    model=OpenAI(id="gpt-4o"),
    db=db,

    # 记忆
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_memories_to_context=True,

    # 历史
    add_history_to_context=True,
    num_history_runs=10,

    # 状态
    session_state={"tasks": [], "reminders": []},
    enable_agentic_state=True,
    add_session_state_to_context=True,

    instructions="""
    你是用户的私人助手。
    - 记住用户的偏好和习惯
    - 使用用户喜欢的称呼
    - 主动提供个性化建议
    """
)

# 使用
def chat(user_email: str, message: str, session_id: str = None):
    if session_id is None:
        session_id = f"chat-{user_email}"

    return assistant.run(
        message=message,
        user_id=user_email,
        session_id=session_id
    )

# 首次对话
chat("zhang@example.com", "你好，我叫张三，是一名产品经理")

# 后续对话（记住偏好）
chat("zhang@example.com", "帮我分析一下用户需求")  # 知道用户是 PM
```

### 多用户隔离

```python
def create_user_session(user_id: str, conversation_id: str):
    """为每个用户创建隔离的会话"""
    session_id = f"{user_id}-{conversation_id}"

    return agent.run(
        message="开始新对话",
        user_id=user_id,          # 用户级记忆
        session_id=session_id     # 会话级历史
    )

# 用户 A 的对话
create_user_session("user-a", "conv-1")  # user-a-conv-1
create_user_session("user-a", "conv-2")  # user-a-conv-2（新对话）

# 用户 B 的对话（完全隔离）
create_user_session("user-b", "conv-1")  # user-b-conv-1
```

### 生产环境配置

```python
from agno.db.postgres import PostgresDb

# 生产数据库
prod_db = PostgresDb(
    host="prod-db.internal",
    port=5432,
    database="agents",
    user="agent_service",
    password=os.environ["DB_PASSWORD"],
    # 连接池配置
    pool_size=10,
    max_overflow=20,
)

# 生产 Agent
prod_agent = Agent(
    model=OpenAI(id="gpt-4o"),
    db=prod_db,

    # 记忆
    memory_manager=MemoryManager(
        model=OpenAI(id="gpt-4o-mini"),  # 便宜模型
        db=prod_db,
    ),
    enable_agentic_memory=True,

    # 历史（适度）
    add_history_to_context=True,
    num_history_runs=5,       # 不要太多，节省 token

    # 调试
    debug_mode=False,         # 生产关闭调试
)
```

### 历史长度建议

| 场景 | num_history_runs | 原因 |
|------|------------------|------|
| 聊天助手 | 5-10 | 保持上下文连贯 |
| 任务执行 | 2-5 | 关注当前任务 |
| 代码助手 | 3-5 | 记住最近代码变更 |
| 客服 | 10-15 | 理解完整问题 |

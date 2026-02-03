---
name: agno-agent-builder
description: Agno 智能体开发框架完整指南。用于构建 AI Agent、多智能体团队和工作流应用。当用户提到 agno、智能体开发、Agent 创建、多智能体系统、AI 工作流、RAG 知识库、Agent 记忆存储、工具调用、LLM 应用开发时使用此 skill。支持：(1) 单体 Agent 创建与配置 (2) 工具系统集成 (3) 40+ LLM 模型配置 (4) 记忆与会话存储 (5) 知识库 RAG 实现 (6) 多智能体 Team 协作 (7) Workflow 工作流编排 (8) 生产部署最佳实践。
---

# Agno 智能体开发指南

Agno 是用于构建多智能体系统的生产级 Python 框架，支持 40+ LLM 提供商和 100+ 内置工具。

## 目录

- [快速入门](#快速入门)
- [模块导航](#模块导航)
- [核心概念](#核心概念)
- [常用模式速查](#常用模式速查)

## 快速入门

### 安装

```bash
pip install agno                     # 基础安装
pip install "agno[openai]"          # OpenAI 支持
pip install "agno[anthropic]"       # Anthropic 支持
pip install "agno[google]"          # Google Gemini 支持
pip install "agno[postgres]"        # PostgreSQL 生产存储
```

### 最简 Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAI

agent = Agent(
    name="助手",
    model=OpenAI(id="gpt-4o"),
    instructions="你是一个有帮助的助手。"
)

# 同步运行
response = agent.run("你好！")
print(response.content)

# 流式输出
agent.print_response("介绍一下你自己", stream=True)
```

### 带工具的 Agent

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    name="金融分析师",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    instructions="你是专业的金融分析师，使用工具获取实时数据。",
    markdown=True
)

agent.print_response("分析一下 NVIDIA 的股票", stream=True)
```

### 带记忆的 Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAI
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

db = SqliteDb(db_file="agents.db")

agent = Agent(
    name="个性化助手",
    model=OpenAI(id="gpt-4o"),
    db=db,
    memory_manager=MemoryManager(model=OpenAI(id="gpt-4o-mini"), db=db),
    enable_agentic_memory=True,
    add_history_to_context=True
)

# 记忆用户偏好
agent.run("我喜欢科技股，风险承受能力中等", user_id="user-001")

# 后续对话会记住偏好
agent.run("推荐一些股票", user_id="user-001")
```

## 模块导航

根据需求选择相应模块：

| 需求 | 参考文档 |
|------|----------|
| Agent 完整配置 | [01-agent.md](references/01-agent.md) |
| 工具系统与自定义工具 | [02-tools.md](references/02-tools.md) |
| LLM 模型配置 | [03-models.md](references/03-models.md) |
| 记忆与会话存储 | [04-memory-storage.md](references/04-memory-storage.md) |
| 知识库与 RAG | [05-knowledge-rag.md](references/05-knowledge-rag.md) |
| 多智能体 Team 与 Workflow | [06-team-workflow.md](references/06-team-workflow.md) |
| 生产最佳实践 | [07-best-practices.md](references/07-best-practices.md) |

## 核心概念

### 架构层次

```
┌─────────────────────────────────┐
│   应用层: Agent / Team / Workflow   │
├─────────────────────────────────┤
│   能力层: Tools / Memory / Knowledge │
├─────────────────────────────────┤
│   基础层: Model / Database / VectorDB │
└─────────────────────────────────┘
```

### 关键组件

| 组件 | 作用 | 典型用途 |
|------|------|----------|
| **Agent** | 核心智能体 | 对话、任务执行 |
| **Model** | LLM 提供商 | Claude、GPT、Gemini 等 |
| **Tools** | 外部能力 | API 调用、数据获取 |
| **Memory** | 用户记忆 | 跨会话偏好存储 |
| **Storage** | 会话存储 | 对话历史持久化 |
| **Knowledge** | 知识库 | RAG 文档检索 |
| **Team** | 多智能体 | 协作讨论分析 |
| **Workflow** | 工作流 | 顺序任务管道 |

## 常用模式速查

### 结构化输出

```python
from pydantic import BaseModel

class StockAnalysis(BaseModel):
    ticker: str
    recommendation: str  # BUY/HOLD/SELL
    target_price: float
    risks: list[str]

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    output_schema=StockAnalysis
)

response = agent.run("分析苹果股票")
analysis = response.output  # 类型化的 StockAnalysis 对象
```

### 多智能体团队

```python
from agno.team import Team

bull = Agent(name="看多分析师", model=OpenAI(id="gpt-4o"), role="找投资正面理由")
bear = Agent(name="看空分析师", model=OpenAI(id="gpt-4o"), role="找投资负面理由")

team = Team(
    name="投资研究团队",
    members=[bull, bear],
    model=Claude(id="claude-sonnet-4-5"),
    instructions="综合多空观点给出平衡建议"
)

team.print_response("应该投资特斯拉吗？")
```

### 知识库 RAG

```python
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

knowledge = Knowledge(
    name="公司文档",
    vector_db=ChromaDb(name="docs", path="./chromadb")
)

knowledge.insert(path="./documents/")  # 批量导入文档

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    knowledge=knowledge,
    search_knowledge=True
)

agent.print_response("公司的退款政策是什么？")
```

### 顺序工作流

```python
from agno.workflow import Workflow, Step

workflow = Workflow(
    name="研究管道",
    steps=[
        Step(name="数据收集", agent=data_agent),
        Step(name="分析处理", agent=analysis_agent),
        Step(name="报告生成", agent=report_agent)
    ]
)

workflow.run("分析2024年市场趋势")
```

# 知识库与 RAG 实现指南

## 目录

- [知识库概述](#知识库概述)
- [向量数据库配置](#向量数据库配置)
- [文档加载](#文档加载)
- [搜索配置](#搜索配置)
- [分块策略](#分块策略)
- [嵌入模型](#嵌入模型)
- [Agent 集成](#agent-集成)
- [实战示例](#实战示例)

## 知识库概述

### 核心组件

| 组件 | 作用 | 说明 |
|------|------|------|
| **Knowledge** | 文档容器 | 管理文档的加载、搜索 |
| **VectorDB** | 向量存储 | 存储文档嵌入向量 |
| **Embedder** | 嵌入模型 | 将文本转换为向量 |
| **Chunking** | 分块策略 | 将文档切分为小块 |

### 工作流程

```
文档 → 分块 → 嵌入 → 存储 → 搜索 → 检索 → Agent 回答
```

## 向量数据库配置

### 支持的向量数据库

| VectorDB | 最佳用途 | 安装 |
|----------|---------|------|
| ChromaDB | 本地开发 | `pip install chromadb` |
| Pinecone | 托管生产 | `pip install pinecone-client` |
| Qdrant | 自托管 | `pip install qdrant-client` |
| Weaviate | 混合搜索 | `pip install weaviate-client` |
| pgvector | PostgreSQL 用户 | `pip install pgvector` |
| Milvus | 大规模 | `pip install pymilvus` |

### ChromaDB（开发推荐）

```python
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

knowledge = Knowledge(
    name="公司文档",
    vector_db=ChromaDb(
        name="company_docs",
        collection="documents",
        path="./chromadb",              # 持久化路径
        persistent_client=True,         # 持久化
    )
)
```

### Pinecone（生产推荐）

```python
from agno.vectordb.pinecone import Pinecone

knowledge = Knowledge(
    name="产品知识库",
    vector_db=Pinecone(
        name="product-kb",
        index="product-index",
        api_key="pinecone-api-key",
        environment="us-east-1",
    )
)
```

### Qdrant

```python
from agno.vectordb.qdrant import Qdrant

knowledge = Knowledge(
    name="技术文档",
    vector_db=Qdrant(
        name="tech-docs",
        collection="documents",
        host="localhost",
        port=6333,
    )
)

# 云端 Qdrant
knowledge = Knowledge(
    vector_db=Qdrant(
        name="tech-docs",
        url="https://xxx.qdrant.io",
        api_key="...",
    )
)
```

### pgvector（PostgreSQL）

```python
from agno.vectordb.pgvector import PgVector

knowledge = Knowledge(
    name="企业知识",
    vector_db=PgVector(
        connection_string="postgresql://user:pass@host:5432/db",
        table_name="documents",
    )
)
```

### Weaviate

```python
from agno.vectordb.weaviate import Weaviate

knowledge = Knowledge(
    name="产品目录",
    vector_db=Weaviate(
        url="http://localhost:8080",
        class_name="Document",
    )
)
```

## 文档加载

### 加载本地文件

```python
# 加载单个文件
knowledge.insert(path="./docs/guide.pdf")
knowledge.insert(path="./docs/faq.md")

# 加载目录
knowledge.insert(
    path="./documents/",
    include=["*.pdf", "*.md", "*.txt"],  # 包含模式
    exclude=["draft/*", "*.tmp"],         # 排除模式
    recursive=True                        # 递归子目录
)
```

### 加载网页

```python
# 单个 URL
knowledge.insert(url="https://docs.example.com/guide")

# 多个 URL
knowledge.insert(urls=[
    "https://docs.example.com/guide",
    "https://docs.example.com/faq",
    "https://docs.example.com/api"
])

# 网站爬取
knowledge.insert(
    url="https://docs.example.com",
    crawl=True,                    # 爬取链接
    max_depth=2,                   # 最大深度
    max_pages=100                  # 最大页数
)
```

### 加载文本

```python
# 直接文本
knowledge.insert(
    text_content="这是一段重要的政策说明...",
    metadata={"source": "policy", "version": "2024"}
)

# 文本列表
knowledge.insert(
    texts=[
        "文档1内容...",
        "文档2内容...",
    ],
    metadata={"batch": "001"}
)
```

### 支持的文件格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | .pdf | 自动提取文本 |
| Markdown | .md | 保留结构 |
| 文本 | .txt | 纯文本 |
| Word | .docx | Office 文档 |
| HTML | .html | 网页 |
| CSV | .csv | 表格数据 |
| JSON | .json | 结构化数据 |

### 文档读取器

```python
from agno.knowledge.readers import PDFReader, DocxReader

# 自定义读取器
knowledge = Knowledge(
    name="文档库",
    vector_db=ChromaDb(...),
    readers={
        ".pdf": PDFReader(extract_images=True),
        ".docx": DocxReader(),
    }
)
```

## 搜索配置

### 搜索类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| **vector** | 语义相似度 | 概念性查询 |
| **keyword** | 关键词匹配 | 精确查询 |
| **hybrid** | 语义 + 关键词 | 通用（推荐）|

```python
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.base import SearchType

knowledge = Knowledge(
    name="知识库",
    vector_db=ChromaDb(
        name="docs",
        search_type=SearchType.hybrid,  # 混合搜索
    )
)
```

### 手动搜索

```python
# 基础搜索
results = knowledge.search(
    query="如何配置数据库？",
    limit=5
)

for result in results:
    print(f"相关度: {result.score}")
    print(f"内容: {result.content}")
    print(f"来源: {result.metadata['source']}")

# 带过滤器搜索
results = knowledge.search(
    query="退款政策",
    limit=10,
    filters={"category": "policy", "version": "2024"}
)
```

### 搜索参数

```python
results = knowledge.search(
    query="用户查询",
    limit=10,                        # 返回数量
    score_threshold=0.7,             # 最低相关度阈值
    filters={"key": "value"},        # 元数据过滤
    include_metadata=True,           # 包含元数据
)
```

## 分块策略

### 固定大小分块

```python
from agno.knowledge.chunking import FixedSizeChunking

knowledge = Knowledge(
    name="文档库",
    vector_db=ChromaDb(...),
    chunking_strategy=FixedSizeChunking(
        chunk_size=1000,      # 每块字符数
        overlap=200,          # 重叠字符数
    )
)
```

### 递归分块（推荐）

```python
from agno.knowledge.chunking import RecursiveChunking

knowledge = Knowledge(
    name="文档库",
    vector_db=ChromaDb(...),
    chunking_strategy=RecursiveChunking(
        chunk_size=1000,
        separators=["\n\n", "\n", "。", " "],  # 按优先级分割
    )
)
```

### 语义分块

```python
from agno.knowledge.chunking import SemanticChunking

knowledge = Knowledge(
    name="文档库",
    vector_db=ChromaDb(...),
    chunking_strategy=SemanticChunking(
        model=OpenAI(id="gpt-4o-mini"),  # 用 AI 判断分块
    )
)
```

### 分块大小建议

| 场景 | chunk_size | overlap | 原因 |
|------|------------|---------|------|
| Q&A 文档 | 500 | 100 | 精准匹配 |
| 技术文档 | 1000 | 200 | 保持上下文 |
| 长文分析 | 1500 | 300 | 更多上下文 |
| 代码文档 | 800 | 150 | 函数级别 |

## 嵌入模型

### OpenAI Embeddings（推荐）

```python
from agno.embedder.openai import OpenAIEmbedder

knowledge = Knowledge(
    name="知识库",
    vector_db=ChromaDb(
        name="docs",
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small",  # 或 text-embedding-3-large
            api_key="sk-...",
        )
    )
)
```

### 其他嵌入模型

```python
# Cohere
from agno.embedder.cohere import CohereEmbedder

embedder = CohereEmbedder(
    id="embed-multilingual-v3.0",
    api_key="...",
)

# HuggingFace
from agno.embedder.huggingface import HuggingFaceEmbedder

embedder = HuggingFaceEmbedder(
    id="sentence-transformers/all-MiniLM-L6-v2"
)

# Ollama（本地）
from agno.embedder.ollama import OllamaEmbedder

embedder = OllamaEmbedder(
    id="nomic-embed-text",
    host="http://localhost:11434"
)
```

## Agent 集成

### 基础集成

```python
from agno.agent import Agent
from agno.models.openai import OpenAI
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb

# 创建知识库
knowledge = Knowledge(
    name="产品文档",
    vector_db=ChromaDb(name="product-docs", path="./chromadb")
)

# 加载文档
knowledge.insert(path="./docs/")

# 创建 Agent
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    knowledge=knowledge,
    search_knowledge=True,              # 给 Agent 搜索工具
    add_knowledge_to_context=True,      # 上下文包含知识
)

agent.print_response("产品的退款政策是什么？")
```

### 搜索模式

```python
# 模式 1: Agent 自主搜索（推荐）
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,           # Agent 决定是否搜索
)

# 模式 2: 总是搜索
agent = Agent(
    knowledge=knowledge,
    always_search_knowledge=True,    # 每次都搜索
    num_knowledge_results=5,         # 返回数量
)

# 模式 3: Agent 控制过滤器
agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
    enable_agentic_knowledge_filters=True,  # Agent 选择过滤器
)
```

### 多知识库

```python
# 创建多个知识库
product_kb = Knowledge(
    name="产品知识",
    vector_db=ChromaDb(name="product", path="./chromadb/product")
)
product_kb.insert(path="./docs/product/")

policy_kb = Knowledge(
    name="政策知识",
    vector_db=ChromaDb(name="policy", path="./chromadb/policy")
)
policy_kb.insert(path="./docs/policy/")

# Agent 使用多个知识库
agent = Agent(
    model=OpenAI(id="gpt-4o"),
    knowledge=[product_kb, policy_kb],
    search_knowledge=True,
)
```

## 实战示例

### 客服知识库

```python
from agno.agent import Agent
from agno.models.openai import OpenAI
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.chunking import RecursiveChunking

# 知识库配置
customer_kb = Knowledge(
    name="客服知识库",
    vector_db=ChromaDb(
        name="customer-service",
        path="./chromadb",
        search_type="hybrid",       # 混合搜索
    ),
    chunking_strategy=RecursiveChunking(
        chunk_size=500,             # 较小块，精准匹配
        overlap=100,
    )
)

# 加载文档
customer_kb.insert(path="./docs/faq.md")
customer_kb.insert(path="./docs/policies/")
customer_kb.insert(path="./docs/product-guide.pdf")

# 客服 Agent
service_agent = Agent(
    name="智能客服",
    model=OpenAI(id="gpt-4o"),
    knowledge=customer_kb,
    search_knowledge=True,
    instructions="""
    你是友好的客服助手。

    ## 回答原则
    1. 先搜索知识库获取准确信息
    2. 基于知识库内容回答
    3. 如果知识库没有相关信息，诚实说明
    4. 保持友好专业的语气

    ## 格式要求
    - 简洁明了
    - 重要信息用粗体标注
    - 必要时提供步骤列表
    """,
    markdown=True,
)

service_agent.print_response("如何申请退款？", stream=True)
```

### 代码文档助手

```python
from agno.knowledge.readers import CodeReader

# 代码知识库
code_kb = Knowledge(
    name="代码文档",
    vector_db=ChromaDb(name="code-docs", path="./chromadb"),
    readers={
        ".py": CodeReader(language="python"),
        ".js": CodeReader(language="javascript"),
    },
    chunking_strategy=RecursiveChunking(
        chunk_size=800,
        separators=["\n\nclass ", "\n\ndef ", "\n\n", "\n"],
    )
)

# 加载代码库
code_kb.insert(
    path="./src/",
    include=["*.py", "*.js"],
    exclude=["test_*", "__pycache__"]
)

# 代码助手
code_agent = Agent(
    name="代码助手",
    model=OpenAI(id="gpt-4o"),
    knowledge=code_kb,
    search_knowledge=True,
    instructions="""
    你是代码库专家。
    - 搜索代码库回答问题
    - 提供代码示例和解释
    - 说明代码的位置和上下文
    """
)

code_agent.print_response("用户认证是怎么实现的？", stream=True)
```

### 生产环境配置

```python
from agno.vectordb.pinecone import Pinecone
from agno.embedder.openai import OpenAIEmbedder

# 生产知识库
prod_knowledge = Knowledge(
    name="企业知识库",
    vector_db=Pinecone(
        name="enterprise-kb",
        index="enterprise-documents",
        api_key=os.environ["PINECONE_API_KEY"],
        environment="us-east-1",
        embedder=OpenAIEmbedder(
            id="text-embedding-3-large",  # 更好的嵌入
        )
    ),
    chunking_strategy=RecursiveChunking(
        chunk_size=1000,
        overlap=200,
    )
)

# 生产 Agent
prod_agent = Agent(
    model=OpenAI(id="gpt-4o"),
    knowledge=prod_knowledge,
    search_knowledge=True,
    num_knowledge_results=10,
)
```

### 知识库更新

```python
# 增量更新
knowledge.insert(path="./new_docs/new_guide.pdf")

# 重新索引
knowledge.rebuild()

# 删除文档
knowledge.delete(filters={"source": "outdated.pdf"})

# 清空知识库
knowledge.clear()
```

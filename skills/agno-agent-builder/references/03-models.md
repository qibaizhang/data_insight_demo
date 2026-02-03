# 模型配置指南

## 目录

- [支持的模型提供商](#支持的模型提供商)
- [主流模型配置](#主流模型配置)
- [本地模型](#本地模型)
- [推理优化提供商](#推理优化提供商)
- [云平台托管](#云平台托管)
- [模型选择指南](#模型选择指南)
- [多模态支持](#多模态支持)
- [高级配置](#高级配置)

## 支持的模型提供商

Agno 支持 40+ LLM 提供商：

| 类型 | 提供商 |
|------|--------|
| **主流云** | OpenAI, Anthropic, Google, Mistral, Cohere |
| **云平台** | AWS Bedrock, Azure OpenAI, Google Vertex AI |
| **推理优化** | Groq, Together, Fireworks, DeepInfra |
| **本地模型** | Ollama, LM Studio, llama.cpp, vLLM |
| **其他** | Perplexity, OpenRouter, DeepSeek, Zhipu |

## 主流模型配置

### OpenAI

```python
from agno.models.openai import OpenAI

# GPT-4o（推荐通用）
model = OpenAI(
    id="gpt-4o",
    api_key="sk-...",           # 或设置 OPENAI_API_KEY 环境变量
    temperature=0.7,
    max_tokens=4096,
)

# GPT-4o-mini（快速、便宜）
model = OpenAI(id="gpt-4o-mini")

# O1 推理模型
model = OpenAI(id="o1")
model = OpenAI(id="o1-mini")

# O3 最新推理模型
model = OpenAI(id="o3-mini")

agent = Agent(model=model)
```

### Anthropic Claude

```python
from agno.models.anthropic import Claude

# Claude Sonnet 4.5（推荐）
model = Claude(
    id="claude-sonnet-4-5",
    api_key="sk-ant-...",       # 或设置 ANTHROPIC_API_KEY
    max_tokens=8192,
)

# Claude Opus 4.5（最强）
model = Claude(id="claude-opus-4-5")

# Claude Haiku 3.5（快速）
model = Claude(id="claude-haiku-3-5")

# 启用推理模式
model = Claude(
    id="claude-sonnet-4-5",
    reasoning="enabled",
    reasoning_budget_tokens=10000,
)

agent = Agent(model=model)
```

### Google Gemini

```python
from agno.models.google import Gemini

# Gemini 2.0 Flash（推荐）
model = Gemini(
    id="gemini-2.0-flash",
    api_key="AIza...",          # 或设置 GOOGLE_API_KEY
)

# Gemini 1.5 Pro（长上下文）
model = Gemini(id="gemini-1.5-pro")  # 支持 1M tokens

# Gemini 1.5 Flash
model = Gemini(id="gemini-1.5-flash")

agent = Agent(model=model)
```

### Mistral

```python
from agno.models.mistral import Mistral

# Mistral Large
model = Mistral(
    id="mistral-large-latest",
    api_key="...",
)

# Mistral Small（快速）
model = Mistral(id="mistral-small-latest")

# Codestral（代码专用）
model = Mistral(id="codestral-latest")

agent = Agent(model=model)
```

### Cohere

```python
from agno.models.cohere import Cohere

model = Cohere(
    id="command-r-plus",
    api_key="...",
)

agent = Agent(model=model)
```

### DeepSeek

```python
from agno.models.deepseek import DeepSeek

# DeepSeek V3
model = DeepSeek(
    id="deepseek-chat",
    api_key="...",
)

# DeepSeek Reasoner
model = DeepSeek(id="deepseek-reasoner")

agent = Agent(model=model)
```

## 本地模型

### Ollama（推荐）

```python
from agno.models.ollama import Ollama

# Llama 3.2
model = Ollama(
    id="llama3.2",
    host="http://localhost:11434",  # Ollama 服务地址
)

# Mistral
model = Ollama(id="mistral:latest")

# CodeLlama
model = Ollama(id="codellama:latest")

# Qwen
model = Ollama(id="qwen2.5:latest")

agent = Agent(model=model)
```

### LM Studio

```python
from agno.models.lmstudio import LMStudio

model = LMStudio(
    id="local-model",
    host="http://localhost:1234",
)

agent = Agent(model=model)
```

### vLLM

```python
from agno.models.vllm import vLLM

model = vLLM(
    id="meta-llama/Llama-3.2-8B",
    host="http://localhost:8000",
)

agent = Agent(model=model)
```

### llama.cpp

```python
from agno.models.llamacpp import LlamaCpp

model = LlamaCpp(
    model_path="/path/to/model.gguf",
    n_ctx=4096,
    n_gpu_layers=35,
)

agent = Agent(model=model)
```

## 推理优化提供商

### Groq（超快推理）

```python
from agno.models.groq import Groq

# Llama 3.3 70B（推荐）
model = Groq(
    id="llama-3.3-70b-versatile",
    api_key="gsk_...",
)

# Mixtral
model = Groq(id="mixtral-8x7b-32768")

agent = Agent(model=model)
```

### Together AI

```python
from agno.models.together import Together

model = Together(
    id="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    api_key="...",
)

agent = Agent(model=model)
```

### Fireworks AI

```python
from agno.models.fireworks import Fireworks

model = Fireworks(
    id="accounts/fireworks/models/llama-v3p1-70b-instruct",
    api_key="...",
)

agent = Agent(model=model)
```

### DeepInfra

```python
from agno.models.deepinfra import DeepInfra

model = DeepInfra(
    id="meta-llama/Meta-Llama-3.1-70B-Instruct",
    api_key="...",
)

agent = Agent(model=model)
```

## 云平台托管

### AWS Bedrock

```python
from agno.models.aws import Bedrock

# Claude on Bedrock
model = Bedrock(
    id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    region="us-east-1",
)

# Llama on Bedrock
model = Bedrock(id="meta.llama3-70b-instruct-v1:0")

agent = Agent(model=model)
```

### Azure OpenAI

```python
from agno.models.azure import AzureOpenAI

model = AzureOpenAI(
    id="gpt-4o",
    azure_endpoint="https://xxx.openai.azure.com/",
    api_key="...",
    api_version="2024-02-15-preview",
)

agent = Agent(model=model)
```

### Google Vertex AI

```python
from agno.models.google import VertexAI

model = VertexAI(
    id="gemini-1.5-pro",
    project="your-project-id",
    location="us-central1",
)

agent = Agent(model=model)
```

## 模型选择指南

### 按场景推荐

| 场景 | 推荐模型 | 原因 |
|------|----------|------|
| **复杂推理** | o1, Claude Opus 4.5 | 最强推理能力 |
| **通用任务** | GPT-4o, Claude Sonnet 4.5 | 性价比最高 |
| **代码生成** | GPT-4o, Claude Sonnet, Codestral | 代码能力强 |
| **快速响应** | GPT-4o-mini, Groq/Llama | 低延迟 |
| **成本优化** | GPT-4o-mini, Gemini Flash | 便宜 |
| **长文档** | Claude (200K), Gemini 1.5 Pro (1M) | 超长上下文 |
| **本地/隐私** | Ollama/Llama, LM Studio | 数据本地化 |
| **中文优化** | DeepSeek, Qwen, Zhipu | 中文理解强 |

### 性能 vs 成本权衡

```python
# 高性能配置
reasoning_agent = Agent(
    model=Claude(id="claude-opus-4-5"),  # 最强模型
    reasoning=True,
)

# 平衡配置
balanced_agent = Agent(
    model=OpenAI(id="gpt-4o"),           # 性价比
)

# 成本优化配置
cost_agent = Agent(
    model=OpenAI(id="gpt-4o-mini"),      # 便宜
)

# 混合配置：主模型 + 便宜的辅助模型
agent = Agent(
    model=OpenAI(id="gpt-4o"),           # 主要推理
    memory_manager=MemoryManager(
        model=OpenAI(id="gpt-4o-mini")   # 记忆提取用便宜模型
    )
)
```

## 多模态支持

### 图像输入

```python
from agno.media import Image

agent = Agent(model=OpenAI(id="gpt-4o"))

# 从 URL
response = agent.run(
    "描述这张图片",
    images=[Image(url="https://example.com/image.jpg")]
)

# 从本地文件
response = agent.run(
    "这张图片里有什么？",
    images=[Image(path="/path/to/image.png")]
)

# 从 Base64
response = agent.run(
    "分析这张图表",
    images=[Image(base64="iVBORw0KGgo...")]
)

# 多张图片
response = agent.run(
    "比较这两张图片",
    images=[
        Image(path="image1.jpg"),
        Image(path="image2.jpg")
    ]
)
```

### 音频输入

```python
from agno.media import Audio

agent = Agent(model=OpenAI(id="gpt-4o-audio-preview"))

response = agent.run(
    "转录并总结这段音频",
    audio=Audio(path="/path/to/audio.mp3")
)
```

### 视频输入

```python
from agno.media import Video

agent = Agent(model=Gemini(id="gemini-1.5-pro"))

response = agent.run(
    "描述这个视频的内容",
    video=Video(path="/path/to/video.mp4")
)
```

## 高级配置

### 通用参数

```python
model = OpenAI(
    id="gpt-4o",

    # 生成参数
    temperature=0.7,           # 创造性 (0-2)
    max_tokens=4096,           # 最大输出长度
    top_p=1.0,                 # 核采样
    frequency_penalty=0.0,     # 频率惩罚
    presence_penalty=0.0,      # 存在惩罚

    # API 配置
    api_key="sk-...",
    base_url="https://api.openai.com/v1",  # 自定义端点
    timeout=30,                # 超时秒数

    # 重试配置
    max_retries=3,
)
```

### 流式配置

```python
model = OpenAI(
    id="gpt-4o",
    stream=True,               # 默认启用流式
    stream_options={
        "include_usage": True  # 包含 token 使用统计
    }
)
```

### 响应格式

```python
# JSON 模式
model = OpenAI(
    id="gpt-4o",
    response_format={"type": "json_object"}
)

# 结构化输出
from pydantic import BaseModel

class Response(BaseModel):
    answer: str
    confidence: float

agent = Agent(
    model=OpenAI(id="gpt-4o"),
    output_schema=Response,
    structured_outputs=True,   # 使用原生结构化输出
)
```

### 自定义 HTTP 客户端

```python
import httpx

custom_client = httpx.Client(
    proxies="http://proxy:8080",
    verify=False,
)

model = OpenAI(
    id="gpt-4o",
    http_client=custom_client
)
```

### 环境变量配置

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Google
export GOOGLE_API_KEY="AIza..."

# Groq
export GROQ_API_KEY="gsk_..."
```

```python
# 自动从环境变量读取
model = OpenAI(id="gpt-4o")  # 自动使用 OPENAI_API_KEY
model = Claude(id="claude-sonnet-4-5")  # 自动使用 ANTHROPIC_API_KEY
```

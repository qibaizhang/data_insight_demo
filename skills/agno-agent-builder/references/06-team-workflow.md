# 多智能体 Team 与 Workflow 指南

## 目录

- [Team vs Workflow](#team-vs-workflow)
- [Team 多智能体团队](#team-多智能体团队)
- [Workflow 工作流](#workflow-工作流)
- [高级模式](#高级模式)
- [实战示例](#实战示例)

## Team vs Workflow

### 核心区别

| 特性 | Team | Workflow |
|------|------|----------|
| **执行顺序** | 动态（Leader 决定） | 显式（你定义） |
| **Agent 协作** | 可来回讨论 | 单向数据流 |
| **可预测性** | 低 | 高 |
| **适用场景** | 讨论、分析、创意 | 流程、管道、处理 |

### 选择指南

```
需要多角度讨论？        → Team
需要确定性流程？        → Workflow
需要 Agent 互相协作？   → Team
需要顺序处理步骤？      → Workflow
输出需要高度可预测？    → Workflow
需要灵活的决策？        → Team
```

## Team 多智能体团队

### 基础配置

```python
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAI

# 创建成员 Agent
researcher = Agent(
    name="研究员",
    model=OpenAI(id="gpt-4o"),
    role="负责信息收集和事实核查",
    tools=[DuckDuckGoTools()],
)

writer = Agent(
    name="作家",
    model=OpenAI(id="gpt-4o"),
    role="负责内容创作和润色",
)

# 创建 Team
team = Team(
    name="内容创作团队",
    model=OpenAI(id="gpt-4o"),       # Leader 模型
    members=[researcher, writer],
    instructions="""
    你领导一个内容创作团队。
    工作流程：
    1. 让研究员收集相关信息
    2. 让作家基于信息创作内容
    3. 审核并输出最终内容
    """,
    show_members_responses=True,     # 显示成员回复
)

team.print_response("写一篇关于 AI 发展趋势的文章", stream=True)
```

### Team 配置选项

```python
team = Team(
    name="团队名称",
    model=OpenAI(id="gpt-4o"),        # Leader 模型
    members=[agent1, agent2],          # 成员列表

    # 指令
    instructions="团队工作指令...",

    # 显示选项
    show_members_responses=True,       # 显示成员回复

    # 存储
    db=SqliteDb(db_file="team.db"),
    add_history_to_context=True,

    # 输出
    markdown=True,
    output_schema=TeamOutput,          # 结构化输出
)
```

### 对立分析模式

```python
# 看多分析师
bull_analyst = Agent(
    name="看多分析师",
    model=OpenAI(id="gpt-4o"),
    role="看多派，寻找投资正面理由",
    tools=[YFinanceTools()],
    instructions="""
    你是看多派分析师，专注于：
    - 发现公司的增长潜力
    - 识别竞争优势
    - 分析正面催化剂
    - 论证买入理由
    """
)

# 看空分析师
bear_analyst = Agent(
    name="看空分析师",
    model=OpenAI(id="gpt-4o"),
    role="看空派，寻找投资风险",
    tools=[YFinanceTools()],
    instructions="""
    你是看空派分析师，专注于：
    - 发现潜在风险和问题
    - 识别估值泡沫
    - 分析负面因素
    - 论证谨慎理由
    """
)

# 投资研究团队
investment_team = Team(
    name="投资研究团队",
    model=OpenAI(id="gpt-4o"),
    members=[bull_analyst, bear_analyst],
    instructions="""
    你是首席投资官，领导多空分析团队。

    工作流程：
    1. 让看多分析师分析正面因素
    2. 让看空分析师分析风险因素
    3. 综合双方观点
    4. 给出平衡的投资建议

    输出格式：
    ## 看多观点
    [看多分析师的分析]

    ## 看空观点
    [看空分析师的分析]

    ## 综合建议
    [你的平衡建议]
    """,
    show_members_responses=True,
)

investment_team.print_response("分析特斯拉是否值得投资", stream=True)
```

### 专家团队模式

```python
# 技术专家
tech_expert = Agent(
    name="技术专家",
    role="评估技术可行性和架构",
    model=OpenAI(id="gpt-4o"),
)

# 产品专家
product_expert = Agent(
    name="产品专家",
    role="评估产品价值和用户需求",
    model=OpenAI(id="gpt-4o"),
)

# 商业专家
business_expert = Agent(
    name="商业专家",
    role="评估商业模式和市场机会",
    model=OpenAI(id="gpt-4o"),
)

# 评审团队
review_team = Team(
    name="产品评审委员会",
    model=OpenAI(id="gpt-4o"),
    members=[tech_expert, product_expert, business_expert],
    instructions="""
    你主持产品评审会议。

    1. 让技术专家评估技术方案
    2. 让产品专家评估产品价值
    3. 让商业专家评估商业可行性
    4. 综合各方意见做出决策
    """
)

review_team.print_response("评审这个 AI 助手产品方案", stream=True)
```

## Workflow 工作流

### 基础配置

```python
from agno.workflow import Workflow, Step
from agno.agent import Agent

# 步骤 1: 数据收集
data_agent = Agent(
    name="数据收集器",
    model=OpenAI(id="gpt-4o"),
    tools=[YFinanceTools(), DuckDuckGoTools()],
    instructions="收集相关数据和信息"
)

# 步骤 2: 分析处理
analysis_agent = Agent(
    name="分析师",
    model=OpenAI(id="gpt-4o"),
    instructions="分析数据并得出结论"
)

# 步骤 3: 报告生成
report_agent = Agent(
    name="报告撰写",
    model=OpenAI(id="gpt-4o"),
    instructions="生成结构化报告"
)

# 创建工作流
workflow = Workflow(
    name="研究报告管道",
    steps=[
        Step(name="数据收集", agent=data_agent),
        Step(name="分析处理", agent=analysis_agent),
        Step(name="报告生成", agent=report_agent),
    ]
)

workflow.run("研究 2024 年 AI 行业发展趋势")
```

### 并行执行

```python
from agno.workflow import Workflow, Step, Parallel

# 并行研究步骤
parallel_research = Parallel(
    steps=[
        Step(name="技术研究", agent=tech_researcher),
        Step(name="市场研究", agent=market_researcher),
        Step(name="竞品研究", agent=competitor_researcher),
    ]
)

workflow = Workflow(
    name="综合研究",
    steps=[
        parallel_research,                    # 并行执行
        Step(name="综合分析", agent=analyst),  # 汇总分析
        Step(name="报告输出", agent=reporter), # 生成报告
    ]
)
```

### 条件分支

```python
from agno.workflow import Workflow, Step, Condition

def needs_deep_analysis(context):
    """判断是否需要深度分析"""
    return context.get("complexity", "low") == "high"

# 条件分支
analysis_branch = Condition(
    condition=needs_deep_analysis,
    if_true=Step(name="深度分析", agent=deep_analyst),
    if_false=Step(name="快速摘要", agent=summarizer),
)

workflow = Workflow(
    name="智能分析",
    steps=[
        Step(name="初步评估", agent=evaluator),
        analysis_branch,                      # 根据条件选择
        Step(name="输出结果", agent=reporter),
    ]
)
```

### 循环执行

```python
from agno.workflow import Workflow, Step, Loop

def quality_check(context):
    """检查质量是否达标"""
    return context.get("quality_score", 0) >= 0.8

# 循环直到质量达标
refinement_loop = Loop(
    step=Step(name="优化", agent=refiner),
    condition=quality_check,
    max_iterations=3,
)

workflow = Workflow(
    name="质量优化",
    steps=[
        Step(name="初稿", agent=writer),
        refinement_loop,                      # 循环优化
        Step(name="最终输出", agent=finalizer),
    ]
)
```

### 动态路由

```python
from agno.workflow import Workflow, Step, Router

def route_by_type(context):
    """根据类型路由"""
    query_type = context.get("type", "general")
    return query_type

# 路由器
type_router = Router(
    router_function=route_by_type,
    routes={
        "finance": Step(name="金融处理", agent=finance_agent),
        "tech": Step(name="技术处理", agent=tech_agent),
        "general": Step(name="通用处理", agent=general_agent),
    }
)

workflow = Workflow(
    name="智能路由",
    steps=[
        Step(name="分类", agent=classifier),
        type_router,                          # 动态路由
        Step(name="输出", agent=output_agent),
    ]
)
```

## 高级模式

### Team 中使用 Workflow

```python
# 每个成员是一个 Workflow
research_workflow = Workflow(
    name="研究流程",
    steps=[
        Step(name="搜索", agent=search_agent),
        Step(name="摘要", agent=summary_agent),
    ]
)

writing_workflow = Workflow(
    name="写作流程",
    steps=[
        Step(name="起草", agent=draft_agent),
        Step(name="润色", agent=polish_agent),
    ]
)

# Team 使用 Workflow 作为成员
content_team = Team(
    name="内容团队",
    model=OpenAI(id="gpt-4o"),
    members=[research_workflow, writing_workflow],
    instructions="协调研究和写作流程"
)
```

### 嵌套 Team

```python
# 子团队 1: 研究团队
research_team = Team(
    name="研究团队",
    members=[researcher1, researcher2],
    model=OpenAI(id="gpt-4o"),
)

# 子团队 2: 创作团队
creative_team = Team(
    name="创作团队",
    members=[writer, designer],
    model=OpenAI(id="gpt-4o"),
)

# 主团队
main_team = Team(
    name="项目团队",
    members=[research_team, creative_team],
    model=OpenAI(id="gpt-4o"),
    instructions="协调研究团队和创作团队完成项目"
)
```

### 状态传递

```python
from agno.workflow import Workflow, Step

workflow = Workflow(
    name="状态传递示例",
    steps=[
        Step(name="步骤1", agent=agent1),
        Step(name="步骤2", agent=agent2),
    ],
    # 初始状态
    initial_state={
        "project": "AI 助手",
        "deadline": "2024-12-31"
    }
)

# 每个步骤可以访问和修改状态
# agent 通过 session_state 获取状态
```

## 实战示例

### 内容创作管道

```python
from agno.agent import Agent
from agno.workflow import Workflow, Step
from agno.models.openai import OpenAI
from agno.tools.duckduckgo import DuckDuckGoTools

# 步骤 1: 选题研究
topic_researcher = Agent(
    name="选题研究员",
    model=OpenAI(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions="""
    研究给定主题的热点和趋势。
    输出：
    - 3-5 个热门子话题
    - 每个话题的关键点
    - 建议的文章角度
    """
)

# 步骤 2: 大纲生成
outline_creator = Agent(
    name="大纲作者",
    model=OpenAI(id="gpt-4o"),
    instructions="""
    基于研究结果创建详细大纲。
    输出：
    - 文章标题
    - 引言要点
    - 3-5 个主要章节及要点
    - 结论要点
    """
)

# 步骤 3: 内容撰写
content_writer = Agent(
    name="内容作者",
    model=OpenAI(id="gpt-4o"),
    instructions="""
    根据大纲撰写完整文章。
    要求：
    - 流畅自然的语言
    - 每个章节 200-300 字
    - 包含具体例子
    - SEO 友好
    """
)

# 步骤 4: 编辑润色
editor = Agent(
    name="编辑",
    model=OpenAI(id="gpt-4o"),
    instructions="""
    编辑和润色文章。
    检查：
    - 语法和拼写
    - 逻辑流畅性
    - 表达清晰度
    - 整体质量
    """
)

# 创建工作流
content_pipeline = Workflow(
    name="内容创作管道",
    steps=[
        Step(name="选题研究", agent=topic_researcher),
        Step(name="大纲生成", agent=outline_creator),
        Step(name="内容撰写", agent=content_writer),
        Step(name="编辑润色", agent=editor),
    ]
)

# 运行
result = content_pipeline.run("人工智能在医疗领域的应用")
print(result.content)
```

### 客服升级系统

```python
from agno.team import Team
from agno.workflow import Workflow, Step, Condition

# 一线客服
tier1_agent = Agent(
    name="一线客服",
    model=OpenAI(id="gpt-4o-mini"),  # 便宜模型
    tools=[CustomerServiceToolkit()],
    instructions="处理常见问题，复杂问题升级"
)

# 二线技术支持
tier2_agent = Agent(
    name="二线技术",
    model=OpenAI(id="gpt-4o"),
    tools=[TechSupportToolkit()],
    instructions="处理技术问题"
)

# 高级专家
expert_agent = Agent(
    name="高级专家",
    model=OpenAI(id="gpt-4o"),
    instructions="处理复杂和敏感问题"
)

def needs_escalation(context):
    return context.get("escalation_needed", False)

def needs_expert(context):
    return context.get("expert_needed", False)

# 升级工作流
support_workflow = Workflow(
    name="客服升级系统",
    steps=[
        Step(name="一线处理", agent=tier1_agent),
        Condition(
            condition=needs_escalation,
            if_true=Step(name="二线处理", agent=tier2_agent),
            if_false=Step(name="完成", agent=None),  # 直接结束
        ),
        Condition(
            condition=needs_expert,
            if_true=Step(name="专家处理", agent=expert_agent),
        ),
    ]
)
```

### 投资决策委员会

```python
from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

# 基本面分析师
fundamental_analyst = Agent(
    name="基本面分析师",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    instructions="""
    分析公司基本面：
    - 财务报表分析
    - 盈利能力评估
    - 现金流分析
    - 估值水平判断
    """
)

# 技术面分析师
technical_analyst = Agent(
    name="技术面分析师",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    instructions="""
    分析技术面：
    - 价格走势分析
    - 成交量分析
    - 技术指标解读
    - 支撑阻力位判断
    """
)

# 宏观分析师
macro_analyst = Agent(
    name="宏观分析师",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[DuckDuckGoTools()],
    instructions="""
    分析宏观环境：
    - 行业发展趋势
    - 政策影响
    - 竞争格局
    - 市场情绪
    """
)

# 风险官
risk_officer = Agent(
    name="风险官",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="""
    评估投资风险：
    - 市场风险
    - 流动性风险
    - 信用风险
    - 操作风险
    给出风险评级和建议仓位
    """
)

# 投资委员会
investment_committee = Team(
    name="投资决策委员会",
    model=Claude(id="claude-sonnet-4-5"),
    members=[
        fundamental_analyst,
        technical_analyst,
        macro_analyst,
        risk_officer
    ],
    instructions="""
    你是投资委员会主席，负责协调分析师团队做出投资决策。

    决策流程：
    1. 让基本面分析师评估公司价值
    2. 让技术面分析师判断入场时机
    3. 让宏观分析师评估行业和政策环境
    4. 让风险官评估风险并建议仓位
    5. 综合所有意见做出最终决策

    输出格式：
    ## 基本面分析
    [基本面分析师观点]

    ## 技术面分析
    [技术面分析师观点]

    ## 宏观分析
    [宏观分析师观点]

    ## 风险评估
    [风险官观点]

    ## 投资决策
    - 建议：买入/持有/卖出
    - 目标价：
    - 止损价：
    - 建议仓位：
    - 理由：
    """,
    show_members_responses=True,
)

# 使用
investment_committee.print_response(
    "分析苹果公司(AAPL)是否值得投资",
    stream=True
)
```

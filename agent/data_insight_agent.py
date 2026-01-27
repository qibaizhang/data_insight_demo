"""
DataInsight Agent

Main AI agent for data analysis, chart generation, and report creation.
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

from config import config
from agent.tools.sql_query_tool import SQLQueryToolkit
from agent.tools.chart_tool import ChartToolkit
from agent.tools.report_tool import ReportToolkit
from agent.tools.export_tool import ExportToolkit
from agent.prompts.system_prompt import SYSTEM_PROMPT


def create_data_insight_agent(
    model_id: str = None,
    datasource: str = 'sqlite'
) -> Agent:
    """
    Create a DataInsight agent instance

    Args:
        model_id: LLM model ID (defaults to config.DEFAULT_MODEL)
        datasource: Data source type (demo only supports 'sqlite')

    Returns:
        Configured Agent instance
    """

    model_id = model_id or config.DEFAULT_MODEL

    # Initialize database for session storage
    db = SqliteDb(db_file=config.SESSION_DB_PATH)

    # Initialize LLM model
    model = OpenAIChat(
        id=model_id,
        api_key=config.OPENAI_API_KEY,
        base_url=config.OPENAI_BASE_URL,
    )

    # Memory model (use MEMORY_MODEL if set, otherwise use the main model)
    memory_model_id = config.MEMORY_MODEL or model_id

    # Initialize memory manager (for user preferences)
    memory_manager = MemoryManager(
        model=OpenAIChat(
            id=memory_model_id,
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL,
        ),
        db=db,
        additional_instructions="""
        记住用户的：
        - 常用的数据查询偏好
        - 喜欢的图表类型
        - 关注的业务指标
        - 报告格式偏好
        """
    )

    # Create agent
    agent = Agent(
        name='DataInsight',
        id='data-insight-agent',
        model=model,
        db=db,

        # Instructions
        # Instructions - use replace instead of format to avoid conflicts with JSON examples
        instructions=SYSTEM_PROMPT.replace('{datasource}', datasource),

        # Tools
        tools=[
            SQLQueryToolkit(datasource=datasource),
            ChartToolkit(),
            ReportToolkit(),
            ExportToolkit(),
        ],
        tool_call_limit=10,

        # Memory
        memory_manager=memory_manager,
        enable_agentic_memory=True,
        add_memories_to_context=True,

        # History
        add_history_to_context=True,
        num_history_runs=5,

        # Context
        add_datetime_to_context=True,
        timezone_identifier='Asia/Shanghai',

        # Output
        markdown=True,
    )

    return agent


# Global agent instance cache
_agent_cache: dict[str, Agent] = {}


def get_agent(model_id: str = None, datasource: str = 'sqlite') -> Agent:
    """
    Get or create a cached agent instance

    Args:
        model_id: LLM model ID
        datasource: Data source type

    Returns:
        Agent instance
    """
    cache_key = f'{model_id or config.DEFAULT_MODEL}:{datasource}'

    if cache_key not in _agent_cache:
        _agent_cache[cache_key] = create_data_insight_agent(
            model_id=model_id,
            datasource=datasource
        )

    return _agent_cache[cache_key]

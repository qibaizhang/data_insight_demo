"""
Chat API Endpoints

Provides SSE streaming endpoint for chat interactions.
Uses time-window batching for efficient content streaming.
"""
import json
import re
import time
import uuid
from flask import Blueprint, request, Response, stream_with_context
from typing import Generator, Tuple

from agno.agent import RunContentEvent, ToolCallStartedEvent, ToolCallCompletedEvent
from agent.data_insight_agent import create_data_insight_agent
from services.schema_service import schema_service
from utils.helpers import generate_session_id, safe_json_serialize


chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Time window for batching content (seconds)
TIME_WINDOW = 0.01  # Very small for fast response - reduced further

# Report-related keywords detection
INFOGRAPHIC_KEYWORDS = ['信息图', '可视化报告', '像ppt', '像PPT', 'ppt风格', 'PPT风格', '卡片式', '指标卡']
REPORT_KEYWORDS = ['报告', '洞察', '概览', '总结', '汇总', '分析报告', '业务报告', '数据报告']


def detect_report_intent(message: str) -> Tuple[bool, bool]:
    """
    Detect if user wants a report and what type.

    Args:
        message: User message

    Returns:
        Tuple of (wants_report, wants_infographic)
    """
    message_lower = message.lower()

    # Check for infographic keywords first (more specific)
    wants_infographic = any(kw in message for kw in INFOGRAPHIC_KEYWORDS)

    # Check for general report keywords
    wants_report = any(kw in message for kw in REPORT_KEYWORDS)

    return wants_report, wants_infographic


def enhance_message_for_report(message: str, wants_report: bool, wants_infographic: bool) -> str:
    """
    Enhance user message with tool calling hints.

    Args:
        message: Original user message
        wants_report: Whether user wants a report
        wants_infographic: Whether user wants an infographic

    Returns:
        Enhanced message with tool hints
    """
    if not wants_report:
        return message

    if wants_infographic:
        hint = """

【系统提示】用户请求生成信息图报告。
⚠️ 必须调用 create_infographic 工具！
- 先查询所需数据
- 然后调用 create_infographic(syntax="infographic list-grid-badge-card\\ndata\\n  title 标题\\n  lists\\n    - label 指标名\\n      value 数值")
- 不要只在聊天中输出，必须调用工具让报告显示在右侧面板"""
    else:
        hint = """

【系统提示】用户请求生成报告。
⚠️ 必须调用 create_report 工具！
- 先查询所需数据
- 然后调用 create_report(content="# 报告标题\\n\\n## 内容...")
- 不要只在聊天中输出，必须调用工具让报告显示在右侧面板"""

    return message + hint


def stream_chat_response(
    message: str,
    session_id: str,
    datasource: str,
    model: str
) -> Generator[str, None, None]:
    """
    Generate streaming chat response with time-window batching.

    Args:
        message: User message
        session_id: Session identifier
        datasource: Data source type
        model: Model identifier

    Yields:
        SSE formatted events
    """
    try:
        # Create agent
        agent = create_data_insight_agent(model_id=model, datasource=datasource)

        # Get schema context
        schema_prompt = schema_service.get_schema_prompt(datasource)

        # Detect report intent and enhance message
        wants_report, wants_infographic = detect_report_intent(message)
        enhanced_message = enhance_message_for_report(message, wants_report, wants_infographic)

        if wants_report:
            report_type = "infographic" if wants_infographic else "markdown"
            print(f"[DEBUG] Report intent detected: {report_type}")

        # Build context message
        context_message = f"""
当前数据源: {datasource}

数据库Schema信息:
{schema_prompt}

用户问题: {enhanced_message}
"""

        # Run agent with streaming
        response = agent.run(
            context_message,
            session_id=session_id,
            stream=True,
            stream_events=True  # Enable tool call events for chart/data
        )

        # Content buffer for batching
        chunks = []
        last_send_time = time.time()
        all_content = []  # Track all content for final message

        def flush_content():
            """Flush buffered content"""
            nonlocal chunks, last_send_time
            if chunks:
                content = "".join(chunks)
                chunks = []
                last_send_time = time.time()
                # Filter out tool execution markers and empty content
                if content.strip():
                    all_content.append(content)  # Track for final message
                    return "data: {}\n\n".format(
                        json.dumps(
                            {"content": content, "uuid": str(uuid.uuid4())},
                            ensure_ascii=False
                        )
                    )
            return None

        def is_tool_output(text):
            """Check if text is tool execution output that should be filtered"""
            if not text:
                return False
            # Only filter very specific tool output patterns
            # Be conservative to avoid filtering real content
            tool_patterns = [
                'H: Tool execution result:',
                'Tool name:',
                'Parameters: {',
                '</tool_result>',
                '<tool_result>',
            ]
            return any(pattern in text for pattern in tool_patterns)

        for chunk in response:
            # Handle content events
            if isinstance(chunk, RunContentEvent):
                content_delta = chunk.content
                if content_delta:
                    # Skip tool execution output
                    if is_tool_output(content_delta):
                        print(f"[DEBUG] Skipping tool output: {content_delta[:100]}...")
                        continue

                    chunks.append(content_delta)

                    # Send when time window exceeded
                    if time.time() - last_send_time > TIME_WINDOW:
                        flushed = flush_content()
                        if flushed:
                            yield flushed

            # Handle tool call completed events
            elif isinstance(chunk, ToolCallCompletedEvent):
                # Flush any pending content before processing tool result
                flushed = flush_content()
                if flushed:
                    yield flushed

                tool_result = chunk.tool.result if hasattr(chunk.tool, 'result') else None

                # Parse tool result if it's a string
                if isinstance(tool_result, str):
                    try:
                        tool_result = json.loads(tool_result)
                    except json.JSONDecodeError:
                        try:
                            import ast
                            tool_result = ast.literal_eval(tool_result)
                        except (ValueError, SyntaxError):
                            tool_result = None

                if tool_result and isinstance(tool_result, dict):
                    tool_name = chunk.tool.name if hasattr(chunk.tool, 'name') else 'unknown'
                    print(f"[DEBUG] Tool completed: {tool_name}, result keys: {tool_result.keys()}")

                    # Check for chart config
                    if 'config' in tool_result and tool_result.get('success'):
                        config = tool_result['config']
                        if isinstance(config, dict) and 'type' in config:
                            print(f"[DEBUG] Sending chart config: {config.get('type')}")
                            yield "data: {}\n\n".format(
                                json.dumps(
                                    {"chart": config, "uuid": str(uuid.uuid4())},
                                    ensure_ascii=False
                                )
                            )

                    # Check for query data result
                    if tool_result.get('success') and 'data' in tool_result and 'columns' in tool_result:
                        print(f"[DEBUG] Sending query data, rows: {len(tool_result.get('data', []))}")
                        yield "data: {}\n\n".format(
                            json.dumps(
                                {
                                    "data": {
                                        'columns': tool_result['columns'],
                                        'data': tool_result['data'][:100]
                                    },
                                    "uuid": str(uuid.uuid4())
                                },
                                ensure_ascii=False
                            )
                        )

                    # Check for report content - 检测 format 字段表示这是报告工具的输出
                    if 'format' in tool_result:
                        report_content = tool_result.get('content', '')
                        report_format = tool_result.get('format', 'markdown')
                        print(f"[DEBUG] Sending report, format: {report_format}, content length: {len(report_content)}")
                        # 打印 infographic 内容的前 200 字符用于调试
                        if report_format == 'infographic':
                            print(f"[DEBUG] Infographic content preview:\n{report_content[:500]}")
                        yield "data: {}\n\n".format(
                            json.dumps(
                                {
                                    "report": {
                                        "format": report_format,
                                        "content": report_content
                                    },
                                    "uuid": str(uuid.uuid4())
                                },
                                ensure_ascii=False
                            )
                        )

        # Flush remaining content in buffer
        flushed = flush_content()
        if flushed:
            yield flushed

        # Build complete content
        full_content = "".join(all_content)
        print(f"[DEBUG] Stream complete, total content length: {len(full_content)}")

        # Send complete signal with full content for reliability
        yield "data: {}\n\n".format(
            json.dumps(
                {"complete": True, "fullContent": full_content, "uuid": str(uuid.uuid4())},
                ensure_ascii=False
            )
        )

    except Exception as e:
        import traceback
        print(f"[ERROR] Exception in stream_chat_response: {e}")
        print(f"[ERROR] Traceback:\n{traceback.format_exc()}")
        yield "data: {}\n\n".format(
            json.dumps(
                {"error": str(e), "uuid": str(uuid.uuid4())},
                ensure_ascii=False
            )
        )


@chat_bp.route('/stream', methods=['GET'])
def chat_stream():
    """
    SSE endpoint for streaming chat responses

    Query Parameters:
        - message: User message (required)
        - session_id: Session identifier (optional, will generate if not provided)
        - datasource: Data source type (default: 'sqlite')
        - model: Model identifier (optional, uses default from config)
    """
    message = request.args.get('message', '')
    session_id = request.args.get('session_id') or generate_session_id()
    datasource = request.args.get('datasource', 'sqlite')
    model = request.args.get('model')

    if not message:
        return Response(
            format_sse_event({'type': 'error', 'message': '消息不能为空'}, 'error'),
            mimetype='text/event-stream'
        )

    return Response(
        stream_with_context(stream_chat_response(message, session_id, datasource, model)),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )


@chat_bp.route('/sessions', methods=['GET'])
def list_sessions():
    """List all chat sessions"""
    from services.session_service import session_service

    sessions = session_service.list_sessions()
    return {'sessions': sessions}


@chat_bp.route('/sessions/<session_id>', methods=['GET'])
def get_session(session_id: str):
    """Get session details and history"""
    from services.session_service import session_service

    session = session_service.get_session(session_id)
    if not session:
        return {'error': '会话不存在'}, 404

    return session


@chat_bp.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id: str):
    """Delete a session"""
    from services.session_service import session_service

    success = session_service.delete_session(session_id)
    if not success:
        return {'error': '删除失败'}, 500

    return {'success': True}

"""
Chat Callbacks

Handles chat input, message display, and SSE streaming.
Reference: deepseek-r1-online-chat-app pattern
"""
import json
import uuid
from dash import Input, Output, State, callback, ctx, Patch, no_update, set_props, html, ClientsideFunction
import feffery_antd_components as fac
import feffery_markdown_components as fmc

from server import app
from views.chat_panel import message_bubble


@callback(
    Output('chat-messages-container', 'children', allow_duplicate=True),
    Output('chat-input', 'value'),
    Output('streaming-response-container', 'style'),
    Output('streaming-markdown', 'markdownStr'),
    Output('chat-sse-source', 'url'),
    Output('chat-sse-source', 'immediate'),
    Input('send-message-btn', 'nClicks'),
    State('chat-input', 'value'),
    State('chat-messages-container', 'children'),
    State('current-session-id', 'data'),
    State('current-datasource', 'data'),
    State('current-model', 'data'),
    prevent_initial_call=True
)
def send_message(n_clicks, message, current_messages, session_id, datasource, model):
    """Handle message sending"""

    if not message or not message.strip():
        return no_update, no_update, no_update, no_update, no_update, no_update

    # Generate session ID if not exists
    if not session_id:
        session_id = str(uuid.uuid4())

    # Add user message to chat history
    patched_messages = Patch()
    patched_messages.append(message_bubble(message, is_user=True))

    # Build SSE URL
    sse_url = f'/api/chat/stream?session_id={session_id}&datasource={datasource}&model={model}&message={message}'

    return (
        patched_messages,
        '',  # Clear input
        {'display': 'block'},  # Show streaming response container
        '',  # Reset markdown content
        sse_url,
        True  # Enable SSE connection
    )


# Client-side callback for streaming response
# This directly updates the FefferyMarkdown component's markdownStr property
# Following the pattern from deepseek-r1-online-chat-app
app.clientside_callback(
    ClientsideFunction(namespace='datainsight', function_name='updateStreamingResponse'),
    Output('streaming-markdown', 'markdownStr', allow_duplicate=True),
    Input('chat-sse-source', 'data'),
    State('streaming-markdown', 'markdownStr'),
    prevent_initial_call=True
)


# Server-side callback to finalize response when stream completes
@callback(
    Output('chat-messages-container', 'children', allow_duplicate=True),
    Output('streaming-response-container', 'style', allow_duplicate=True),
    Output('streaming-markdown', 'markdownStr', allow_duplicate=True),
    Input('assistant-response-store', 'data'),
    prevent_initial_call=True
)
def finalize_assistant_response(content):
    """Move streaming response to history when complete"""

    # Content is now passed directly from the clientside callback
    if not content or not isinstance(content, str) or len(content) == 0:
        return no_update, no_update, no_update

    # Add the completed response to history
    patched_messages = Patch()
    patched_messages.append(
        fac.AntdSpace(
            [
                fac.AntdAvatar(
                    icon='antd-robot',
                    style={'backgroundColor': '#1890ff', 'flexShrink': 0}
                ),
                html.Div(
                    fmc.FefferyMarkdown(
                        markdownStr=content,
                        codeTheme='a11y-dark',
                        style={'lineHeight': 1.6}
                    ),
                    style={
                        'padding': '12px 16px',
                        'borderRadius': '12px',
                        'background': '#fff',
                        'maxWidth': '85%',
                        'boxShadow': '0 1px 2px rgba(0,0,0,0.05)',
                        'overflow': 'auto'
                    }
                ),
            ],
            align='start',
            style={'width': '100%', 'marginBottom': '16px'}
        )
    )

    return (
        patched_messages,
        {'display': 'none'},  # Hide streaming container
        ''  # Reset streaming markdown
    )


@callback(
    Output('current-model', 'data'),
    Input('model-selector', 'value'),
    prevent_initial_call=True
)
def update_model(model):
    """Update current model selection"""
    return model


@callback(
    Output('current-datasource', 'data'),
    Input('datasource-selector', 'value'),
    prevent_initial_call=True
)
def update_datasource(datasource):
    """Update current datasource selection"""
    return datasource

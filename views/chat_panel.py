"""
Chat Panel Component

Chat interface with message display and input area.
"""
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
import feffery_markdown_components as fmc
from feffery_dash_utils.style_utils import style


def chat_panel():
    """Build chat panel"""

    return html.Div(
        [
            # Chat messages area
            fuc.FefferyScrollbars(
                html.Div(
                    [
                        # Historical messages container
                        html.Div(
                            id='chat-messages-container',
                            children=[
                                _welcome_message(),
                            ],
                        ),
                        # Current streaming response area (separate from history)
                        html.Div(
                            id='streaming-response-container',
                            children=[
                                # Avatar + Markdown response
                                fac.AntdSpace(
                                    [
                                        fac.AntdAvatar(
                                            icon='antd-robot',
                                            style={'backgroundColor': '#1890ff', 'flexShrink': 0}
                                        ),
                                        html.Div(
                                            fmc.FefferyMarkdown(
                                                id='streaming-markdown',
                                                markdownStr='',
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
                                ),
                            ],
                            style={'display': 'none'}  # Hidden by default
                        ),
                    ],
                    style={'padding': '16px'}
                ),
                id='chat-scroll-container',
                style={'flex': 1, 'minHeight': 0},  # minHeight: 0 is critical for flex scrolling
                autoHide=True
            ),

            # Input area
            html.Div(
                [
                    fac.AntdInput(
                        id='chat-input',
                        placeholder='输入您的问题，例如：查询本月销售数据...',
                        mode='text-area',
                        autoSize={'minRows': 2, 'maxRows': 4},
                        allowClear=True,
                        style={'flex': 1}
                    ),
                    fac.AntdButton(
                        icon=fac.AntdIcon(icon='antd-send'),
                        id='send-message-btn',
                        type='primary',
                        style={'marginLeft': 8, 'alignSelf': 'flex-end'}
                    ),
                ],
                style=style(
                    display='flex',
                    padding=16,
                    borderTop='1px solid #f0f0f0',
                    background='#fff',
                    flexShrink=0,  # Prevent input area from shrinking
                )
            ),

            html.Div(
                id='chat-loading-indicator',
                children=fac.AntdSpin(
                    text='思考中...',
                    size='small'
                ),
                style={'display': 'none', 'padding': '8px 16px'}
            ),
        ],
        style=style(
            flex=1,
            display='flex',
            flexDirection='column',
            overflow='hidden',
            minHeight=0,  # Critical for nested flex containers
        )
    )


def _welcome_message():
    """Welcome message component"""

    return html.Div(
        fac.AntdCard(
            [
                fac.AntdSpace(
                    [
                        fac.AntdAvatar(
                            icon='antd-robot',
                            style={'backgroundColor': '#1890ff'}
                        ),
                        html.Div(
                            [
                                fac.AntdText(
                                    'DataInsight 助手',
                                    strong=True,
                                    style={'display': 'block'}
                                ),
                                fac.AntdText(
                                    '您好！我是数据分析助手，可以帮您：',
                                    type='secondary'
                                ),
                            ]
                        ),
                    ],
                    style={'marginBottom': 16}
                ),

                fac.AntdSpace(
                    [
                        fac.AntdTag(content='📊 查询数据', color='blue'),
                        fac.AntdTag(content='📈 生成图表', color='green'),
                        fac.AntdTag(content='📝 分析报告', color='purple'),
                        fac.AntdTag(content='📥 导出文件', color='orange'),
                    ],
                    wrap=True
                ),

                fac.AntdDivider(style={'margin': '16px 0'}),

                fac.AntdText(
                    '试试问我："查询最近7天的销售数据并生成趋势图"',
                    type='secondary',
                    italic=True
                ),
            ],
            variant='borderless',
            style={'background': '#f6ffed', 'borderRadius': 12}
        ),
        style={'marginBottom': 16}
    )


def message_bubble(content: str, is_user: bool = True, extra=None):
    """
    Create a message bubble component

    Args:
        content: Message content
        is_user: True for user message, False for assistant
        extra: Additional components (charts, tables, etc.)
    """

    avatar = fac.AntdAvatar(
        icon='antd-user' if is_user else 'antd-robot',
        style={'backgroundColor': '#87d068' if is_user else '#1890ff'}
    )

    message_content = html.Div(
        [
            fac.AntdText(content),
            extra if extra else None,
        ],
        style=style(
            padding='12px 16px',
            borderRadius=12,
            background='#e6f7ff' if is_user else '#fff',
            maxWidth='85%',
            boxShadow='0 1px 2px rgba(0,0,0,0.05)',
        )
    )

    if is_user:
        return fac.AntdSpace(
            [message_content, avatar],
            align='start',
            style={'justifyContent': 'flex-end', 'width': '100%', 'marginBottom': 16}
        )
    else:
        return fac.AntdSpace(
            [avatar, message_content],
            align='start',
            style={'width': '100%', 'marginBottom': 16}
        )

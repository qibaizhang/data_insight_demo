"""
Session List Component

Displays conversation history with management functions.
"""
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style


def session_list():
    """Build session list panel"""

    return html.Div(
        [
            # Header with new session button
            fac.AntdSpace(
                [
                    fac.AntdText('会话列表', strong=True),
                    fac.AntdButton(
                        icon=fac.AntdIcon(icon='antd-plus'),
                        id='new-session-btn',
                        type='primary',
                        size='small',
                    ),
                ],
                style={'width': '100%', 'justifyContent': 'space-between'}
            ),

            fac.AntdDivider(style={'margin': '12px 0'}),

            # Session list container
            fuc.FefferyScrollbars(
                html.Div(
                    id='session-list-container',
                    children=[
                        # Sessions will be rendered here
                        _session_item('新对话', '现在', True),
                    ]
                ),
                style={'flex': 1},
                autoHide=True
            ),
        ],
        style=style(
            padding=16,
            height=200,
            display='flex',
            flexDirection='column',
            borderBottom='1px solid #f0f0f0',
        )
    )


def _session_item(title: str, time: str, active: bool = False):
    """Build a single session item"""

    return fac.AntdSpace(
        [
            fac.AntdIcon(
                icon='antd-message',
                style={'color': '#1890ff' if active else '#999'}
            ),
            html.Div(
                [
                    fac.AntdText(
                        title,
                        ellipsis=True,
                        style={'display': 'block', 'maxWidth': 200}
                    ),
                    fac.AntdText(
                        time,
                        type='secondary',
                        style={'fontSize': 12}
                    ),
                ],
                style={'flex': 1}
            ),
            fac.AntdButton(
                icon=fac.AntdIcon(icon='antd-delete'),
                type='text',
                size='small',
                danger=True,
                id={'type': 'delete-session-btn', 'index': 'default'},
                style={'opacity': 0.5}
            ),
        ],
        style=style(
            width='100%',
            padding='8px 12px',
            borderRadius=8,
            cursor='pointer',
            background='#e6f7ff' if active else 'transparent',
            marginBottom=4,
        ),
        className='session-item'
    )

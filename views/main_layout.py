"""
Main Layout - Left-Right Split Design

Left Panel: Session list + Chat area
Right Panel: Chart/Report display area
"""
from dash import html, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style

from config import config
from views.chat_panel import chat_panel
from views.display_panel import display_panel


def main_layout():
    """Build main application layout"""

    return html.Div(
        [
            # Header
            _build_header(),

            # Main content area
            html.Div(
                [
                    # Left panel - Chat (collapsible)
                    html.Div(
                        [
                            chat_panel(),
                        ],
                        id='left-panel',
                        style=style(
                            width=400,
                            height='calc(100vh - 64px)',
                            display='flex',
                            flexDirection='column',
                            borderRight='1px solid #f0f0f0',
                            background='#fff',
                            transition='width 0.3s ease, opacity 0.3s ease',
                            overflow='hidden',
                        )
                    ),

                    # Right panel - Display
                    html.Div(
                        display_panel(),
                        style=style(
                            flex=1,
                            height='calc(100vh - 64px)',
                            overflow='auto',
                            background='#f5f5f5',
                            padding=16,
                        )
                    ),
                ],
                style=style(
                    display='flex',
                    height='calc(100vh - 64px)',
                )
            ),

            # Store for sidebar state
            dcc.Store(id='sidebar-collapsed-store', data=False),
        ],
        style=style(
            minHeight='100vh',
            background='#f5f5f5',
        )
    )


def _build_header():
    """Build application header"""

    return fac.AntdHeader(
        fac.AntdRow(
            [
                # Toggle sidebar button
                fac.AntdCol(
                    fac.AntdButton(
                        icon=fac.AntdIcon(icon='antd-menu-fold'),
                        id='toggle-sidebar-btn',
                        type='text',
                        style={'color': '#fff', 'fontSize': 18}
                    ),
                    flex='none'
                ),

                # Logo & Title
                fac.AntdCol(
                    fac.AntdSpace(
                        [
                            fac.AntdIcon(
                                icon='antd-line-chart',
                                style={'fontSize': 24, 'color': '#fff'}
                            ),
                            fac.AntdText(
                                'DataInsight',
                                strong=True,
                                style={'fontSize': 18, 'color': '#fff'}
                            ),
                        ],
                        size='middle'
                    ),
                    flex='none',
                    style={'marginLeft': 8}
                ),

                # Spacer
                fac.AntdCol(flex='auto'),

                # Model selector
                fac.AntdCol(
                    fac.AntdSpace(
                        [
                            fac.AntdText('模型:', style={'color': '#fff'}),
                            fac.AntdSelect(
                                id='model-selector',
                                options=[
                                    {'label': m, 'value': m}
                                    for m in config.AVAILABLE_MODELS
                                ],
                                value=config.DEFAULT_MODEL,
                                style={'width': 150},
                                size='small'
                            ),
                        ],
                        size='small'
                    ),
                    flex='none'
                ),

                # Data source selector
                fac.AntdCol(
                    fac.AntdSpace(
                        [
                            fac.AntdText('数据源:', style={'color': '#fff'}),
                            fac.AntdSelect(
                                id='datasource-selector',
                                options=[
                                    {'label': ds.upper(), 'value': ds}
                                    for ds in config.get_available_datasources()
                                ],
                                value='sqlite',
                                style={'width': 120},
                                size='small'
                            ),
                        ],
                        size='small'
                    ),
                    flex='none',
                    style={'marginLeft': 16}
                ),
            ],
            align='middle',
            style={'height': '100%', 'padding': '0 24px'}
        ),
        style=style(
            background='linear-gradient(90deg, #0f172a 0%, #1e3a5f 100%)',
            height=64,
            padding=0,
            lineHeight='64px',
        )
    )

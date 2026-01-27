"""
Display Panel Component

Right panel for displaying charts, tables, and reports.
"""
from dash import html
import feffery_antd_components as fac
import feffery_antd_charts as fact
import feffery_infographic as fi
import feffery_utils_components as fuc
from feffery_dash_utils.style_utils import style


def display_panel():
    """Build display panel"""

    return html.Div(
        [
            # Tabs for different display types
            fac.AntdTabs(
                id='display-tabs',
                items=[
                    {
                        'key': 'chart',
                        'label': fac.AntdSpace([
                            fac.AntdIcon(icon='antd-bar-chart'),
                            '图表'
                        ], size='small'),
                        'children': _chart_tab(),
                    },
                    {
                        'key': 'data',
                        'label': fac.AntdSpace([
                            fac.AntdIcon(icon='antd-table'),
                            '数据'
                        ], size='small'),
                        'children': _data_tab(),
                    },
                    {
                        'key': 'report',
                        'label': fac.AntdSpace([
                            fac.AntdIcon(icon='antd-file-text'),
                            '报告'
                        ], size='small'),
                        'children': _report_tab(),
                    },
                ],
                defaultActiveKey='chart',
                style={'background': '#fff', 'borderRadius': 8, 'padding': 16}
            ),
        ],
        style={'height': '100%'}
    )


def _chart_tab():
    """Chart display tab"""

    return html.Div(
        [
            # Export toolbar
            fac.AntdSpace(
                [
                    fac.AntdButton(
                        '导出图片',
                        id='export-chart-image-btn',
                        icon=fac.AntdIcon(icon='antd-download'),
                        size='small'
                    ),
                    fac.AntdButton(
                        '全屏',
                        id='fullscreen-chart-btn',
                        icon=fac.AntdIcon(icon='antd-fullscreen'),
                        size='small'
                    ),
                ],
                style={'marginBottom': 16}
            ),

            # Chart container
            html.Div(
                id='chart-display-container',
                children=_empty_chart_placeholder(),
                style=style(
                    minHeight=400,
                    border='1px dashed #d9d9d9',
                    borderRadius=8,
                    display='flex',
                    alignItems='center',
                    justifyContent='center',
                )
            ),

            # Infographic container (for reports with visuals)
            html.Div(
                id='infographic-display-container',
                style={'marginTop': 16, 'display': 'none'}
            ),

            # DOM to Image component (targetSelector initially None, set by callback)
            fuc.FefferyDom2Image(
                id='chart-to-image',
                scale=2
            ),

            # Fullscreen control
            fuc.FefferyFullscreen(
                id='chart-fullscreen-control',
                targetId='chart-display-container'
            ),
        ]
    )


def _data_tab():
    """Data table display tab"""

    return html.Div(
        [
            # Export toolbar
            fac.AntdSpace(
                [
                    fac.AntdButton(
                        '导出 CSV',
                        id='export-csv-btn',
                        icon=fac.AntdIcon(icon='antd-download'),
                        type='primary',
                        size='small'
                    ),
                    fac.AntdText(
                        id='data-row-count',
                        type='secondary',
                        style={'marginLeft': 16}
                    ),
                ],
                style={'marginBottom': 16}
            ),

            # Data table container
            html.Div(
                id='data-table-container',
                children=_empty_data_placeholder(),
            ),
        ]
    )


def _report_tab():
    """Report display tab"""

    return html.Div(
        [
            # Export toolbar
            fac.AntdSpace(
                [
                    fac.AntdButton(
                        '导出 Markdown',
                        id='export-markdown-btn',
                        icon=fac.AntdIcon(icon='antd-download'),
                        type='primary',
                        size='small'
                    ),
                ],
                style={'marginBottom': 16}
            ),

            # Report container
            html.Div(
                id='report-display-container',
                children=_empty_report_placeholder(),
                style=style(
                    minHeight=400,
                    padding=24,
                    background='#fafafa',
                    borderRadius=8,
                )
            ),
        ]
    )


def _empty_chart_placeholder():
    """Empty state for chart display"""

    return fac.AntdEmpty(
        description='暂无图表',
        image='https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg'
    )


def _empty_data_placeholder():
    """Empty state for data table"""

    return fac.AntdEmpty(
        description='暂无数据',
        image='https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg',
        style={'padding': 50}
    )


def _empty_report_placeholder():
    """Empty state for report"""

    return fac.AntdEmpty(
        description='暂无报告',
        image='https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg',
        style={'padding': 50}
    )

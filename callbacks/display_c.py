"""
Display Callbacks

Handles chart rendering, data table display, and report rendering.
"""
import json
from dash import Input, Output, State, callback, ctx, no_update, set_props, html
import feffery_antd_components as fac
import feffery_antd_charts as fact
import feffery_infographic as fi
import feffery_utils_components as fuc
import pandas as pd

from server import app


@callback(
    Output('chart-display-container', 'children'),
    Input('chart-config-store', 'data'),
    prevent_initial_call=True
)
def render_chart(config):
    """Render chart based on configuration from Agent"""

    if not config:
        return _empty_chart()

    chart_type = config.get('type', 'line')
    data = config.get('data', [])
    options = config.get('options', {})

    # Map chart type to fact component
    chart_components = {
        'line': fact.AntdLine,
        'bar': fact.AntdColumn,
        'pie': fact.AntdPie,
        'area': fact.AntdArea,
    }

    ChartComponent = chart_components.get(chart_type, fact.AntdLine)

    return ChartComponent(
        data=data,
        **options,
        style={'height': 400}
    )


@callback(
    Output('data-table-container', 'children'),
    Output('data-row-count', 'children'),
    Input('query-result-store', 'data'),
    prevent_initial_call=True
)
def render_data_table(data):
    """Render data table from query results"""

    if not data:
        return _empty_data(), ''

    # Handle SSE message format: {"type": "data", "columns": [...], "data": [...]}
    if isinstance(data, dict):
        columns_list = data.get('columns', [])
        rows = data.get('data', [])

        if columns_list and rows:
            # Convert to DataFrame using columns and data
            df = pd.DataFrame(rows, columns=columns_list)
        elif rows:
            # Fallback: rows might be list of dicts
            df = pd.DataFrame(rows)
        else:
            return _empty_data(), ''
    else:
        # Direct data array
        df = pd.DataFrame(data)

    if df.empty:
        return _empty_data(), ''

    columns = [
        {'title': col, 'dataIndex': col, 'key': col}
        for col in df.columns
    ]

    table = fac.AntdTable(
        columns=columns,
        data=df.to_dict('records'),
        bordered=True,
        size='small',
        pagination={
            'pageSize': 10,
            'showSizeChanger': True,
            'showQuickJumper': True,
            'pageSizeOptions': [10, 20, 50, 100],
        },
        maxHeight=400,  # Fixed height with scroll
        style={'marginTop': 8}
    )

    row_count = f'共 {len(df)} 条记录'

    return table, row_count


@callback(
    Output('report-display-container', 'children'),
    Input('report-content-store', 'data'),
    prevent_initial_call=True
)
def render_report(content):
    """Render report content"""

    if not content:
        return _empty_report()

    # Check if content contains infographic syntax
    if content.strip().startswith('infographic'):
        return fi.Infographic(
            syntax=content,
            editable=False,
            style={'minHeight': 400}
        )

    # Check if content contains HTML tags - use FefferyRawHtml to render
    if '<div' in content or '<table' in content or '<span' in content:
        return html.Div(
            fuc.FefferyRawHtml(
                rawHtml=content
            ),
            style={'padding': 16, 'background': '#fff', 'borderRadius': 8}
        )

    # Otherwise render as markdown with HTML support
    import feffery_markdown_components as fmc
    return fmc.FefferyMarkdown(
        markdownStr=content,
        renderHtml=True,  # Enable HTML rendering in markdown
        style={'padding': 16}
    )


@callback(
    Output('infographic-display-container', 'children'),
    Output('infographic-display-container', 'style'),
    Input('report-content-store', 'data'),
    prevent_initial_call=True
)
def render_infographic(content):
    """Render infographic if applicable"""

    if not content or not content.strip().startswith('infographic'):
        return no_update, {'display': 'none'}

    return (
        fi.Infographic(
            syntax=content,
            editable=False,
            style={'minHeight': 400}
        ),
        {'display': 'block', 'marginTop': 16}
    )


def _empty_chart():
    return fac.AntdEmpty(
        description='暂无图表',
        image='https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg'
    )


def _empty_data():
    return fac.AntdEmpty(
        description='暂无数据',
        image='https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg',
        style={'padding': 50}
    )


def _empty_report():
    return fac.AntdEmpty(
        description='暂无报告',
        image='https://gw.alipayobjects.com/zos/antfincdn/ZHrcdLPrvN/empty.svg',
        style={'padding': 50}
    )

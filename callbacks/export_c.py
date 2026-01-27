"""
Export Callbacks

Handles data export: CSV, Markdown report, chart images.
"""
import io
import json
from dash import Input, Output, State, callback, ctx, no_update, dcc, set_props
import feffery_antd_components as fac
import pandas as pd

from server import app


@callback(
    Output('global-download', 'data'),
    Input('export-csv-btn', 'nClicks'),
    State('query-result-store', 'data'),
    prevent_initial_call=True
)
def export_csv(n_clicks, data):
    """Export query results as CSV"""

    if not data:
        set_props('message-target', {
            'children': fac.AntdMessage(content='暂无数据可导出', type='warning')
        })
        return no_update

    # Handle SSE message format: {"type": "data", "columns": [...], "data": [...]}
    if isinstance(data, dict):
        columns_list = data.get('columns', [])
        rows = data.get('data', [])

        if columns_list and rows:
            df = pd.DataFrame(rows, columns=columns_list)
        elif rows:
            df = pd.DataFrame(rows)
        else:
            set_props('message-target', {
                'children': fac.AntdMessage(content='暂无数据可导出', type='warning')
            })
            return no_update
    else:
        df = pd.DataFrame(data)

    # Show success message
    set_props('message-target', {
        'children': fac.AntdMessage(content='正在导出 CSV...', type='info')
    })

    return dcc.send_data_frame(
        df.to_csv,
        'data_export.csv',
        index=False,
        encoding='utf-8-sig'  # For Excel compatibility
    )


@callback(
    Output('global-download', 'data', allow_duplicate=True),
    Input('export-markdown-btn', 'nClicks'),
    State('report-content-store', 'data'),
    prevent_initial_call=True
)
def export_markdown(n_clicks, content):
    """Export report as Markdown file"""

    if not content:
        set_props('message-target', {
            'children': fac.AntdMessage(content='暂无报告可导出', type='warning')
        })
        return no_update

    # Show success message
    set_props('message-target', {
        'children': fac.AntdMessage(content='正在导出报告...', type='info')
    })

    return dict(
        content=content,
        filename='analysis_report.md'
    )


@callback(
    Output('chart-to-image', 'targetSelector'),
    Input('export-chart-image-btn', 'nClicks'),
    prevent_initial_call=True
)
def trigger_chart_screenshot(n_clicks):
    """Trigger chart screenshot"""

    set_props('message-target', {
        'children': fac.AntdMessage(content='正在截图...', type='info')
    })

    return '#chart-display-container'


@callback(
    Output('global-download', 'data', allow_duplicate=True),
    Input('chart-to-image', 'screenshotResult'),
    prevent_initial_call=True
)
def download_chart_image(result):
    """Download chart screenshot"""

    if not result or result.get('status') != 'success':
        return no_update

    import base64

    # Extract base64 data
    data_url = result['dataUrl']
    # data:image/png;base64,xxxxx
    header, data = data_url.split(',', 1)
    image_data = base64.b64decode(data)

    set_props('message-target', {
        'children': fac.AntdMessage(content='图表已导出', type='success')
    })

    return dcc.send_bytes(
        image_data,
        'chart_export.png'
    )


@callback(
    Output('chart-fullscreen-control', 'isFullscreen'),
    Input('fullscreen-chart-btn', 'nClicks'),
    State('chart-fullscreen-control', 'isFullscreen'),
    prevent_initial_call=True
)
def toggle_chart_fullscreen(n_clicks, current):
    """Toggle chart fullscreen mode"""
    return not current

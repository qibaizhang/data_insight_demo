"""
DataInsight - AI-Powered Data Analysis Assistant

Main application entry point.
Assembles layout and registers callbacks.
"""
from dash import html, dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app, server
from config import config

# Import views
from views.main_layout import main_layout

# Import callbacks (must import to register)
import callbacks.chat_c
import callbacks.session_c
import callbacks.display_c
import callbacks.export_c


# ========================================
# Application Layout
# ========================================

app.layout = fac.AntdConfigProvider(
    locale='zh-cn',
    children=[
        # Global utility components
        fac.Fragment(id='message-target'),
        dcc.Download(id='global-download'),
        dcc.Store(id='current-session-id', storage_type='session'),
        dcc.Store(id='current-datasource', data='sqlite'),
        dcc.Store(id='current-model', data=config.DEFAULT_MODEL),
        dcc.Store(id='query-result-store', data=None),
        dcc.Store(id='chart-config-store', data=None),
        dcc.Store(id='report-content-store', data=None),
        dcc.Store(id='assistant-response-store', data=None),  # Store for assistant response content

        # SSE event source for streaming
        fuc.FefferyEventSource(
            id='chat-sse-source',
            url='',
            immediate=False
        ),

        # Main layout
        main_layout()
    ]
)


# ========================================
# Entry Point
# ========================================

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════╗
    ║         DataInsight Starting...        ║
    ╠════════════════════════════════════════╣
    ║  Available Data Sources:               ║
    ║  {', '.join(config.get_available_datasources()):<36} ║
    ║                                        ║
    ║  Available Models:                     ║
    ║  {', '.join(config.AVAILABLE_MODELS):<36} ║
    ╚════════════════════════════════════════╝
    """)

    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )

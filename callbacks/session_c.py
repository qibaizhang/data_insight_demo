"""
Session Callbacks

Handles session management and sidebar toggle.
"""
import uuid
from datetime import datetime
from dash import Input, Output, State, callback, ctx, Patch, no_update, set_props, clientside_callback
import feffery_antd_components as fac

from server import app


# Clientside callback for toggling sidebar
clientside_callback(
    """
    function(nClicks, isCollapsed) {
        if (!nClicks) {
            return [window.dash_clientside.no_update, window.dash_clientside.no_update];
        }

        const newCollapsed = !isCollapsed;

        // Update left panel style
        const leftPanelStyle = newCollapsed
            ? {
                width: 0,
                opacity: 0,
                overflow: 'hidden',
                padding: 0,
                height: 'calc(100vh - 64px)',
                display: 'flex',
                flexDirection: 'column',
                borderRight: '1px solid #f0f0f0',
                background: '#fff',
                transition: 'width 0.3s ease, opacity 0.3s ease'
              }
            : {
                width: 400,
                opacity: 1,
                overflow: 'hidden',
                height: 'calc(100vh - 64px)',
                display: 'flex',
                flexDirection: 'column',
                borderRight: '1px solid #f0f0f0',
                background: '#fff',
                transition: 'width 0.3s ease, opacity 0.3s ease'
              };

        // Update button icon using set_props
        window.dash_clientside.set_props('toggle-sidebar-btn', {
            icon: {
                'props': {'icon': newCollapsed ? 'antd-menu-unfold' : 'antd-menu-fold'},
                'type': 'AntdIcon',
                'namespace': 'feffery_antd_components'
            }
        });

        return [newCollapsed, leftPanelStyle];
    }
    """,
    Output('sidebar-collapsed-store', 'data'),
    Output('left-panel', 'style'),
    Input('toggle-sidebar-btn', 'nClicks'),
    State('sidebar-collapsed-store', 'data'),
    prevent_initial_call=True
)

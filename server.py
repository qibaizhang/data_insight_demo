"""
Dash Application Instance

Initializes the Dash app and exposes the Flask server.
"""
import dash

app = dash.Dash(
    __name__,
    title='DataInsight',
    suppress_callback_exceptions=True,
    assets_folder='assets',
)

# Expose Flask server for deployment
server = app.server


def register_api_blueprints():
    """Register API blueprints with Flask server"""
    from api.chat_api import chat_bp
    server.register_blueprint(chat_bp)


# Register blueprints
register_api_blueprints()

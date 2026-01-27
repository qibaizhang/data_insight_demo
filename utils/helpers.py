"""
Helper Utilities

Common utility functions.
"""
import uuid
from datetime import datetime
from typing import Any


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())


def format_datetime(dt: datetime = None) -> str:
    """Format datetime for display"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def safe_json_serialize(obj: Any) -> Any:
    """Safely serialize object to JSON-compatible format"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)

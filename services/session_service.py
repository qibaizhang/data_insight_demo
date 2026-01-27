"""
Session Service

Manages chat sessions with local persistence.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from config import config
from utils.helpers import generate_session_id, format_datetime


class SessionService:
    """Service for managing chat sessions"""

    def __init__(self):
        self.sessions_dir = config.SESSIONS_DIR
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def _get_session_file(self, session_id: str) -> Path:
        """Get session file path"""
        return self.sessions_dir / f'{session_id}.json'

    def create_session(self, session_id: str = None, title: str = None) -> dict:
        """
        Create a new session

        Args:
            session_id: Optional session ID (generates if not provided)
            title: Optional session title

        Returns:
            Session data dict
        """
        if not session_id:
            session_id = generate_session_id()

        session = {
            'id': session_id,
            'title': title or f'会话 {format_datetime()}',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'messages': [],
            'datasource': 'sqlite',
            'model': config.DEFAULT_MODEL
        }

        self._save_session(session)
        return session

    def get_session(self, session_id: str) -> Optional[dict]:
        """
        Get session by ID

        Args:
            session_id: Session identifier

        Returns:
            Session data or None if not found
        """
        session_file = self._get_session_file(session_id)

        if not session_file.exists():
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None

    def update_session(self, session_id: str, updates: dict) -> Optional[dict]:
        """
        Update session data

        Args:
            session_id: Session identifier
            updates: Dict of fields to update

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)

        if not session:
            return None

        session.update(updates)
        session['updated_at'] = datetime.now().isoformat()

        self._save_session(session)
        return session

    def add_message(self, session_id: str, role: str, content: str, metadata: dict = None) -> Optional[dict]:
        """
        Add a message to session

        Args:
            session_id: Session identifier
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional message metadata

        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)

        if not session:
            # Create new session if not exists
            session = self.create_session(session_id)

        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }

        session['messages'].append(message)
        session['updated_at'] = datetime.now().isoformat()

        # Update title from first user message
        if role == 'user' and len(session['messages']) == 1:
            title = content[:50] + '...' if len(content) > 50 else content
            session['title'] = title

        self._save_session(session)
        return session

    def list_sessions(self, limit: int = 50) -> list[dict]:
        """
        List all sessions sorted by update time

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of session summaries
        """
        sessions = []

        for session_file in self.sessions_dir.glob('*.json'):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session = json.load(f)
                    sessions.append({
                        'id': session['id'],
                        'title': session['title'],
                        'updated_at': session['updated_at'],
                        'message_count': len(session.get('messages', []))
                    })
            except Exception:
                continue

        # Sort by update time descending
        sessions.sort(key=lambda x: x['updated_at'], reverse=True)

        return sessions[:limit]

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session

        Args:
            session_id: Session identifier

        Returns:
            True if deleted, False otherwise
        """
        session_file = self._get_session_file(session_id)

        if session_file.exists():
            try:
                session_file.unlink()
                return True
            except Exception as e:
                print(f"Error deleting session {session_id}: {e}")
                return False

        return False

    def _save_session(self, session: dict):
        """Save session to file"""
        session_file = self._get_session_file(session['id'])

        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, ensure_ascii=False, indent=2)


# Global service instance
session_service = SessionService()

"""
Database Service

Manages SQLite database connection for demo.
"""
from typing import Protocol
from abc import abstractmethod

from config import config


class DatabaseConnection(Protocol):
    """Database connection interface"""

    @abstractmethod
    def execute_query(self, sql: str) -> dict:
        """Execute SQL query and return results"""
        ...

    @abstractmethod
    def get_table_schema(self, table_name: str) -> list[dict]:
        """Get table schema information"""
        ...

    @abstractmethod
    def list_tables(self) -> list[str]:
        """List all tables in the database"""
        ...


class SQLiteConnection:
    """SQLite database connection"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def execute_query(self, sql: str) -> dict:
        import sqlite3

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()

            data = [dict(zip(columns, row)) for row in rows]

            return {'columns': columns, 'data': data}

        finally:
            conn.close()

    def get_table_schema(self, table_name: str) -> list[dict]:
        import sqlite3

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            rows = cursor.fetchall()

            return [
                {
                    'name': row[1],
                    'type': row[2],
                    'nullable': not row[3],
                    'primary_key': bool(row[5])
                }
                for row in rows
            ]

        finally:
            conn.close()

    def list_tables(self) -> list[str]:
        import sqlite3

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            return [row[0] for row in cursor.fetchall()]

        finally:
            conn.close()


# Connection cache
_connections: dict[str, DatabaseConnection] = {}


def get_database_connection(datasource: str) -> DatabaseConnection:
    """
    Get or create a database connection

    Args:
        datasource: Data source type (only 'sqlite' supported in demo)

    Returns:
        Database connection instance
    """
    if datasource in _connections:
        return _connections[datasource]

    if datasource == 'sqlite':
        conn = SQLiteConnection(config.SQLITE_PATH)
    else:
        raise ValueError(f"Unknown datasource: {datasource}. Demo only supports 'sqlite'.")

    _connections[datasource] = conn
    return conn

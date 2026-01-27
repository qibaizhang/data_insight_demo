"""
SQL Validator

Validates SQL queries to ensure read-only operations.
"""
import re
from typing import Tuple


# Dangerous SQL keywords that modify data
DANGEROUS_KEYWORDS = [
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
    'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE',
    'EXEC', 'EXECUTE', 'CALL', 'INTO'
]

# SQL comment patterns
COMMENT_PATTERNS = [
    r'--.*$',           # Single line comment
    r'/\*.*?\*/',       # Multi-line comment
]


def validate_sql_readonly(sql: str) -> Tuple[bool, str]:
    """
    Validate that a SQL query is read-only

    Args:
        sql: SQL query string

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not sql or not sql.strip():
        return False, "SQL 查询不能为空"

    # Normalize SQL
    normalized = sql.strip().upper()

    # Remove comments
    for pattern in COMMENT_PATTERNS:
        normalized = re.sub(pattern, '', normalized, flags=re.MULTILINE | re.DOTALL)

    normalized = normalized.strip()

    # Check if starts with SELECT
    if not normalized.startswith('SELECT'):
        return False, "只允许 SELECT 查询"

    # Check for dangerous keywords
    for keyword in DANGEROUS_KEYWORDS:
        # Use word boundary to avoid false positives
        pattern = rf'\b{keyword}\b'
        if re.search(pattern, normalized):
            return False, f"检测到禁止的关键字: {keyword}"

    # Check for semicolon (potential SQL injection)
    if ';' in normalized and not normalized.endswith(';'):
        # Multiple statements
        return False, "不允许多条 SQL 语句"

    return True, ""


def sanitize_identifier(identifier: str) -> str:
    """
    Sanitize a SQL identifier (table name, column name)

    Args:
        identifier: Raw identifier string

    Returns:
        Sanitized identifier
    """
    # Remove any characters that aren't alphanumeric or underscore
    sanitized = re.sub(r'[^\w]', '', identifier)

    # Ensure it doesn't start with a number
    if sanitized and sanitized[0].isdigit():
        sanitized = '_' + sanitized

    return sanitized

"""
SQL Query Tool

Tool for executing SQL queries against configured data sources.
Enforces read-only mode for safety.
"""
from agno.tools import Toolkit
from typing import Optional
import json

from services.database_service import get_database_connection
from utils.sql_validator import validate_sql_readonly


class SQLQueryToolkit(Toolkit):
    """SQL Query toolkit for data retrieval"""

    def __init__(self, datasource: str = 'sqlite'):
        super().__init__(
            name='SQL查询工具',
            instructions="""
            使用此工具执行 SQL 查询获取数据。
            - 只支持 SELECT 查询（只读模式）
            - 查询前请确认表结构
            - 返回的数据会自动格式化为 JSON
            """
        )
        self.datasource = datasource

        # Register tools
        self.register(self.execute_query)
        self.register(self.get_table_schema)
        self.register(self.list_tables)

    def execute_query(self, sql: str) -> dict:
        """
        执行 SQL 查询并返回结果

        Args:
            sql: SQL 查询语句（仅支持 SELECT）

        Returns:
            查询结果字典，包含 columns 和 data
        """
        # Validate SQL is read-only
        is_valid, error = validate_sql_readonly(sql)
        if not is_valid:
            return {'error': f'SQL 验证失败: {error}'}

        try:
            conn = get_database_connection(self.datasource)
            result = conn.execute_query(sql)

            return {
                'success': True,
                'columns': result.get('columns', []),
                'data': result.get('data', []),
                'row_count': len(result.get('data', []))
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_table_schema(self, table_name: str) -> dict:
        """
        获取指定表的结构信息

        Args:
            table_name: 表名

        Returns:
            表结构信息，包含字段名、类型和注释
        """
        try:
            conn = get_database_connection(self.datasource)
            schema = conn.get_table_schema(table_name)

            return {
                'success': True,
                'table_name': table_name,
                'columns': schema
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def list_tables(self) -> dict:
        """
        列出当前数据源中的所有表

        Returns:
            表名列表
        """
        try:
            conn = get_database_connection(self.datasource)
            tables = conn.list_tables()

            return {
                'success': True,
                'tables': tables,
                'datasource': self.datasource
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

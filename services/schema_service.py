"""
Schema Service

Manages database schema information with auto-discovery and manual configuration.
"""
import yaml
from pathlib import Path
from typing import Optional

from config import config
from services.database_service import get_database_connection


class SchemaService:
    """Service for managing database schema information"""

    def __init__(self):
        self.schema_dir = config.SCHEMA_DIR
        self._cache: dict[str, dict] = {}

    def get_schema(self, datasource: str, table_name: Optional[str] = None) -> dict:
        """
        Get schema information for a datasource or specific table

        Args:
            datasource: Data source type
            table_name: Optional table name

        Returns:
            Schema information dict
        """
        # Try to load from config file first
        config_schema = self._load_config_schema(datasource)

        # Auto-discover from database
        db_schema = self._discover_schema(datasource)

        # Merge: config overrides auto-discovered
        merged = self._merge_schemas(db_schema, config_schema)

        if table_name:
            return merged.get('tables', {}).get(table_name, {})

        return merged

    def _load_config_schema(self, datasource: str) -> dict:
        """Load schema from YAML config file"""
        config_file = self.schema_dir / f'{datasource}.yaml'

        if not config_file.exists():
            return {}

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading schema config: {e}")
            return {}

    def _discover_schema(self, datasource: str) -> dict:
        """Auto-discover schema from database"""
        cache_key = f'discover:{datasource}'

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            conn = get_database_connection(datasource)
            tables = conn.list_tables()

            schema = {'tables': {}}

            for table in tables:
                try:
                    columns = conn.get_table_schema(table)
                    schema['tables'][table] = {
                        'columns': columns,
                        'description': ''  # No description from auto-discovery
                    }
                except Exception:
                    pass

            self._cache[cache_key] = schema
            return schema

        except Exception as e:
            print(f"Error discovering schema: {e}")
            return {'tables': {}}

    def _merge_schemas(self, base: dict, override: dict) -> dict:
        """Merge two schema dicts, override takes precedence"""
        result = base.copy()

        for table_name, table_info in override.get('tables', {}).items():
            if table_name not in result.get('tables', {}):
                result.setdefault('tables', {})[table_name] = table_info
            else:
                # Merge table info
                result['tables'][table_name].update(table_info)

        return result

    def get_schema_prompt(self, datasource: str) -> str:
        """
        Generate a schema description prompt for the LLM

        Args:
            datasource: Data source type

        Returns:
            Formatted schema description
        """
        schema = self.get_schema(datasource)

        lines = [f"## 数据源: {datasource}", ""]

        for table_name, table_info in schema.get('tables', {}).items():
            description = table_info.get('description', '')
            lines.append(f"### 表: {table_name}")

            if description:
                lines.append(f"描述: {description}")

            lines.append("字段:")

            for col in table_info.get('columns', []):
                col_name = col.get('name', '')
                col_type = col.get('type', '')
                col_desc = col.get('description', '')

                line = f"  - {col_name} ({col_type})"
                if col_desc:
                    line += f" - {col_desc}"

                lines.append(line)

            lines.append("")

        return '\n'.join(lines)


# Global service instance
schema_service = SchemaService()

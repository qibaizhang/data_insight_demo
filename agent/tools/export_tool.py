"""
Export Tool

Tool for preparing data export in various formats.
"""
from agno.tools import Toolkit
from typing import Optional, Literal
import json


class ExportToolkit(Toolkit):
    """Export toolkit for data and reports"""

    def __init__(self):
        super().__init__(
            name='导出工具',
            instructions="""
            使用此工具准备数据或报告的导出。
            - 支持 CSV 格式数据导出
            - 支持 Markdown 格式报告导出
            - 返回的数据会被前端处理并触发下载
            """
        )

        self.register(self.prepare_csv_export)
        self.register(self.prepare_report_export)

    def prepare_csv_export(
        self,
        data: list[dict],
        filename: Optional[str] = None
    ) -> dict:
        """
        准备 CSV 格式数据导出

        Args:
            data: 要导出的数据列表
            filename: 文件名（可选）

        Returns:
            导出配置
        """
        if not data:
            return {
                'success': False,
                'error': '无数据可导出'
            }

        filename = filename or 'data_export.csv'

        return {
            'success': True,
            'type': 'csv',
            'data': data,
            'filename': filename,
            'row_count': len(data)
        }

    def prepare_report_export(
        self,
        content: str,
        title: Optional[str] = None,
        filename: Optional[str] = None
    ) -> dict:
        """
        准备报告导出

        Args:
            content: 报告内容（Markdown 格式）
            title: 报告标题
            filename: 文件名

        Returns:
            导出配置
        """
        if not content:
            return {
                'success': False,
                'error': '无报告内容可导出'
            }

        filename = filename or 'analysis_report.md'

        return {
            'success': True,
            'type': 'markdown',
            'content': content,
            'title': title,
            'filename': filename
        }

"""
Report Tool

Tool for generating analysis reports using Markdown and Infographic syntax.
"""
import json
from agno.tools import Toolkit
from typing import Optional
from feffery_infographic.prompts import base_prompt as FI_PROMPT


class ReportToolkit(Toolkit):
    """Report generation toolkit"""

    def __init__(self):
        super().__init__(
            name='报告生成工具',
            instructions="""
            ## 报告生成工具 - 必须使用！

            **⚠️ 重要规则：当用户提到以下任何关键词时，必须调用此工具！**

            触发关键词：
            - "报告"、"分析报告"、"洞察报告"、"概览报告"、"业务报告"
            - "生成报告"、"做个报告"、"出个报告"、"写个报告"
            - "数据洞察"、"业务概览"、"数据概览"、"数据总结"
            - "总结"、"汇总分析"、"分析总结"

            **工具选择：**
            - `create_report`: 生成 Markdown 格式报告（默认选择）
            - `create_infographic`: 生成信息图报告（用户明确要求"信息图"时使用）

            **正确用法：**
            ```
            # 用户说"生成报告" → 必须调用 create_report
            create_report(content="# 报告标题\\n\\n## 概要\\n内容...")
            ```

            **错误做法（严禁）：**
            - 用户说"报告"但你只在聊天中输出，没有调用工具
            - 在聊天中直接写报告内容而不调用此工具

            报告会自动显示在右侧「报告」面板中。
            """
        )

        self.register(self.create_report)
        self.register(self.create_infographic)

    def create_report(
        self,
        content: str,
        report_format: str = 'markdown'
    ) -> dict:
        """
        创建 Markdown 格式的分析报告 - 用户说"报告"时必须调用此方法！

        ⚠️ 重要：当用户请求生成报告、分析报告、数据洞察、业务概览等时，
        必须调用此方法，不能只在聊天中输出报告内容！

        Args:
            content: 报告内容（Markdown 格式），包含标题、概要、分析、建议等
            report_format: 报告格式，默认 'markdown'

        Returns:
            包含报告内容的字典，报告会自动显示在右侧「报告」面板

        示例：
            create_report(content='''# 销售分析报告

## 概要
本月销售表现良好，总销售额达到 50,000 元。

## 关键指标
- 总订单数：100 笔
- 平均客单价：500 元
- 活跃客户：25 人

## 分析与建议
1. 销售额环比增长 15%
2. 建议关注高价值客户群体
''')
        """
        return {
            'success': True,
            'content': content,
            'format': report_format
        }

    def create_infographic(
        self,
        syntax: str
    ) -> dict:
        """
        创建信息图报告（简化接口）

        直接传入完整的 infographic 语法字符串即可。

        Args:
            syntax: 完整的 infographic 语法，必须以 'infographic' 开头

        Returns:
            包含信息图内容的字典，会自动显示在右侧报告面板

        示例语法：
        infographic list-grid-badge-card
        data
          title 销售概览
          lists
            - label 总订单
              value 100
            - label 总收入
              value ¥50,000
        """
        # Ensure syntax starts with 'infographic'
        if not syntax.strip().startswith('infographic'):
            syntax = f'infographic list-grid-badge-card\ndata\n  title 数据概览\n  lists\n{syntax}'

        return {
            'success': True,
            'content': syntax,
            'format': 'infographic'
        }

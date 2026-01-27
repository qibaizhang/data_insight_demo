"""
Chart Tool

Tool for generating chart configurations based on data.
"""
from agno.tools import Toolkit
from typing import Optional, Union, Any
import json
import ast


def _parse_param(value, expected_type='str'):
    """
    Parse parameter that might be passed as JSON string by LLM.

    Args:
        value: The parameter value (might be string or native type)
        expected_type: 'str', 'list', or 'dict'

    Returns:
        Parsed value in the expected type
    """
    if value is None:
        return None

    # If already the expected type, return as-is
    if expected_type == 'list' and isinstance(value, list):
        return value
    if expected_type == 'dict' and isinstance(value, dict):
        return value
    if expected_type == 'str' and isinstance(value, str):
        # Check if it's a JSON object string like '{"type": "line"}'
        if value.startswith('{') and value.endswith('}'):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict) and 'type' in parsed:
                    return parsed['type']
            except json.JSONDecodeError:
                pass
        return value

    # Try to parse string as JSON/Python literal
    if isinstance(value, str):
        # Try JSON first
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

        # Try ast.literal_eval
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass

    return value


class ChartToolkit(Toolkit):
    """Chart generation toolkit"""

    def __init__(self):
        super().__init__(
            name='图表生成工具',
            instructions="""
            使用此工具生成数据可视化图表配置。
            - 支持折线图、柱状图、饼图、面积图
            - 自动根据数据特征推荐图表类型
            - 返回的配置可直接用于 feffery-antd-charts 组件
            - chart_type 参数只接受: line, bar, pie, area
            - data 参数必须是数据列表
            """
        )

        self.register(self.generate_chart_config)
        self.register(self.recommend_chart_type)

    def generate_chart_config(
        self,
        chart_type: str,
        data: Any = None,
        x_field: str = '',
        y_field: str = '',
        series_field: Optional[str] = None,
        title: Optional[str] = None
    ) -> dict:
        """
        生成图表配置

        Args:
            chart_type: 图表类型 (line, bar, pie, area)
            data: 数据列表，必须提供！格式为 [{"x字段": 值, "y字段": 值}, ...]
            x_field: X 轴字段名
            y_field: Y 轴字段名
            series_field: 系列字段名（可选，用于多系列图表）
            title: 图表标题

        Returns:
            图表配置字典
        """
        # Parse parameters that might be passed as JSON strings by LLM
        chart_type = _parse_param(chart_type, 'str')
        data = _parse_param(data, 'list')

        # Validate chart_type
        valid_types = ['line', 'bar', 'pie', 'area']
        if chart_type not in valid_types:
            return {
                'success': False,
                'error': f'Invalid chart_type: {chart_type}. Must be one of: {valid_types}'
            }

        # Validate data - this is required!
        if data is None or not isinstance(data, list) or len(data) == 0:
            return {
                'success': False,
                'error': '数据参数 data 是必需的！请提供数据列表，格式为 [{"字段1": 值1, "字段2": 值2}, ...]。请先使用 execute_query 工具查询数据，然后将查询结果的 data 字段传递给此工具。'
            }

        # Validate x_field and y_field
        if not x_field or not y_field:
            return {
                'success': False,
                'error': 'x_field 和 y_field 参数是必需的！请指定 X 轴和 Y 轴对应的字段名。'
            }

        base_config = {
            'type': chart_type,
            'data': data,
            'options': {
                'xField': x_field,
                'yField': y_field,
            }
        }

        if series_field:
            base_config['options']['seriesField'] = series_field
            base_config['options']['color'] = [
                '#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1'
            ]

        # Chart-specific options
        if chart_type == 'line':
            base_config['options'].update({
                'smooth': True,
            })

        elif chart_type == 'bar':
            base_config['options'].update({
                'columnWidthRatio': 0.6,
            })

        elif chart_type == 'pie':
            # 饼图使用 angleField 和 colorField，不需要 xField/yField
            base_config['options'] = {
                'angleField': y_field,
                'colorField': x_field,
                'radius': 0.9,
                'innerRadius': 0.6,
            }
            # 注意：data 已经在 base_config['data'] 中，不要重复添加到 options

        elif chart_type == 'area':
            base_config['options'].update({
                'smooth': True,
                'areaStyle': {'fillOpacity': 0.6},
            })

        return {
            'success': True,
            'config': base_config,
            'message': f'已生成 {chart_type} 图表配置'
        }

    def recommend_chart_type(
        self,
        data_description: str,
        analysis_goal: str
    ) -> dict:
        """
        根据数据特征推荐图表类型

        Args:
            data_description: 数据描述
            analysis_goal: 分析目标

        Returns:
            推荐的图表类型和原因
        """
        recommendations = []

        # Time series data
        if any(kw in data_description.lower() for kw in ['时间', '日期', '趋势', 'date', 'time']):
            recommendations.append({
                'type': 'line',
                'reason': '时间序列数据适合使用折线图展示趋势变化'
            })
            recommendations.append({
                'type': 'area',
                'reason': '面积图可以更好地展示累积效果'
            })

        # Comparison data
        if any(kw in analysis_goal.lower() for kw in ['对比', '比较', 'compare']):
            recommendations.append({
                'type': 'bar',
                'reason': '柱状图适合进行分类数据的对比'
            })

        # Proportion data
        if any(kw in analysis_goal.lower() for kw in ['占比', '比例', '构成', 'proportion']):
            recommendations.append({
                'type': 'pie',
                'reason': '饼图适合展示数据的占比构成'
            })

        # Default
        if not recommendations:
            recommendations.append({
                'type': 'bar',
                'reason': '柱状图是最通用的图表类型'
            })

        return {
            'success': True,
            'recommendations': recommendations,
            'primary': recommendations[0]['type']
        }

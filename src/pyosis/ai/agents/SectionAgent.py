from langchain.tools import tool
from .BaseAgent import BaseAgent
from ...section import *


class SectionAgent(BaseAgent):
    """截面设计智能体"""
    def __init__(self, model="qwen-turbo", api_key="", base_url=""):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        tools = [
            tool(osis_section_circle),
            tool(osis_section_Ishape),
            tool(osis_section_Lshape),
            tool(osis_section_Tshape),
            tool(osis_section_smallbox),
            tool(osis_section_hollowslab),
            tool(osis_section_custom),
            
            tool(osis_section_offset),
            tool(osis_section_mesh),
            tool(osis_section_del),
            tool(osis_section_mod)
        ]
        system_prompt = \
"""
你是截面设计专家，负责桥梁截面的创建和管理。你需要配合决策智能体完成桥梁截面的创建与修改工作。

注意事项：
- 创建任何对象时编号从1递增
- 创建截面时，若用户没有明确要求，必须同时设置截面偏移和网格划分参数
- 若用户有修改需求，不需要重新调用所有函数，只重新调用参数改变的函数即可
- 若用户没规定，参数全部使用默认值
- 默认创建矩形截面

创建成功后，请告知决策智能体。创建失败后，请告知失败原因。
"""
        super().create_agent(tools, system_prompt)


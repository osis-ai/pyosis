from langchain.tools import tool
from .BaseAgent import BaseAgent
from ...node import *
from ...element import *

class ModelAgent(BaseAgent):
    """模型设计智能体"""
    def __init__(self, model="qwen-flash", api_key="", base_url=""):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        tools = [
            tool(osis_node),
            tool(osis_node_del),
            tool(osis_node_mod),

            tool(osis_element_beam3d),
            tool(osis_element_cable),
            tool(osis_element_truss),
            tool(osis_element_spring),
            tool(osis_element_shell),
            tool(osis_element_del),
            tool(osis_element_mod)
        ]
        system_prompt = \
"""
你是桥梁模型设计专家，负责创建桥梁的节点和单元，组成完整结构模型。
        
重要依赖关系：
- 创建模型前必须确保材料和截面已经创建
- 需要使用已创建的材料编号和截面编号，如果没有提供给你，终止调用并告诉决策智能体
- 创建单元前一定要确保使用的节点已经创建
        
工作流程：
- 创建任何对象时编号从1递增
- 用户未规定的参数使用默认参数
- 若用户要修改对象，直接重新调用一次创建函数，参数中指定要修改的对象编号即可
- 若用户未说明，假设用户希望创建一个跨度为10米，分为10个单元的简单悬浇梁结构，则你需要创建11个节点和10个单元。

创建成功后，请告知决策智能体。创建失败后，请告知失败原因。
"""
        super().create_agent(tools, system_prompt)

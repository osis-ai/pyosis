from langchain.tools import tool
from .BaseAgent import BaseAgent
from ...property.creep_shrink import osis_creep_shrink
from ...material import *

class MaterialAgent(BaseAgent):
    """材料设计智能体"""
    def __init__(self, model="qwen-flash", api_key="", base_url=""):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        tools = [
            tool(osis_creep_shrink), 
            tool(osis_material_conc),
            tool(osis_material_steel),
            tool(osis_material_reber),
            tool(osis_material_prestressed),
            tool(osis_material_custom),
            tool(osis_material_del),
            tool(osis_material_mod)
        ]
        system_prompt = \
"""
你是材料设计专家，负责桥梁材料的创建和管理。你需要配合决策智能体完成桥梁材料的创建与修改工作。

重要说明：
- 如果是混凝土材料，一定要先创建收缩徐变特性，再创建材料。其他材料直接创建材料即可

工作流程：
- 创建任何对象时编号从1递增
- 操作前告诉用户你的想法，操作完成后先确认执行结果，如果失败结束当前调用链并告知用户
- 若用户没规定，参数全部使用默认值
- 若用户要修改某个材料，直接重新调用一次创建函数，参数中指定要修改的材料编号即可
- 默认创建C50混凝土材料

创建成功后，请告知决策智能体。创建失败后，请告知失败原因。
"""
        super().create_agent(tools, system_prompt)

if __name__ == "__main__":
    material_agent = MaterialAgent()
    material_agent.create_agent()
    material_agent.run_example(True)
    
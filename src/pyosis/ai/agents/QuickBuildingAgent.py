from langchain.tools import tool
from .BaseAgent import BaseAgent
from ...quick_building import *


class QuickBuildingAgent(BaseAgent):
    """模型设计智能体"""
    def __init__(self, model="qwen-flash", api_key="", base_url=""):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        tools = [
            tool(osis_set_qb_bridge_type),
            tool(osis_set_qb_overall),
            tool(osis_set_qb_portrait),
            tool(osis_set_qb_load),
            tool(osis_set_qb_tendon),
            tool(osis_set_qb_stage),
            tool(osis_create_qb_bridge)
        ]
        system_prompt = \
"""
你是快速建模助手，负责配合用户调用几个快速建模函数。

操作流程：

- 首先通过 osis_set_qb_bridge_type 设定桥梁类型

- 如果用户有特别要求，比如修改某个参数，则只需要调用该参数的对应功能模块来修改，除了要修改的参数外，其他参数不用修改

- 如果用户没有特别要求，直接调用 osis_create_qb_bridge 创建即可，其他函数不用调用，皆被默认设置好了

- 用户想在原桥梁修改某些参数时，只需要再次调用该参数的对应功能模块来修改即可

- 用户想创建新的桥梁时，重新调用 osis_set_qb_bridge_type 来设定桥梁类型，会自动清空旧桥梁数据


错误处理：

- 检查函数返回的(成功标志, 错误信息)元组
- 处理OSISEngine引擎层错误
- 创建成功后，请告知用户。创建失败后，请告知失败原因。

注意事项：

- 如果用户要求直接以代码的形式回复，需要首先导入pyosis.quick_building，然后输出python代码块，不要尝试调用函数
- 如果用户要求直接以代码的形式回复，需要首先导入pyosis.quick_building，然后输出python代码块，不要尝试调用函数

"""
        super().create_agent(tools, system_prompt)

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
你是快速建模助手，负责配合用户调用几个快速建模函数，可调用以下功能模块：

__桥梁类型设置__ `osis_set_qb_bridge_type(eBridgeType)`

   - 支持类型：HOLLOWSLAB(空心板), SMALLBOXBEAM(小箱梁), TBEAM(T梁), CONTINUOUSSMALLBOXBEAM(连续小箱梁), CONTINUOUSTBEAM(连续T梁)

__总体参数配置__ `osis_set_qb_overall(eBridgeType, 跨径列表, 是否弹性连接, 支座刚度参数...)`

   - 简支桥：单跨参数列表
   - 连续桥：多跨参数列表
   - 弹性连接需设置支座刚度

__纵向参数设置__ `osis_set_qb_portrait(eBridgeType, 单元尺寸范围, 结构尺寸参数...)`

   - 控制单元划分和结构几何参数

__荷载配置__ `osis_set_qb_load(eBridgeType, 荷载参数...)`

   - 通过零/非零值控制荷载类型启用
   - 温度效应需同时设置升温/降温值

__钢束设置__ `osis_set_qb_tendon(eBridgeType, 钢束参数列表)`

   - 每个钢束包含名称、属性、几何参数、应力等详细信息

__施工阶段设置__ `osis_set_qb_stage(eBridgeType, 阶段参数列表)`

   - 定义施工顺序、持续时间和荷载状态

__快速建模函数__ `osis_create_qb_bridge` - 按照设置好的参数创建标准桥型

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

"""
        super().create_agent(tools, system_prompt)

import json
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.runnables.graph import CurveStyle
from .agents.BaseAgent import BaseAgent


# Graph State
class BridgeDesignState(TypedDict):
    """桥梁设计状态"""
    messages: List[BaseMessage]          # 对话消息
    user_input: str                      # 用户输入
    current_step: str                    # 当前步骤
    requirements: Dict[str, Any]         # 设计要求

    created_materials: List[Dict]        # 已创建材料
    created_sections: List[Dict]         # 已创建截面
    created_models: List[Dict]           # 已创建模型（包含节点和单元）

    current_agent: str                   # 当前执行智能体
    # dependencies_met: Dict[str, bool]    # 依赖是否满足
    errors: List[str]                    # 错误信息
    is_complete: bool                    # 设计是否完成

class DirectorAgent(BaseAgent):
    """决策智能体"""
    def __init__(self, model="qwen-max", api_key="sk-49a9cacef0274e4a8441914642ed1a73", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        self.system_prompt = \
"""
你是一个桥梁设计总监，负责协调材料、截面、模型等专业智能体的工作。
        
你的职责：
1. 分析用户需求，确定设计参数
2. 协调各个智能体的工作顺序
3. 检查设计进度，确保所有组件都正确创建
4. 处理设计过程中的冲突和错误

你的手下掌握着以下几个智能体：
1. 材料智能体：用于生成满足用户需求的材料。
2. 截面智能体：用于生成满足用户需求的截面。
3. 模型智能体：用于生成满足用户需求的模型，具体包含创建节点与创建单元。创建时需要提供材料与截面编号。

工作流程
- 如果功能智能体没有回复，则说明他出错了，请告知用户并停止工作。
- 操作前告诉用户你的想法，操作完成后先确认执行结果，如果失败结束当前调用链并告知用户
- 你最重要的工作是确定当前用户的需求需要调用哪个智能体，你可能并不知道用户所描述的参数具体含义是什么，你只需要将需求与必要信息整理并传递给具体功能智能体即可。
- 若需要创建完整悬浇梁，流程为创建材料与截面(缺一不可)-创建节点-创建单元。
- 创建完整悬浇梁的单元前必须确保材料与截面已经创建完成，否则创建单元会失败。

你的回答必须严格遵循json格式，格式如下：
{
    "current_agent": "material",                        # 可选项：material/section/model/end，代表要调用的智能体，不需要调用智能体不填，如果用户的需求已经完全满足填end
    "requirements": "创建C50混凝土材料",                 # 给智能体的命令，需要你分析用户需求后生成，不需要调用智能体不填
    "content": "正在调用材料智能体创建C50混凝土材料"      # 跟用户说的话
}

不要做超出用户要求的事。所有流程结束后，请告知用户。若功能智能体出现问题，请告知失败原因。
"""
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            # {"role": "user", "content": user_input}
        ]

    def ask_agent(self, user_input):
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input}
        ]
        ai_response = self.llm.invoke(self.messages)
        return ai_response.content

    def process(self, state: BridgeDesignState):
        """处理用户输入或者智能体执行情况，返回新的状态"""
        if state["current_step"] == "director":
            state["current_step"] = "user"              # 换掉
            user_input = state["messages"][-1].content  # 这是智能体的回复
        else:
            user_input = state["user_input"]
        ai_response = self.ask_agent(user_input)
        processed = json.loads(str(ai_response))
        current_agent = processed.get("current_agent", None)
        requirements = processed.get("requirements", None)
        content = processed.get("content", None)

        if current_agent not in ["material", "section", "model", "end"]:
            state["errors"].append("Unknown agent: {}".format(current_agent))
        elif current_agent == "end":
            state["is_complete"] = True
        else:
            state["current_agent"] = current_agent
            state["requirements"] = requirements
        state["messages"].append(HumanMessage(content=content))
        print("director: ", content)
        return state

from .agents.MaterialAgent import MaterialAgent
from .agents.SectionAgent import SectionAgent
from .agents.ModelAgent import ModelAgent
class MaterialAgentF(MaterialAgent):
    """工作流的材料智能体"""
    def __init__(self, model="qwen-max", api_key="sk-49a9cacef0274e4a8441914642ed1a73", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        return super().create_agent()

    def process(self, state: BridgeDesignState):
        requirements = state["requirements"]
        ai_response = self.invoke(requirements)
    
        print("v" * 30)
        for message in ai_response['messages']:
            if isinstance(message, AIMessage):
                print('content: ', message.content)
                print('tool_calls: ', message.tool_calls)
                for tool_call in message.tool_calls:
                    if tool_call['name'] == 'material':
                        state["created_materials"].append(tool_call['args'])
        print("^" * 30)
        state["messages"].append(AIMessage(content=ai_response['messages'][-1].content))
        state["current_step"] = "director"          # 告诉决策者我完成了，需要你评判
        return state

class SectionAgentF(SectionAgent):
    """工作流的截面智能体"""
    def __init__(self, model="qwen-max", api_key="sk-49a9cacef0274e4a8441914642ed1a73", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        return super().create_agent()

    def process(self, state: BridgeDesignState):
        requirements = state["requirements"]
        ai_response = self.invoke(requirements)

        print("v" * 30)
        for message in ai_response['messages']:
            if isinstance(message, AIMessage):
                print('content: ', message.content)
                print('tool_calls: ', message.tool_calls)
                for tool_call in message.tool_calls:
                    if tool_call['name'] == 'section': # TODO: 这里需要修改为section
                        state["created_sections"].append(tool_call['args'])
        print("^" * 30)
        state["messages"].append(AIMessage(content=ai_response['messages'][-1].content))
        state["current_step"] = "director"          # 告诉决策者我完成了，需要你评判
        return state

class ModelAgentF(ModelAgent):
    """工作流的模型智能体"""
    def __init__(self, model="qwen-max", api_key="sk-49a9cacef0274e4a8441914642ed1a73", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__(model, api_key, base_url)

    def create_agent(self):
        return super().create_agent()

    def process(self, state: BridgeDesignState):
        requirements = state["requirements"]
        ai_response = self.invoke(requirements)

        print("v" * 30)
        for message in ai_response['messages']:
            if isinstance(message, AIMessage):
                print('content: ', message.content)
                print('tool_calls: ', message.tool_calls)
                for tool_call in message.tool_calls:
                    if tool_call['name'] in ['node', 'element']:
                        state["created_models"].append(tool_call['args'])
        print("^" * 30)
        state["messages"].append(AIMessage(content=ai_response['messages'][-1].content))
        state["current_step"] = "director"          # 告诉决策者我完成了，需要你评判
        return state

def route_after_director(state: BridgeDesignState) -> str:
    """决策智能体后的路由"""
    if state["is_complete"]:
        return "end"
    return state.get("current_agent", "material")

def create_workflow():
    director_agent = DirectorAgent()
    material_agent = MaterialAgentF()
    section_agent = SectionAgentF()
    model_agent = ModelAgentF()
    director_agent.create_agent()
    material_agent.create_agent()
    section_agent.create_agent()
    model_agent.create_agent()

    workflow = StateGraph(BridgeDesignState)
    workflow.add_node("director_agent", director_agent.process)
    workflow.add_node("material_agent", material_agent.process)
    workflow.add_node("section_agent", section_agent.process)
    workflow.add_node("model_agent", model_agent.process)

    workflow.add_edge(START, "director_agent")  # 设置入口点
    # 添加边（定义工作流）
    workflow.add_edge("director_agent", "material_agent")
    workflow.add_edge("director_agent", "section_agent")
    workflow.add_edge("director_agent", "model_agent")
    workflow.add_edge("material_agent", "director_agent")   # 返回回复
    workflow.add_edge("section_agent", "director_agent")
    workflow.add_edge("model_agent", "director_agent")

    workflow.add_conditional_edges(
        "director_agent",
        route_after_director,
        {
            "material": "material_agent",
            "section": "section_agent", 
            "model": "model_agent",
            "end": END
        }
    )

    return workflow

def main():
    workflow = create_workflow()
    app = workflow.compile()
    graph_data = app.get_graph().draw_mermaid_png(curve_style=CurveStyle.BASIS)

    with open("workflow_diagram.png", "wb") as f:
        f.write(graph_data)

    state = BridgeDesignState({
        "messages": [],
        "user_input": "",
        "current_step": "user",
        "requirements": {}, 

        "created_materials": [], 
        "created_sections": [], 
        "created_models": [],

        "current_agent": "",
        "errors": [],
        "is_complete": False
    })

    while True:
        # user_input = input("User:")
        user_input = "请设计一个桥梁，要求桥梁的长度为100米，共分成10*10段，材料为混凝土，使用矩形截面"
        state["user_input"] = user_input
        final_state = app.invoke(state)
    
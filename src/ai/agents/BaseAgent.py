from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import pydantic
from typing import Literal

class BaseAgent:
    """Agent base class"""
    
    def __init__(self, model="qwen-flash", api_key="", base_url=""):
        """Initialize the agent"""
        if model == "" or api_key == "" or base_url == "":
            raise ValueError("API key and Base URL must be provided for Agent.")
        self.llm = ChatOpenAI(
            model=model,
            api_key=pydantic.SecretStr(api_key),
            base_url=base_url)

    def create_agent(self, tools, system_prompt):
        self.system_prompt = system_prompt
        self.checkpointer = InMemorySaver()          # 记忆管理
        self.agent = create_agent(model=self.llm, 
                            tools=tools, 
                            system_prompt=self.system_prompt, 
                            checkpointer=self.checkpointer)

    def invoke(self, user_input, thread_id="1"):
        """向智能体提问"""
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}, 
            {"configurable": {"thread_id": thread_id}}
        )
        return result
    def stream(self, user_input, thread_id="1", stream_mode: Literal["values", "updates", "checkpoints", "tasks"] = "updates"):
        """流式输出智能体回复"""
        return self.agent.stream(
            {"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": thread_id}},
             stream_mode=stream_mode)
    
    def ask_agent(self, user_input, thread_id="1"):
        """向智能体提问，回答仅文本"""
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}, 
            {"configurable": {"thread_id": thread_id}}
        )
        return result['messages'][-1].content
    
    def ask_agent_stream(self, user_input, thread_id="1", stream_mode: Literal["values", "updates", "checkpoints", "tasks"] = "updates"):
        """流式输出智能体回复，回答仅文本"""
        for chunk in self.agent.stream(
            {"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": thread_id}}, 
            stream_mode=stream_mode):
            # 提取消息内容
            for step, data in chunk.items():
                if step == "tools":     # 工具调用结果不需要显示
                    continue
                ai_response = data['messages'][-1].content
                yield ai_response
    
    def run_example(self, stream=True):
        """运行智能体"""
        while True:
            user_input = input("User: ")
            if user_input == "exit" or user_input == "quit":
                break
            if stream:
                print("Agent: ", end="")
                for chunk in self.stream(user_input):
                    # 提取消息内容
                    for step, data in chunk.items():
                        if 'messages' in data and len(data['messages']) > 0:
                            ai_response = f"\nstep: {step}\ncontent: {data['messages'][-1].content_blocks}"     # 调试信息
                            print(ai_response)
                            if step == "tools":     # 工具调用结果不需要显示
                                continue
                            ai_response = data['messages'][-1].content                                          # 一般回复
                
            else:
                print("Agent: ", self.ask_agent(user_input))

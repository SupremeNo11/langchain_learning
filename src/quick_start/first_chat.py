from langchain_openai import ChatOpenAI
import os
from langchain.messages import SystemMessage, HumanMessage

model = ChatOpenAI(
    model = "deepseek-v4.1-flash",
    api_key = os.getenv("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/coding/v3",
    temperature = 0,
)

def chat_with_llm(prompt: str) -> str:
    """与 LLM 对话。"""
    answer = model.invoke(prompt)
    return answer.content

# Langchain的核心组件
# 1. 消息与对话模型
def message_and_chat():
    """消息与对话模型。"""

    messages = [
        SystemMessage(content="你是一位资深python工程师，回答要简洁、准确。"),
        HumanMessage(content="该如何学习LangChain?")
    ]
    answer = model.invoke(messages)
    return answer.content

# 2. Prompt 模板
def prompt_template():
    """Prompt 模板。"""
    from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

    # 字符串模板
    prompt = PromptTemplate.from_template(
        "用一句话像{audience}回答{question}."
    )
    print(prompt.format(audience="python工程师", question="该如何学习LangChain?"))

    # 聊天模板
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system","你是{role},回答不超过{maxwords}字。"),
            ("human","{question}"),
        ]
    )
    print(chat_template.format(role="技术教练",maxwords=50,question="如何开始学习LangChain?"))

# 3. 结构化输出
def structure_output():
    """让大模型结构性输出内容"""

    from typing import Literal
    from pydantic import BaseModel, Field
    
    class Joke(BaseModel):
        setup:str = Field(description="笑点铺垫")
        punchline:str = Field(description="包袱")
        style: Literal["冷幽默","谐音梗","反转"]

    structed = model.with_structured_output(Joke)

    joke = structed.invoke("讲一个程序员的笑话")
    print(joke.setup)
    print(joke.punchline)
    print(joke.style)

# 4. 给模型tools
def llm_use_tools():
    """让大模型自己选择我们自己定义的工具

    docstring非常重要，直接决定模型调用哪个工具和参数传入的准确性
    """
    from langchain.tools import tool

    @tool
    def get_weather(city:str) -> str:
        """查询指定城市的天气。
        Args:
            city:城市名，如"深圳"。
        """
        return f"{city} 今天多云，26℃，东北风 3 级"

    model_with_tools = model.bind_tools([get_weather])

    resp = model_with_tools.invoke("信阳今天天气怎么样？")
    # 查看模型调用工具结果
    print(resp.tool_calls)   # 这里只是模型决定调用哪个tool以及需要传入的参数，并未真正执行
    # 输出结果
    # [{'name': 'get_weather', 'args': {'city': '信阳'}, 'id': 'call_00_yzqgufd7tl7qdnrw958gbpmb', 'type': 'tool_call'}]
    
    # 根据模型的工具调用结果，使用相应的工具和参数
    # 执行tools
    # 工具调用结果和上面的prompt拼接在一起，然后再上传给LLM处理



if __name__ == "__main__":
    # # 简单对话
    # print(chat_with_llm("你好"))
    # # 消息和对话
    # print(message_and_chat())
    # # 提示词模板
    # prompt_template()
    # 结构化输出
    # structure_output()

    # LLN使用tool
    llm_use_tools()


    



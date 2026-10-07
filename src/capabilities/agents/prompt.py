"""Agent 系统提示词 —— 阶段2 任务 2.4

职责：定义 Agent 的系统提示词（含消息占位符）。
学习目标：掌握 MessagesPlaceholder 与 bind_tools 的配合。
对应文档：docs/02-phase2-langgraph.md

关键区别:
    {question}  这类占位符吃"字符串"
    MessagesPlaceholder 吃"一整条消息历史(list)"
    —— 每次循环 agent 节点都把完整历史(含工具消息)填进来，模型才能看到上一轮工具结果
"""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_AGENT_TEMPLATE = """你是一个严谨的助手，可以使用提供的工具完成任务。

规则:
1. 需要计算时必须调用工具，禁止心算。
2. 拿到工具结果后，用中文向用户总结最终答案。
"""

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_AGENT_TEMPLATE),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

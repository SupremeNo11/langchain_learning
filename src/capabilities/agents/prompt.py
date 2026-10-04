"""Agent 系统提示词 —— 阶段2 任务 2.4

职责：定义 Agent 的系统提示词（含消息占位符）。
学习目标：掌握 MessagesPlaceholder 与 bind_tools 的配合。
对应文档：docs/02-phase2-langgraph.md
"""
# TODO(阶段2): 创建 agent_prompt（ChatPromptTemplate.from_messages）
#   结构: [("system", SYSTEM_AGENT_TEMPLATE), MessagesPlaceholder(variable_name="messages")]
agent_prompt = None

"""Prompt 模板 —— 阶段1 任务 1.2

职责：集中管理常用 Prompt 模板，避免散落在业务代码里。
学习目标：掌握 ChatPromptTemplate / from_template / from_messages。
对应文档：docs/01-phase1-langchain-core.md

验收: 实现后 tests/unit/test_prompts.py 应通过。
"""
from langchain_core.prompts import ChatPromptTemplate

# RAG 问答模板: 要求模型只基于检索资料回答
# 占位变量: {context} 和 {question}
RAG_QA_TEMPLATE = """你是一个严谨的问答助手。请仅基于以下检索到的资料回答问题。

【检索资料】
{context}

【问题】
{question}

要求：
1. 只使用资料中的信息，不要编造。
2. 如果资料不足以回答，请明确说明"资料中没有相关信息"。
3. 使用中文回答。
"""

# TODO(阶段1): 用 ChatPromptTemplate.from_template(RAG_QA_TEMPLATE) 创建 rag_qa_prompt
rag_qa_prompt = ChatPromptTemplate.from_template(RAG_QA_TEMPLATE)

# 普通对话模板: system + human 消息
# TODO(阶段1): 用 ChatPromptTemplate.from_messages 创建 chat_prompt
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，请用正文简洁回答。"),
        ("human", "{question}")
    ]
)

if __name__ == "__main__":
    print(rag_qa_prompt.format(context="检索资料", question="How are you?"))
    print(" ")
    print(chat_prompt.format(role="专业的老师", question="How are you?"))


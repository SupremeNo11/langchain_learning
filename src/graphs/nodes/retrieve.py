"""检索节点 —— 阶段2 任务 2.2

职责：Graph 中的一个节点，输入 question 输出检索到的上下文。
学习目标：掌握节点函数签名（接收 state 返回 state 的部分更新）。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.retrievers import BaseRetriever

from capabilities.rag.qa_chain import format_docs
from graphs.state import RagState


def make_retrieve_node(retriever: BaseRetriever):
    """节点工厂: 焊死检索依赖，返回可被 LangGraph 调用的节点函数。

    为什么用闭包而不是把 retriever 放进 state:
        state 将来要被 checkpointer 持久化，只能是可序列化的纯数据；
        retriever 带着向量库连接和嵌入模型，属于运行时对象，不该被序列化。
    """

    def retrieve_node(state: RagState) -> dict:
        # 1. 从状态总线取输入
        question = state["question"]
        # 2. 干活: 检索并拼装上下文（复用阶段1的胶水函数）
        docs = retriever.invoke(question)
        context = format_docs(docs)
        # 3. 只返回要更新的字段，LangGraph 自动合并进 state
        return {"context": context}

    return retrieve_node

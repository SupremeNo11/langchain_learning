"""检索节点 —— 阶段2 任务 2.2

职责：Graph 中的一个节点，输入 question 输出检索到的上下文。
学习目标：掌握节点函数签名（接收 state 返回 state 的部分更新）。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.retrievers import BaseRetriever

from graphs.state import RagState


def make_retrieve_node(retriever: BaseRetriever):
    """通过闭包注入检索器（避免把不可序列化对象放进 state）。

    提示:
        - retriever.invoke(question) 得到 documents
        - 用 format_docs(documents) 拼成 context 字符串
        - 返回 {"context": ...}（LangGraph 会自动合并进 state）
    """

    def retrieve_node(state: RagState) -> dict:
        # TODO(阶段2): 你的实现
        raise NotImplementedError("阶段2 任务 2.2: 实现 retrieve_node")

    return retrieve_node

"""LangGraph 状态定义 —— 阶段2 任务 2.1

职责：定义 Graph 中流转的状态结构（"数据总线"的形状说明书）。
学习目标：掌握 TypedDict 状态、字段合并（Annotated + add_messages）。
对应文档：docs/02-phase2-langgraph.md

关键认知:
    TypedDict 是"字典形状说明书"，运行时就是普通 dict。
    它不提供初始值——初始状态由调用方传入 app.invoke({"question": ...})。
    每个节点返回"要更新的字段子集"，LangGraph 逐字段覆盖合并进 state。
"""
from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class RagState(TypedDict):
    """RAG 工作流状态。

    字段的生命周期:
        question: str   # 调用方注入（入口）
        context:  str   # retrieve 节点写入
        answer:   str   # generate 节点写入
    """
    question: str
    context: str
    answer: str


class AgentState(TypedDict):
    """Agent 工作流状态（阶段2.4 启用）。

    与 RagState 的本质区别:
        RagState 字段默认"覆盖"合并（各节点写各自的字段）
        messages 用 add_messages reducer 改成"追加"合并——
        每个节点返回 {"messages": [新消息]}，新消息被 append 进历史，
        于是 Human/AI/Tool 消息在循环中不断累积，模型每轮都看到完整历史。
    """
    messages: Annotated[list, add_messages]

if __name__ == "__main__":
    from core.llm import create_llm
    from core.retriever import get_retriever
    from core.vectorstore import get_vectorstore
    from capabilities.rag.embedding import get_embeddings
    from graphs.nodes.retrieve import make_retrieve_node
    from graphs.nodes.generate import make_generate_node

    vs = get_vectorstore("docs_kb", get_embeddings("ark"))
    retrieve = make_retrieve_node(get_retriever(vs, 4))
    generate = make_generate_node(create_llm())

    # 这里没有图，而是手动模拟图的行为
    state = {"question": "本项目的四层架构是什么？"}
    print("① 入口:", state)                    # 只有 question
    state.update(retrieve(state))
    print("② 检索后:", list(state.keys()))       # 多了 context
    state.update(generate(state))
    print("③ 生成后:", list(state.keys()))       # 多了 answer
    print("④ 答案:\n", state["answer"], "...")
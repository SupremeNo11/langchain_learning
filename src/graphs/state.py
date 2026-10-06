"""LangGraph 状态定义 —— 阶段2 任务 2.1

职责：定义 Graph 中流转的状态结构（"数据总线"的形状说明书）。
学习目标：掌握 TypedDict 状态、字段合并（Annotated + add_messages）。
对应文档：docs/02-phase2-langgraph.md

关键认知:
    TypedDict 是"字典形状说明书"，运行时就是普通 dict。
    它不提供初始值——初始状态由调用方传入 app.invoke({"question": ...})。
    每个节点返回"要更新的字段子集"，LangGraph 逐字段覆盖合并进 state。
"""
from typing import TypedDict


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

    # 预告(阶段2.4 Agent 时启用): 消息列表字段用 Annotated 改变合并策略——
    #   from typing import Annotated
    #   from langgraph.graph.message import add_messages
    #   messages: Annotated[list, add_messages]   # 默认策略是"覆盖"，add_messages 改成"追加"

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
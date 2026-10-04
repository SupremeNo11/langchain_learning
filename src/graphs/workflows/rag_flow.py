"""RAG 工作流（LangGraph）—— 阶段2 任务 2.3

职责：用 StateGraph 把节点连成有向图并编译。
学习目标：掌握 StateGraph / add_node / add_edge / compile / invoke。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.vectorstores import VectorStore
from langgraph.graph import END, START, StateGraph

from graphs.state import RagState


def build_rag_graph(vectorstore: VectorStore, k: int = 4):
    """构建编译好的 RAG Graph。

    期望用法::

        app = build_rag_graph(vectorstore)
        result = app.invoke({"question": "什么是LangGraph?"})
        print(result["answer"])

    提示:
        - 创建 graph = StateGraph(RagState)
        - add_node("retrieve", make_retrieve_node(retriever))
        - add_node("generate", make_generate_node(llm))
        - 连线: START -> retrieve -> generate -> END
        - graph.compile() 返回可调用对象
    """
    # TODO(阶段2): 你的实现
    raise NotImplementedError("阶段2 任务 2.3: 实现 build_rag_graph")

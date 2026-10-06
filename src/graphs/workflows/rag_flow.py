"""RAG 工作流（LangGraph）—— 阶段2 任务 2.3

职责：用 StateGraph 把节点连成有向图并编译。
学习目标：掌握 StateGraph / add_node / add_edge / compile / invoke。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.vectorstores import VectorStore
from langgraph.graph import END, START, StateGraph

from graphs.state import RagState

from core.retriever import get_retriever
from core.llm import create_llm
from graphs.nodes.retrieve import make_retrieve_node
from graphs.nodes.generate import make_generate_node


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
    graph = StateGraph(RagState)

    retriever = get_retriever(vectorstore, k)
    llm = create_llm()
    # 添加检索和生成节点
    graph.add_node("retrieve", make_retrieve_node(retriever=retriever))
    graph.add_node("generate", make_generate_node(llm))
    # 添加边
    graph.add_edge(start_key="retrieve", end_key="generate")
    # 设置起止节点
    graph.set_entry_point("retrieve")
    graph.set_finish_point("generate")
    # 编译为图
    compiled = graph.compile()

    return compiled

if __name__ == "__main__":
    from core.vectorstore import get_vectorstore
    from capabilities.rag.embedding import get_embeddings
    
    emb = get_embeddings("ark")
    vs = get_vectorstore("docs_kb", emb)

    app = build_rag_graph(vs, k=4)

    result = app.invoke({"question":"本项目的四层架构是什么？"})

    print(result["answer"])



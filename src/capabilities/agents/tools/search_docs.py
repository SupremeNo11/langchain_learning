"""知识库检索工具 —— 阶段2 综合任务（Agentic RAG 核心）

把"检索"从固定管道（阶段1 的 build_rag_chain）降格为 Agent 可自主调用的一个工具:
    模型自己决定: 要不要查知识库、用什么关键词查（自主改写检索词）。
    这就是 Agentic RAG 与传统 RAG 的本质区别——检索从"必然发生的一环"变成"模型的选择"。
"""
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools import tool

from capabilities.rag.qa_chain import format_docs


def make_search_docs_tool(retriever: BaseRetriever):
    """工厂: 注入 retriever，返回一个 @tool 工具。

    新模式——装饰器在工厂体内:
        @tool 装饰器在 make_search_docs_tool 被【调用时】执行（不是 import 时），
        生成的工具通过闭包"记住"retriever——结构与 make_retrieve_node 完全同构，
        只是这次闭包里造出来的不是节点函数，而是一个工具。
    """

    @tool
    def search_docs(query: str) -> str:
        """在项目知识库中检索资料。回答与本项目内容相关的问题之前，必须先调用此工具。"""
        return format_docs(retriever.invoke(query))

    return search_docs

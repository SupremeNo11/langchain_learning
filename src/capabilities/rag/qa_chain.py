"""RAG 问答链路（LCEL）—— 阶段1 任务 1.6

职责：用 `|` 管道把"检索 -> 组装上下文 -> 生成"串成一条可调用链。
学习目标：掌握 LCEL（LangChain Expression Language）组合式编程。
对应文档：docs/01-phase1-langchain-core.md
"""
from langchain_core.vectorstores import VectorStore


def format_docs(documents: list) -> str:
    """将检索到的文档拼装为上下文文本。

    提示:
        用 "\\n\\n---\\n\\n".join(doc.page_content for doc in documents)
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.6: 实现 format_docs")


def build_rag_chain(vectorstore: VectorStore, k: int = 4):
    """构建 RAG 可组合管道。

    期望用法::

        chain = build_rag_chain(vectorstore)
        answer = chain.invoke("什么是LangGraph?")

    提示:
        - retriever = get_retriever(vectorstore, k=k)
        - 管道结构:
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | rag_qa_prompt | create_llm() | StrOutputParser()
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.6: 实现 build_rag_chain")

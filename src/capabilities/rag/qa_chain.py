"""RAG 问答链路（LCEL）—— 阶段1 任务 1.6

职责：用 `|` 管道把"检索 -> 组装上下文 -> 生成"串成一条可调用链。
学习目标：掌握 LCEL（LangChain Expression Language）组合式编程。
对应文档：docs/01-phase1-langchain-core.md
"""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStore

from core.llm import create_llm
from core.prompts import rag_qa_prompt
from core.retriever import get_retriever


def format_docs(documents: list) -> str:
    """将检索到的文档拼装为上下文文本。

    retriever 返回 list[Document]（对象），prompt 需要字符串，
    这个函数就是两种类型之间的胶水。
    """
    return "\n\n---\n\n".join(doc.page_content for doc in documents)


def build_rag_chain(vectorstore: VectorStore, k: int = 4):
    """构建 RAG 可组合管道。

    期望用法::

        chain = build_rag_chain(vectorstore)
        answer = chain.invoke("什么是LangGraph?")
    """
    # 第1块积木: 检索器（也是 Runnable，invoke 返回文档列表）
    retriever = get_retriever(vectorstore, k=k)

    # 第2块积木: 并行字典 -> RunnableParallel
    #   输入一个字符串，同时跑两条支路，合并成 {"context": ..., "question": ...}
    #   注意: key 必须与 rag_qa_prompt 的占位符 {context} {question} 逐字一致（硬契约）
    #   retriever | format_docs: 文档列表 -> 纯文本，普通函数自动包装成 RunnableLambda
    #   RunnablePassthrough: 输入原样直通（问题本身）
    parallel = {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }

    # 第3块积木: 用 | 把所有 Runnable 串成 RunnableSequence
    #   字典 | prompt: 并行结果恰好是 prompt 需要的两个变量
    #   prompt | llm:   消息列表 -> AIMessage
    #   llm | parser:   AIMessage -> 纯字符串
    chain = (
        parallel
        | rag_qa_prompt
        | create_llm()
        | StrOutputParser()
    )
    return chain

if __name__ == "__main__":
    # smoke 测试
    from capabilities.rag.loader import load_directory
    from capabilities.rag.splitter import split_documents
    from capabilities.rag.embedding import get_embeddings
    from core.vectorstore import get_vectorstore
    from capabilities.rag.qa_chain import build_rag_chain
    import time

    emb = get_embeddings(provider="ark")
    vs = get_vectorstore("docs_kb", emb)
    vs.delete_collection()  # 防止重复入库，实际建库时不需要这么干
    vs = get_vectorstore("docs_kb", emb)

    chunks = split_documents(load_directory("data/raw"), chunk_size=500, chunk_overlap=80)
    print(f"切分后 chunk 数: {len(chunks)}")
    assert chunks, "切分结果为空，检查 loader/splitter"

    # 分批入库（避免 429）
    BATCH, SLEEP = 5, 1
    ids = []
    for i in range(0, len(chunks), BATCH):
        ids.extend(vs.add_documents(chunks[i : i + BATCH]))
        time.sleep(SLEEP)
    print(f"✅ 入库完成: {len(ids)} 条")
    assert len(ids) == len(chunks), "入库数量与 chunk 数不一致"

    # qa chain
    chain = build_rag_chain(vs, k=4)
    print(chain.invoke("说清楚本项目的四层架构是什么？"))

    # rag 检索效果检查
    print(chain.invoke("红烧肉怎么做？"))

    

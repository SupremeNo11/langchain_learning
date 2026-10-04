"""向量库封装 —— 阶段1 任务 1.3

职责：统一向量库创建入口（默认 Chroma 持久化）。
学习目标：掌握 VectorStore 概念与 Chroma 初始化。
对应文档：docs/01-phase1-langchain-core.md
"""
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings

from config.settings import settings


def get_vectorstore(
    collection_name: str,
    embeddings: Embeddings,
    persist_dir: str | None = None,
) -> Chroma:
    """获取（或创建）一个持久化向量库实例。

    参数:
        collection_name: 集合名，同一 persist_dir 下可按业务区分集合。
        embeddings: 向量化模型实例。
        persist_dir: 持久化目录，默认取 settings.vector_store_dir。

    提示:
        Chroma(collection_name=..., embedding_function=..., persist_directory=...)
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.3: 实现 get_vectorstore")

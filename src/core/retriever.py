"""检索器封装 —— 阶段1 任务 1.4

职责：从向量库创建检索器，统一返回文档条数等参数。
学习目标：掌握 vectorstore.as_retriever 的用法。
对应文档：docs/01-phase1-langchain-core.md
"""
from langchain_core.vectorstores import VectorStore


def get_retriever(
    vectorstore: VectorStore,
    k: int = 4,
    score_threshold: float | None = None,
):
    """从向量库创建检索器。

    参数:
        vectorstore: 向量库实例。
        k: 返回文档数。
        score_threshold: 相似度阈值（部分向量库支持），None 表示不过滤。

    提示:
        vectorstore.as_retriever(search_kwargs={"k": k, "score_threshold": ...})
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.4: 实现 get_retriever")

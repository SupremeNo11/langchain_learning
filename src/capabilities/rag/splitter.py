"""文档切分 —— 阶段1 任务 1.5

职责：把长文档切成小块，供向量化与检索使用。
学习目标：掌握 TextSplitter 与切分参数（chunk_size / chunk_overlap）。
对应文档：docs/01-phase1-langchain-core.md
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_text_splitter(
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> RecursiveCharacterTextSplitter:
    """递归字符切分器，针对中英文标点优化。

    提示:
        separators=["\\n\\n", "\\n", "。", "！", "？", "；", " ", ""]
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.5: 实现 get_text_splitter")


def split_documents(documents: list, **kwargs) -> list:
    """便捷入口：直接切分文档列表。

    提示:
        get_text_splitter(**kwargs).split_documents(documents)
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.5: 实现 split_documents")

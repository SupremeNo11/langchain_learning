"""文档加载 —— 阶段1 任务 1.5

职责：按文件后缀加载文档（PDF / Markdown / 纯文本），返回 Document 列表。
学习目标：掌握 DocumentLoader 的用法。
对应文档：docs/01-phase1-langchain-core.md
"""
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader

SUPPORTED_SUFFIXES = {".pdf", ".md", ".txt"}


def load_document(path: str | Path) -> list:
    """按后缀加载单个文档。

    参数:
        path: 文件路径。

    返回:
        Document 列表。

    异常:
        ValueError: 不支持的文件类型。

    提示:
        - .pdf  -> PyPDFLoader(path).load()
        - 其他  -> TextLoader(path, encoding="utf-8").load()
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.5: 实现 load_document")


def load_directory(dir_path: str | Path) -> list:
    """递归加载目录下所有支持的文档。

    提示:
        - 遍历 dir_path.rglob("*")
        - 只处理 is_file() 且后缀在 SUPPORTED_SUFFIXES 内的文件
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.5: 实现 load_directory")

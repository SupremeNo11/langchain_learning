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
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(
            f"不支持的文件类型: {suffix or '<无后缀>'}，"
            f"仅支持: {', '.join(sorted(SUPPORTED_SUFFIXES))}"
        )

    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    else:
        # .md 和 .txt 都按 UTF-8 纯文本加载
        loader = TextLoader(str(file_path), encoding="utf-8")

    return loader.load()


def load_directory(dir_path: str | Path) -> list:
    """递归加载目录下所有支持的文档。

    提示:
        - 遍历 dir_path.rglob("*")
        - 只处理 is_file() 且后缀在 SUPPORTED_SUFFIXES 内的文件
    """
    base = Path(dir_path)

    if not base.is_dir():
        raise NotADirectoryError(f"不是有效目录: {base}")

    documents = []
    for file_path in sorted(base.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_SUFFIXES:
            documents.extend(load_document(file_path))

    return documents

if __name__ == "__main__":
    path_str = "data"
    print(len(load_directory(path_str)))
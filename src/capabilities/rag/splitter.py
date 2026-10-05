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
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",  # 段落
            "\n",    # 换行
            "。",    # 中文句号
            "！",    # 中文叹号
            "？",    # 中文问号
            "；",    # 中文分号
            " ",     # 空格（英文断词）
            "",      # 兜底：按字符切
        ],
        length_function=len,
    )


def split_documents(documents: list, **kwargs) -> list:
    """便捷入口：直接切分文档列表。

    提示:
        get_text_splitter(**kwargs).split_documents(documents)
    """
    splitter = get_text_splitter(**kwargs)
    return splitter.split_documents(documents)

if __name__ == "__main__":
    from capabilities.rag.loader import load_directory

    docs = load_directory("data/raw")
    chunks = split_documents(docs, chunk_size=500, chunk_overlap=80)

    print ( "原始文档数:" , len (docs), "| 切分后块数:" , len (chunks)) 
    print ( "--- 第一块 ---" ); print (chunks[ 0 ].page_content) 
    print ( "--- metadata ---" ); print (chunks[ 0 ].metadata)
    


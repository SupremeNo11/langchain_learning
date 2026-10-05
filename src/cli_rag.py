"""RAG问答 CLI

用法：
    python src/cli_rag.py "本项目的四层架构是什么？"

特性：
    - 幂等初始化: 集合为空才入库，第二次运行不重复付费/限流。
"""

import os
import sys
import time
import argparse

from capabilities.rag.qa_chain import build_rag_chain
from capabilities.rag.loader import load_directory
from capabilities.rag.splitter import split_documents
from capabilities.rag.embedding import get_embeddings
from core.vectorstore import get_vectorstore
from core.retriever import get_retriever

COLLECTION_NAME = "docs_kb"
DATA_DIR = "data/raw"
PROVIDER = "ark"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
BATCH = 10
SLEEP = 1
TOP_K = 4

def get_or_build_store():
    """幂等获取向量库：为空时才入库

    Chroma 的 `vs.get()["ids"]` 为空列表时，说明集合里没有记录，
    需要加载文档、切分、分批入库；否则直接复用现有集合，跳过 embedding。
    """

    emb = get_embeddings(PROVIDER)
    vs = get_vectorstore(COLLECTION_NAME, emb)

    existing = vs.get()["ids"]
    if len(existing) > 0:
        print(f"[store] 复用现有集合 '{COLLECTION_NAME}'，已有 {len(existing)} 条记录")
        return vs
    
    print(f"[store] 集合 '{COLLECTION_NAME}' 为空，开始入库...")
    docs = load_directory(DATA_DIR)
    if not docs:
        raise SystemExit(f"目录 {DATA_DIR} 下没有可加载的文档")
    
    chunks = split_documents(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    print(f"[store] 加载 {len(docs)} 个文档 → 切分 {len(chunks)} 个 chunk")

    # 分批入库，避免 429
    ids = []
    for i in range(0, len(chunks), BATCH):
        ids.extend(vs.add_documents(chunks[i:i + BATCH]))
        time.sleep(SLEEP)

    print(f"[store] ✅ 入库完成: {len(ids)} 条")
    return vs

def main() -> None:
    if len(sys.argv) < 2:
        print('用法: python src/cli_rag.py "你的问题"')
        sys.exit(1)

    question = sys.argv[1]

    vs = get_or_build_store()
    chain = build_rag_chain(vs, k=TOP_K)

    print(f"\n[question] {question}")
    answer = chain.invoke(question)
    print("\n=== 回答 ===")
    print(answer)

if __name__ == "__main__":
    main()
    



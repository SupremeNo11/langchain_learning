"""应用装配层 —— 阶段3 任务 3.3

职责: 把分散的能力(向量库/检索器/工具/Agent图)组合成"可运行应用"，
     供 CLI 入口(cli_rag.py / agent_chat.py)与 API 入口(api/) 共享。

架构原则: 入口脚本要薄——只做参数解析和交互循环；凡是"会被别人 import 的逻辑"
必须住在包里。反例: 让 api/main.py 去 import 一个散装脚本(agent_chat.py)——
它不在任何包里，打包系统找不到它，这正是 ModuleNotFoundError 的根源。
"""
import time

from langgraph.checkpoint.memory import MemorySaver

from capabilities.agents.tools.calculator import add
from capabilities.agents.tools.get_time import get_current_time
from capabilities.agents.tools.multiply import multiply
from capabilities.agents.tools.search_docs import make_search_docs_tool
from capabilities.rag.embedding import get_embeddings
from capabilities.rag.loader import load_directory
from capabilities.rag.splitter import split_documents
from core.llm import create_llm
from core.retriever import get_retriever
from core.vectorstore import get_vectorstore
from graphs.workflows.agent_flow import build_agent_graph

# ===== 装配常量（两处入口共享）=====
COLLECTION_NAME = "docs_kb"
DATA_DIR = "data/raw"
PROVIDER = "ark"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
BATCH = 10
SLEEP = 1
TOP_K = 4


def get_or_build_store():
    """幂等获取向量库: 为空时才入库（重复运行不重复付费/限流）。"""
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

    ids = []                       # 分批入库，避免 429
    for i in range(0, len(chunks), BATCH):
        ids.extend(vs.add_documents(chunks[i:i + BATCH]))
        time.sleep(SLEEP)

    print(f"[store] ✅ 入库完成: {len(ids)} 条")
    return vs


def build_chat_agent():
    """装配完整对话 Agent: 向量库 -> 检索器 -> 工具表 -> 带记忆的图。"""
    vs = get_or_build_store()
    retriever = get_retriever(vs, TOP_K)
    tools = [
        add,
        multiply,
        get_current_time,
        make_search_docs_tool(retriever),  # 检索作为工具，交给模型自主决策
    ]
    # MemorySaver 存内存: 进程活着记忆就在，重启即失（生产换 SqliteSaver/PostgresSaver）
    return build_agent_graph(create_llm(), tools, checkpointer=MemorySaver())

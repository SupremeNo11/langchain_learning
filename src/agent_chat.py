"""多轮 Agent 对话 CLI —— 阶段2 综合任务（Agentic RAG）

用法（必须在项目根目录运行，data/raw 的相对路径才有效）:
    python src/agent_chat.py

一次会话三合一:
    多轮记忆（checkpointer + 固定 thread_id）
    自主检索（search_docs 工具，模型自己决定查不查、怎么查）
    工具循环（ReAct: agent -> tools -> agent -> ...）
"""
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from capabilities.agents.tools.calculator import add
from capabilities.agents.tools.get_time import get_current_time
from capabilities.agents.tools.multiply import multiply
from capabilities.agents.tools.search_docs import make_search_docs_tool
from cli_rag import get_or_build_store  # 复用阶段1的幂等建库，不许复制粘贴（DRY）
from core.llm import create_llm
from core.retriever import get_retriever
from graphs.workflows.agent_flow import build_agent_graph

SESSION_ID = "cli-main"
TOP_K = 4


def build_chat_agent():
    """装配: 向量库 -> 检索器 -> 工具表 -> 带记忆的 Agent 图。"""
    vs = get_or_build_store()
    retriever = get_retriever(vs, TOP_K)
    tools = [
        add,
        multiply,
        get_current_time,
        make_search_docs_tool(retriever),  # 检索作为工具交给模型自主决策
    ]
    # MemorySaver 存内存: 进程活着记忆就在，重启即失（生产换 SqliteSaver/PostgresSaver）
    return build_agent_graph(create_llm(), tools, checkpointer=MemorySaver())


def main() -> None:
    app = build_chat_agent()
    # 固定 thread_id = 本次进程内的会话身份，多轮记忆靠它续档
    cfg = {"configurable": {"thread_id": SESSION_ID}}

    print("Agent 对话已就绪（exit/quit/q 退出）\n")
    while True:
        try:
            q = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit", "q"):
            break

        result = app.invoke({"messages": [HumanMessage(q)]}, config=cfg)

        for m in result["messages"]:
            if getattr(m, "tool_calls", None):
                print("  [调用]", m.tool_calls[0]["name"], m.tool_calls[0]["args"])
        # 只打印最后一条 AIMessage——完整历史(含工具调用轨迹)都在 result["messages"] 里
        print(f"AI> {result['messages'][-1].content}\n")

    print("再见！")


if __name__ == "__main__":
    main()

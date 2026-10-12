"""多轮 Agent 对话 CLI —— 阶段2 综合任务（Agentic RAG，入口薄壳）

用法（必须在项目根目录运行，data/raw 的相对路径才有效）:
    python src/agent_chat.py
"""
from langchain_core.messages import HumanMessage

from capabilities.assembly import build_chat_agent

SESSION_ID = "cli-main"


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

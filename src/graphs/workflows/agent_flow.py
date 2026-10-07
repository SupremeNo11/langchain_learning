"""Agent 工作流（ReAct 循环）—— 阶段2 任务 2.4

职责：手搓一个带工具循环的 Agent 图（先懂原理，再用官方封装）。
学习目标：掌握 add_messages 状态、ToolNode、条件边、循环边。
对应文档：docs/02-phase2-langgraph.md

循环结构（Boss 战核心）:

    START → [agent] ──带 tool_calls──> [tools] ──┐
                │                                │
                └──不带 tool_calls──> END        │
                                               ──┘ 这条边回到 agent，形成环
"""
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from capabilities.agents.prompt import agent_prompt
from graphs.state import AgentState


def build_agent_graph(llm: BaseChatModel, tools: list[BaseTool]):
    """构建 ReAct Agent 图。

    参数:
        llm: 模型实例（来自 create_llm 工厂）
        tools: @tool 装饰过的工具列表
    """
    # ---- 装配期（建图时执行一次）----

    # 1. 给模型"工具说明书": bind_tools 把工具的签名+docstring 发给模型，
    #    模型从此知道有哪些工具可调（你在 first_chat 里做过）
    llm_with_tools = llm.bind_tools(tools)

    # 2. 官方工具执行节点: 读 AIMessage.tool_calls → 真正调用函数 →
    #    把结果包装成 ToolMessage 追加进历史。补上了你注释里缺的"真正执行"
    tool_node = ToolNode(tools)

    # ---- 运行期（每次请求执行）----

    def agent_node(state: AgentState) -> dict:
        """决策节点: 看历史，决定直接回答还是调工具。"""
        # 组装消息: system(说明书) + 完整历史(含工具结果)
        messages = agent_prompt.format_messages(messages=state["messages"])
        # 模型决策: 无需工具 → 普通 AIMessage；需要 → AIMessage(带 tool_calls)
        response = llm_with_tools.invoke(messages)
        # add_messages reducer 自动把这条 AIMessage 追加进历史
        return {"messages": [response]}

    def route(state: AgentState) -> str:
        """条件边: 看最后一条消息有没有工具调用意图。"""
        last = state["messages"][-1]
        if getattr(last, "tool_calls", None):
            return "continue"    # 还有工具要调
        return "end"             # 模型已给出最终回答

    # ---- 建图 ----
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")
    # 条件边: route 的返回值在映射表里查到下一跳（图里的 if）
    graph.add_conditional_edges(
        "agent", route, {"continue": "tools", "end": END}
    )
    # 循环边: 工具执行完带着结果回到 agent 重新决策——环就在这一行
    graph.add_edge("tools", "agent")

    return graph.compile()


if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    from capabilities.agents.tools.calculator import add
    from capabilities.agents.tools.multiply import multiply
    from capabilities.agents.tools.get_time import get_current_time
    from core.llm import create_llm

    app = build_agent_graph(create_llm(), [add, multiply, get_current_time])

    print("=== 问题1: 多步工具链（循环的实证）===")
    r1 = app.invoke({"messages": [HumanMessage("先算 123 乘以 456，再把结果加上 789")]})
    for m in r1["messages"]:
        name = type(m).__name__
        for tc in getattr(m, "tool_calls", None) or []:
            print(f"[{name}→工具] {tc['name']}({tc['args']})")
        if m.content:
            print(f"[{name}] {m.content}")

    print("\n=== 问题2: 无需工具（条件边的实证）===")
    r2 = app.invoke({"messages": [HumanMessage("你好，用一句话介绍你自己")]})
    for m in r2["messages"]:
        name = type(m).__name__
        for tc in getattr(m, "tool_calls", None) or []:
            print(f"[{name}→工具] {tc['name']}({tc['args']})")
        if m.content:
            print(f"[{name}] {m.content}")

    print("\n=== 问题3: 获取当前时间===")
    r2 = app.invoke({"messages": [HumanMessage("现在几点了？")]})
    for m in r2["messages"]:
        name = type(m).__name__
        for tc in getattr(m, "tool_calls", None) or []:
            print(f"[{name}→工具] {tc['name']}({tc['args']})")
        if m.content:
            print(f"[{name}] {m.content}")


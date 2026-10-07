# 阶段2：LangGraph 编排

> 目标：掌握 LangGraph 的状态图编程，把阶段1 的 RAG 链升级为 Graph，并实现带工具调用的 Agent。
> 前置：阶段1 全部任务完成，`build_rag_chain` 可用。

## 2.1 任务总览

| 任务 | 文件 | 核心知识点 |
|---|---|---|
| 2.1 | [graphs/state.py](../src/graphs/state.py) | State / TypedDict |
| 2.2 | [graphs/nodes/](../src/graphs/nodes/) | 节点函数 |
| 2.3 | [graphs/workflows/rag_flow.py](../src/graphs/workflows/rag_flow.py) | StateGraph / 边 / compile |
| 2.4 | [agents/](../src/capabilities/agents/) | 工具绑定、Agent 循环 |
| 2.5 | [memory/conversation.py](../src/capabilities/memory/conversation.py) | 记忆 / Checkpointer |

## 2.2 核心概念（先读）

- **State（状态）**：Graph 中流转的数据结构（TypedDict），每个节点返回的部分字典会自动"合并"进状态。
- **Node（节点）**：普通函数，接收 `state`，返回 `dict`（要更新的字段）。
- **Edge（边）**：节点间的连接；`START` 是入口，`END` 是出口；**条件边** `add_conditional_edges` 决定分支。
- **编译与调用**：`graph.compile()` 后 `invoke(初始状态)` 得到最终状态。
- **与 LCEL 的区别**：LCEL 是"线性管道"，Graph 支持**分支、循环、条件、持久化**。

## 2.3 任务 2.1：状态定义

**要求**：在 `RagState` 中定义 `question`、`context`、`answer` 三个字段（均为 str）。

**延伸**：如果状态里有消息列表，用 `Annotated[list, add_messages]` 让多节点追加的消息自动合并。

**自测**：为什么节点返回 `{"context": ...}` 而不是整个状态？——因为 LangGraph 按字段合并。

## 2.4 任务 2.2：检索节点与生成节点

**要求**：实现 `make_retrieve_node`（注入 retriever）与 `make_generate_node`（注入 llm）。

**提示**：用"闭包注入"而不是把 retriever/llm 放进 state——状态应只放可序列化数据。

## 2.5 任务 2.3：RAG 工作流

**要求**：实现 `build_rag_graph`，连线 `START -> retrieve -> generate -> END` 并 `compile()`。

**验收**：

```python
from core.vectorstore import get_vectorstore
from capabilities.rag.embedding import get_embeddings
from graphs.workflows.rag_flow import build_rag_graph

app = build_rag_graph(get_vectorstore("demo", get_embeddings()))
print(app.invoke({"question": "测试问题"}))
```

## 2.6 任务 2.4：带工具的 Agent（本阶段难点）

**要求**

1. 在 `capabilities/agents/prompt.py` 实现 `agent_prompt`（含 `MessagesPlaceholder("messages")`）。
2. 新建 `graphs/workflows/agent_flow.py`，实现一个 ReAct 式 Agent：

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, tools)  # 或自己用 StateGraph 实现循环
```

3. 工具在 [capabilities/agents/tools/](../src/capabilities/agents/tools/) 注册，示例 `add` 已就绪；请**再新增一个工具**（如乘法、取当前时间）。

**自测问题**
- 为什么 Agent 需要"循环"？什么时候退出循环？
> 模型的下一步决策依赖工具的执行结果，而结果在执行之前不存在，所以流程必然是"决策-->执行-->决策再回看"。模型返回单的AIMessage不再带tool_calls，条件边路由到END。
- `bind_tools` 的作用是什么？
> 告诉LLM有哪些工具可以使用。

## 2.7 任务 2.5：会话记忆

**要求**：实现 `get_session_history` / `clear_session`，并在 Graph 中接入 Checkpointer 实现多轮对话记忆。

**提示**：`graph.compile(checkpointer=MemorySaver())`，`invoke` 时传 `config={"configurable": {"thread_id": session_id}}`。

## 2.8 综合任务：多轮 RAG 对话

把阶段1 的 CLI 升级：支持连续提问（记住上文）+ 可选调用工具。

**验收标准**
- 连续两轮对话中，第二轮能引用第一轮的信息。
- Agent 能正确调用你新增的工具并给出计算结果。

---

完成全部任务后，进入 [阶段3：工业级模式](./03-phase3-industrial.md)。

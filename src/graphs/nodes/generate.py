"""生成节点 —— 阶段2 任务 2.2

职责：Graph 中的一个节点，基于上下文生成最终回答。
学习目标：掌握节点函数签名、llm.invoke(messages)。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.language_models import BaseChatModel

from graphs.state import RagState


def make_generate_node(llm: BaseChatModel):
    """通过闭包注入 LLM。

    提示:
        - 用 rag_qa_prompt.format_messages(context=..., question=...) 组装消息
        - llm.invoke(messages) 得到响应，取 response.content
        - 返回 {"answer": ...}
    """

    def generate_node(state: RagState) -> dict:
        # TODO(阶段2): 你的实现
        raise NotImplementedError("阶段2 任务 2.2: 实现 generate_node")

    return generate_node

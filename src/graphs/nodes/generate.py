"""生成节点 —— 阶段2 任务 2.2

职责：Graph 中的一个节点，基于上下文生成最终回答。
学习目标：掌握节点函数签名、llm.invoke(messages)。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.language_models import BaseChatModel

from core.prompts import rag_qa_prompt
from graphs.state import RagState


def make_generate_node(llm: BaseChatModel):
    """节点工厂: 焊死 LLM 依赖，返回生成节点函数。"""

    def generate_node(state: RagState) -> dict:
        # 1. 从状态总线取输入（retrieve 节点已写入 context）
        #    注意 key 必须与 RagState 逐字一致——契约
        messages = rag_qa_prompt.format_messages(
            context=state["context"],
            question=state["question"],
        )
        # 2. 调模型。response 是 AIMessage，取 .content 得纯文本
        #    （阶段1 StrOutputParser 干的就是这件事，这里手动做）
        response = llm.invoke(messages)
        # 3. 只返回要更新的字段
        return {"answer": response.content}

    return generate_node

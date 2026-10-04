"""LangGraph 状态定义 —— 阶段2 任务 2.1

职责：定义 Graph 中流转的状态结构。
学习目标：掌握 TypedDict 状态、字段合并（Annotated + add_messages）。
对应文档：docs/02-phase2-langgraph.md
"""
from typing import TypedDict


class RagState(TypedDict):
    """RAG 工作流状态。

    提示:
        字段设计: question(str) / context(str) / answer(str)
        若状态中包含消息列表，用 Annotated[list, add_messages] 实现自动合并
    """
    # TODO(阶段2): 定义状态字段
    pass

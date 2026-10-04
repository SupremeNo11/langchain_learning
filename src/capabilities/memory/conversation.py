"""会话记忆（短期）—— 阶段2 任务 2.5

职责：按 session_id 隔离的对话历史管理。
学习目标：掌握 BaseChatMessageHistory / InMemoryChatMessageHistory。
对应文档：docs/02-phase2-langgraph.md
"""
from langchain_core.chat_history import BaseChatMessageHistory


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """获取（或创建）指定会话的历史记录。

    提示:
        用一个 dict 存 session_id -> InMemoryChatMessageHistory()，缺失则新建
    """
    # TODO(阶段2): 你的实现
    raise NotImplementedError("阶段2 任务 2.5: 实现 get_session_history")


def clear_session(session_id: str) -> None:
    """清空指定会话的历史。"""
    # TODO(阶段2): 你的实现
    raise NotImplementedError("阶段2 任务 2.5: 实现 clear_session")

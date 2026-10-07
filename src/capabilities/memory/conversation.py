"""会话记忆（短期）—— 阶段2 任务 2.5

职责：按 session_id 隔离的对话历史管理（LCEL 时代的"链级记忆"参考实现）。
学习目标：掌握 BaseChatMessageHistory / InMemoryChatMessageHistory。
对应文档：docs/02-phase2-langgraph.md

时代对比（面试常问）:
    链级记忆（本文件）: 手动管理历史，给 RunnableWithMessageHistory 用
    图级记忆（checkpointer）: LangGraph 自动存档/恢复，你已在 agent_chat 用过
"""
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# 模块级存储: session_id -> 历史实例（进程内有效，重启即失——与 MemorySaver 同类局限）
_store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """获取（或创建）指定会话的历史记录。"""
    if session_id not in _store:
        _store[session_id] = InMemoryChatMessageHistory()
    return _store[session_id]


def clear_session(session_id: str) -> None:
    """清空指定会话的历史。"""
    _store.pop(session_id, None)

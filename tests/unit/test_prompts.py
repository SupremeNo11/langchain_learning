"""Prompt 模板单元测试。"""
from core.prompts import rag_qa_prompt


def test_rag_qa_prompt_format():
    messages = rag_qa_prompt.format_messages(context="示例资料", question="测试问题")
    assert len(messages) == 1
    content = messages[0].content
    assert "示例资料" in content
    assert "测试问题" in content

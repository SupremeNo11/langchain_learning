"""意图路由单元测试。"""
from capabilities.routing.router import route_by_keywords

KEYWORD_MAP = {
    "rag": ["知识库", "文档", "架构", "rag"],
    "agent": ["计算", "时间"],
}


def test_route_rag():
    assert route_by_keywords("本项目的架构是什么？", KEYWORD_MAP) == "rag"


def test_route_agent():
    assert route_by_keywords("帮我计算 123 乘以 456", KEYWORD_MAP) == "agent"


def test_route_default():
    assert route_by_keywords("你好呀", KEYWORD_MAP) == "default"


def test_route_case_insensitive():
    assert route_by_keywords("What is the RAG architecture?", KEYWORD_MAP) == "rag"


def test_route_registration_order_wins():
    """两个 route 同时命中时，注册在前面的赢。"""
    km = {"first": ["a"], "second": ["a", "b"]}
    assert route_by_keywords("a b", km) == "first"

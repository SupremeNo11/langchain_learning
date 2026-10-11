"""意图路由 —— 阶段3 任务 3.2

职责：根据问题内容把请求路由到不同处理链路（关键词版）。
学习目标：掌握规则路由设计；LLM 语义路由是延伸方向。
对应文档：docs/03-phase3-industrial.md
"""


def route_by_keywords(
    question: str,
    keyword_map: dict[str, list[str]],
    default: str = "default",
) -> str:
    """根据关键词命中返回路由名，命中多个时取注册顺序第一个。

    规则:
        1. 问题与关键词都小写化后比对（大小写不敏感）
        2. 按 keyword_map 的注册顺序优先——dict 保序，先注册的先匹配，命中即返回
        3. 全部未命中返回 default
    """
    text = question.lower()
    for route, keywords in keyword_map.items():
        if any(kw.lower() in text for kw in keywords):
            return route
    return default

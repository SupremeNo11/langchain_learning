"""意图路由 —— 阶段3 任务 3.2

职责：根据问题内容把请求路由到不同处理链路（关键词版）。
学习目标：掌握规则路由设计；阶段3 可替换为 LLM 语义路由。
对应文档：docs/03-phase3-industrial.md
"""


def route_by_keywords(
    question: str,
    keyword_map: dict[str, list[str]],
    default: str = "default",
) -> str:
    """根据关键词命中返回路由名，命中多个时取注册顺序第一个。

    期望用法::

        keyword_map = {
            "rag": ["知识库", "文档", "资料"],
            "agent": ["计算", "工具"],
        }
        route = route_by_keywords(question, keyword_map)

    提示:
        - question 先转小写再匹配
        - 遍历 keyword_map 的 key 顺序，命中任一个关键词即返回该 route
        - 全部未命中返回 default
    """
    # TODO(阶段3): 你的实现
    raise NotImplementedError("阶段3 任务 3.2: 实现 route_by_keywords")

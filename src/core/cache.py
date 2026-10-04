"""TTL 内存缓存 —— 阶段3 任务 3.1

职责：带过期时间的简单内存缓存（LRU 淘汰），生产可替换为 Redis。
学习目标：掌握缓存设计要点（TTL / 淘汰 / 线程安全）。
对应文档：docs/03-phase3-industrial.md

验收: 实现后 tests/unit/test_cache.py 应通过。
"""
import time
from collections import OrderedDict


class TTLCache:
    """带 TTL 的内存缓存。

    要求:
        - get(key): 命中且未过期返回 value，否则返回 None（过期即淘汰）
        - set(key, value, ttl=None): 写入并记录过期时间，超过 max_size 淘汰最旧
        - clear(): 清空
    """

    def __init__(self, max_size: int = 128, ttl: float = 300.0):
        # TODO(阶段3): 初始化存储（建议 OrderedDict 实现 LRU）
        raise NotImplementedError("阶段3 任务 3.1: 实现 TTLCache")

    def get(self, key: str):
        # TODO(阶段3): 命中且未过期返回，否则返回 None
        raise NotImplementedError("阶段3 任务 3.1: 实现 get")

    def set(self, key: str, value: object, ttl: float | None = None) -> None:
        # TODO(阶段3): 写入并淘汰最旧
        raise NotImplementedError("阶段3 任务 3.1: 实现 set")

    def clear(self) -> None:
        # TODO(阶段3): 清空
        raise NotImplementedError("阶段3 任务 3.1: 实现 clear")

"""TTL 内存缓存 —— 阶段3 任务 3.1

职责：带过期时间的简单内存缓存（LRU 淘汰），线程安全，生产可替换为 Redis。
学习目标：掌握缓存设计要点（TTL / 淘汰 / 线程安全）。
对应文档：docs/03-phase3-industrial.md

验收: 实现后 tests/unit/test_cache.py 应通过。
"""
import threading
import time
from collections import OrderedDict


class TTLCache:
    """带 TTL 的线程安全内存缓存。

    要求:
        - get(key): 命中且未过期返回 value，否则返回 None（过期即淘汰）
        - set(key, value, ttl=None): 写入并记录过期时间，超过 max_size 淘汰最旧
        - clear(): 清空

    线程安全:
        FastAPI 的同步路由跑在线程池里，多个线程会同时踩这个缓存。
        get/set/clear 都包含"查-再-改"的复合操作（查过期+删、查容量+淘汰），
        GIL 保证不了复合操作的原子性，所以每个方法整体上锁。
    """

    def __init__(self, max_size: int = 128, ttl: float = 300.0):
        self._max_size = max_size
        self._ttl = ttl
        self._store: OrderedDict = OrderedDict()
        self._lock = threading.Lock()   # 为什么用 Lock 不用 RLock: 三个方法互不嵌套调用

    def get(self, key: str):
        with self._lock:               # with 语法: 异常时也保证释放锁
            item = self._store.get(key)
            if item is None:
                return None
            value, expire_at = item
            if time.monotonic() > expire_at:
                del self._store[key]
                return None

            self._store.move_to_end(key)
            return value

    def set(self, key: str, value: object, ttl: float | None = None) -> None:
        with self._lock:
            expire_at = time.monotonic() + (ttl if ttl is not None else self._ttl)
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = (value, expire_at)
            while len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

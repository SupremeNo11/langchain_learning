"""TTL 缓存单元测试。"""
import time

from core.cache import TTLCache


def test_cache_set_get():
    cache = TTLCache()
    cache.set("key", "value")
    assert cache.get("key") == "value"


def test_cache_expire():
    cache = TTLCache(ttl=0.1)
    cache.set("key", "value")
    time.sleep(0.2)
    assert cache.get("key") is None


def test_cache_clear():
    cache = TTLCache()
    cache.set("key", "value")
    cache.clear()
    assert cache.get("key") is None


def test_cache_eviction():
    """超员淘汰: 超过 max_size 时最旧条目被挤掉，其余幸存。"""
    cache = TTLCache(max_size=2)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    cache.set("k3", "v3")           # 超员 → k1（最旧）应被淘汰

    assert cache.get("k1") is None  # 死者
    assert cache.get("k2") == "v2"  # 幸存者
    assert cache.get("k3") == "v3"  # 幸存者


def test_cache_eviction_is_lru_not_fifo():
    """LRU ≠ FIFO: 刚被访问过的 key 不会被淘汰——淘汰的是"最久未访问"，不是"最早写入"。"""
    cache = TTLCache(max_size=2)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    cache.get("k1")                 # k1 刚被访问 → 挪到"最新"端
    cache.set("k3", "v3")           # 超员 → 该淘汰的是 k2（最久未访问），不是 k1

    assert cache.get("k1") == "v1"  # 刚访问过的幸存（这条断言验证 get 里的 move_to_end 真的在起作用）
    assert cache.get("k2") is None  # 真正的"最旧"被淘汰

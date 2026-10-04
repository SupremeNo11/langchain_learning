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

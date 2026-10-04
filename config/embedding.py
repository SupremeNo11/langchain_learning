"""嵌入模型供应商注册表：一处定义，全局复用。"""
from dataclasses import dataclass

@dataclass(frozen=True)
class EmbedProviderConfig:
    model: str
    api_key_env: str
    base_url: str | None = None

EMBED_PROVIDERS: dict[str, EmbedProviderConfig] = {
    "ark": EmbedProviderConfig(
        model="doubao-embedding-vision",
        api_key_env="ARK_API_KEY",
        base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    ),



}

def get_embed_provider(provider: str) -> EmbedProviderConfig:
    """获取供应商配置，未知供应商直接报错（fail-fast）。"""
    if provider not in EMBED_PROVIDERS:
        raise ValueError(
            f"未知 embedding 供应商: {provider}，可选: {list(EMBED_PROVIDERS)}"
        )
    return EMBED_PROVIDERS[provider]
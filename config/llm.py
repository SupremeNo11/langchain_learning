"""模型供应商注册表：一处定义，全局复用。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderConfig:
    model: str
    api_key_env: str  # 对应的环境变量名
    base_url: str | None = None


LLM_PROVIDERS: dict[str, ProviderConfig] = {
    "ark": ProviderConfig(
        model="deepseek-v4.1-flash",
        api_key_env="ARK_API_KEY",
        base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    ),
    "deepseek": ProviderConfig(
        model="deepseek-chat",
        api_key_env="DEEPSEEK_API_KEY",
        base_url="https://api.deepseek.com",
    ),
    "openai": ProviderConfig(
        model="gpt-4o-mini",
        api_key_env="OPENAI_API_KEY",
    ),
    "ollama": ProviderConfig(
        model="qwen2.5:7b",
        api_key_env="",
        base_url="http://localhost:11434/v1",
    ),
}


def get_provider(provider: str) -> ProviderConfig:
    """获取供应商配置，未知供应商直接报错（fail-fast）。"""
    if provider not in LLM_PROVIDERS:
        raise ValueError(
            f"未知 LLM 供应商: {provider}，可选: {list(LLM_PROVIDERS)}"
        )
    return LLM_PROVIDERS[provider]

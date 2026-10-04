"""统一配置：pydantic-settings 从环境变量 / .env 文件读取。"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ===== LLM 供应商 =====
    llm_provider: str = "ark"  # ark / deepseek / openai / ollama
    llm_model: str = "deepseek-v4.1-flash"
    llm_api_key: str = ""
    llm_base_url: str = "https://ark.cn-beijing.volces.com/api/coding/v3"
    llm_temperature: float = 0.0

    # Ark(火山方舟) 专用，兼容 first_chat.py
    ark_api_key: str = ""

    # ===== 向量库 =====
    vector_store_dir: str = "data/vector_db"

    # ===== Embedding（向量化）=====
    # local: fastembed 本地模型（离线免费）；openai: OpenAI 兼容接口
    embedding_provider: str = "local"
    embedding_model: str = "BAAI/bge-small-zh-v1.5"
    embedding_api_key: str = ""
    embedding_base_url: str = "https://ark.cn-beijing.volces.com/api/coding/v3"
    chunk_size: int = 10

    # ===== 日志 =====
    log_level: str = "INFO"

    # ===== LangSmith 追踪(可选) =====
    langsmith_api_key: str = ""
    langsmith_project: str = "langchain-learning"

    @property
    def resolved_api_key(self) -> str:
        """优先取 Ark 专用密钥，其次取通用密钥。"""
        return self.ark_api_key or self.llm_api_key


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

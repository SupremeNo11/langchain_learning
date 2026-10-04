"""向量化封装 —— 阶段1 任务 1.3

职责：创建向量化模型实例（OpenAI 兼容接口）。
学习目标：掌握 Embeddings 概念与 OpenAIEmbeddings 初始化。
对应文档：docs/01-phase1-langchain-core.md

注意: 若当前供应商(base_url)不支持 embedding，需将 LLM_BASE_URL
指向支持 embedding 的 OpenAI 兼容服务。
"""
from langchain_openai import OpenAIEmbeddings

from config.settings import settings


def get_embeddings(model: str = "text-embedding-3-small") -> OpenAIEmbeddings:
    """创建向量化模型实例。

    提示:
        OpenAIEmbeddings(model=..., api_key=settings.resolved_api_key, base_url=...)
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.3: 实现 get_embeddings")

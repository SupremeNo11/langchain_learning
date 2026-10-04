"""向量化封装 —— 阶段1 任务 1.3

职责：创建向量化模型实例（工厂模式，与 core/llm.py 的 create_llm 同理）。
学习目标：掌握 Embeddings 概念（embed_query / embed_documents）与供应商切换。
对应文档：docs/01-phase1-langchain-core.md

背景: ark 的 coding 端点不提供 /embeddings 服务，本项目默认使用
本地模型（fastembed + BAAI/bge-small-zh-v1.5，512 维，中文优化，CPU 可跑）。
以后要换供应商，只需改 .env 中的 EMBEDDING_PROVIDER / EMBEDDING_MODEL。
"""
from langchain_core.embeddings import Embeddings

from config.settings import settings


def get_embeddings(provider: str | None = None) -> Embeddings:
    """创建向量化模型实例。

    参数:
        provider: "local"（本地 fastembed）或 "openai"（OpenAI 兼容接口），
                  默认取 settings.embedding_provider。

    提示:
        - local:  from langchain_community.embeddings import FastEmbedEmbeddings
                  FastEmbedEmbeddings(model_name=settings.embedding_model)
        - openai: from langchain_openai import OpenAIEmbeddings
                  OpenAIEmbeddings(model=settings.embedding_model,
                                   api_key=settings.resolved_api_key)
        - 未知 provider 抛 ValueError（fail-fast，参照 config/llm.py 的做法）
        - 首次运行 fastembed 会下载模型(~100MB)，之后走本地缓存
    """
    # TODO(阶段1): 你的实现
    raise NotImplementedError("阶段1 任务 1.3: 实现 get_embeddings")

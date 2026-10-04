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
from langchain_openai import OpenAIEmbeddings
from config.embedding import get_embed_provider

import os


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
    # 1. 解析供应商
    provider = provider or settings.embedding_provider

    # 2. 根据供应商决定嵌入模型
    if provider == "local":
        from langchain_community.embeddings import FastEmbedEmbeddings
        embed_model = FastEmbedEmbeddings(model=settings.embedding_model)
    elif provider == "ark":
        cfg = get_embed_provider(provider)
        api_key = (
            os.getenv(cfg.api_key_env)
            or settings.embedding_api_key
            or settings.resolved_api_key   # ← .env 里的 ARK_API_KEY 就住在这里
        )
        base_url = cfg.base_url or settings.embedding_base_url
        chunk_size = settings.chunk_size

        embed_model = OpenAIEmbeddings(
            model=cfg.model,
            api_key=api_key,
            base_url=base_url,
            check_embedding_ctx_length = False,    # 直接发送原始文本，因为Ark模型内部已经做了tokenize
            chunk_size = chunk_size, # 最大就是10
        )
    else:
        get_embed_provider(provider)

    return embed_model
    
if __name__ == "__main__":
    emb = get_embeddings("local")
    print ( len (emb.embed_query( "你好，世界" )))

    emb = get_embeddings("ark")
    print ( len (emb.embed_query( "你好，世界" )))

    emb = get_embeddings("openai")  # 值错误，没有添加该供应商
    print ( len (emb.embed_query( "你好，世界" )))
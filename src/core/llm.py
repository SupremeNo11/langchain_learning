"""LLM 工厂 —— 阶段1 任务 1.1

职责：按配置创建模型实例，让业务代码不直接 new 模型。
学习目标：掌握 ChatOpenAI 的初始化参数、配置与密钥的解析。
对应文档：docs/01-phase1-langchain-core.md
"""

import os

from langchain_openai import ChatOpenAI

from config.llm import get_provider
from config.settings import get_settings, settings

# LangSmith 追踪只初始化一次
_tracing_initialized = False


def _ensure_tracing() -> None:
    """配置了 LangSmith 密钥时启用追踪（阶段3-3.5 详讲，这里先埋点）。

    原理: LangSmith 通过环境变量启用，只需在首次调用前设置一次。
    """
    global _tracing_initialized
    if _tracing_initialized:
        return
    _tracing_initialized = True
    if settings.langsmith_api_key:
        os.environ.setdefault("LANGSMITH_API_KEY", settings.langsmith_api_key)
        os.environ.setdefault("LANGSMITH_PROJECT", settings.langsmith_project)
        os.environ["LANGSMITH_TRACING"] = "true"


def create_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
    streaming: bool = False,
) -> ChatOpenAI:
    """创建 ChatOpenAI 实例（兼容 OpenAI 协议的各供应商）。

    参数:
        provider: 供应商名，默认取 settings.llm_provider。
        model: 覆盖模型名（优先级: 显式 > 供应商注册表默认 > 全局配置）。
        temperature: 覆盖温度，None 时用配置值。
        streaming: 是否流式输出。

    密钥解析优先级: 环境变量 > settings.resolved_api_key
    """
    # 1. 解析供应商（未指定则用全局默认）
    provider_explicit = provider is not None
    provider = provider or settings.llm_provider
    cfg = get_provider(provider)  # 未知供应商在此抛 ValueError（fail-fast）

    # 2. 解析密钥: 优先该供应商的环境变量，拿不到退回全局配置
    api_key = os.getenv(cfg.api_key_env) or settings.resolved_api_key

    # 3. 解析模型名: 显式参数优先；未显式指定供应商时允许全局配置覆盖
    #    （模型名与供应商强绑定，切换供应商必须跟着换默认模型）
    if model is None:
        model = cfg.model if provider_explicit else (settings.llm_model or cfg.model)

    # 4. 解析 base_url: 以供应商注册表为准（每个供应商地址不同）
    base_url = cfg.base_url

    # 5. 解析温度与流式
    temperature = settings.llm_temperature if temperature is None else temperature

    # 6. 可选: 启用 LangSmith 追踪
    _ensure_tracing()

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        streaming=streaming,
    )


if __name__ == "__main__":
    print("默认(ark):", create_llm().model_name)
    print("切换openai:", create_llm(provider="openai").model_name)
    print("显式覆盖模型:", create_llm(model="gpt-4o").model_name)

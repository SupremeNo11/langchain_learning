"""FastAPI 应用入口 —— 阶段3 任务 3.3

启动: uvicorn api.main:app --reload
文档: http://localhost:8000/docs

装配策略（工业要点）:
    Agent 图、向量库连接、缓存都是重型资源——在 lifespan 启动阶段装配一次，
    挂到 app.state（FastAPI 的依赖容器）上，所有请求共享。
    反面教材是"每个请求建一次图"：等于每次问答都付一遍冷启动。
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import chat
from core.cache import TTLCache
from core.log import setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期: yield 之前 = 启动装配，之后 = 关闭清理。"""
    # 惰性导入: 建图要拉起向量库和嵌入模型，放到启动阶段而不是 import 阶段
    from capabilities.assembly import build_chat_agent
    from core.llm import create_llm

    app.state.agent = build_chat_agent()       # 完整图: 工具 + 检索 + 记忆
    app.state.chat_llm = create_llm()          # 轻量直答用的裸模型(闲聊分流)
    app.state.cache = TTLCache(max_size=256, ttl=300.0)  # 回答缓存 5 分钟
    yield
    # 关闭阶段: 生产上在这里释放连接池、flush 日志（本项目无资源需释放）


app = FastAPI(
    title="LangChain Learning API",
    description="LangChain + LangGraph 工业级学习项目",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(chat.router)


@app.get("/health", tags=["system"])
async def health() -> dict:
    """健康检查。"""
    return {"status": "ok"}

"""FastAPI 应用入口。

启动: uvicorn api.main:app --reload
"""
from fastapi import FastAPI

from api.routers import chat
from core.log import setup_logging

setup_logging()

app = FastAPI(
    title="LangChain Learning API",
    description="LangChain + LangGraph 工业级学习项目",
    version="0.1.0",
)

app.include_router(chat.router)


@app.get("/health", tags=["system"])
async def health() -> dict:
    """健康检查。"""
    return {"status": "ok"}

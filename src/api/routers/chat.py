"""聊天路由 —— 阶段3 任务 3.3

职责：把 /chat 请求接入完整工作流（记忆 + Graph + 流式）。
学习目标：掌握 FastAPI 异步处理 LLM 请求、Graph 集成。
对应文档：docs/03-phase3-industrial.md
"""
from fastapi import APIRouter

from api.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """对话接口。

    提示:
        - 阶段3 前可先用 create_llm() 直接调用（基础对话）
        - 阶段3 目标: 根据 req.session_id 恢复记忆，
          路由到 RAG / Agent 工作流，返回答案
    """
    # TODO(阶段3): 你的实现
    raise NotImplementedError("阶段3 任务 3.3: 实现 chat")

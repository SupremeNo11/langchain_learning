"""请求 / 响应模型。"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="用户消息", min_length=1)
    session_id: str | None = Field(None, description="会话ID，用于记忆")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="模型回答")
    session_id: str | None = None


class HealthResponse(BaseModel):
    status: str

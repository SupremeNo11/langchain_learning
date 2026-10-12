"""聊天路由 —— 阶段3 任务 3.3

职责: /api/v1/chat 全链路: 缓存 → 意图分流 → Agent 图 / 轻量直答 → 回写缓存
学习目标: FastAPI 异步路由 + LangGraph 集成 + run_in_threadpool 防阻塞。
对应文档: docs/03-phase3-industrial.md

为什么分流能省钱（路由的意义）:
    命中 agent 关键词的问题才进完整图（工具说明书 + 系统提示 + 循环判断，全要付 token）；
    普通闲聊走轻量直答（裸模型一次调用），不进图、不背工具、不读向量库。

为什么必须 run_in_threadpool（防阻塞的核心论证）:
    async 路由跑在事件循环（单线程）上；LangGraph 的 invoke 是同步长耗时操作
    （LLM 网络 IO，秒级）。直接调用 = 事件循环被卡死 = 整个服务单线程化。
    TTLCache 已上锁，被线程池并发踩是安全的——3.1 的伏笔在此回收。
"""
import time

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from langchain_core.messages import HumanMessage

from api.schemas import ChatRequest, ChatResponse
from capabilities.routing.router import route_by_keywords
from core.log import get_logger
from core.prompts import chat_prompt

router = APIRouter(prefix="/api/v1", tags=["chat"])

# 3.5 可观测性: 每个模块一个 logger，输出自动携带模块名(api.routers.chat)
logger = get_logger(__name__)

# 分流关键词表: 命中 → 完整图；未命中 → 轻量闲聊
# （规则路由的宿命: 用户换个说法就漏——"几点"补丁就是实例。漏多了就该换语义路由，见 3.2 延伸）
KEYWORD_MAP = {
    "agent": ["计算", "时间", "几点", "知识库", "文档", "架构", "项目", "多少", "rag"],
}


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, request: Request) -> ChatResponse:
    """对话接口: 缓存 → 路由 → 生成 → 回写缓存。"""
    cache = request.app.state.cache
    session_id = req.session_id or "anonymous"

    # 缓存 key 必须带 session_id:
    #   "我最喜欢的数字乘以8是多少"的答案依赖各会话自己的记忆——
    #   s1 记住了7所以答56；s2 从没说过7，答案必然不同。
    #   若只用消息做 key，s2 会命中 s1 缓存的"56"——拿到别人的错误答案。
    cache_key = f"{session_id}:{req.message}"

    start = time.perf_counter()   # perf_counter: 高分辨率单调时钟（与 TTLCache 同族）

    cached = cache.get(cache_key)
    if cached is not None:
        # 命中: 路由根本没执行，所以 route 记 "--"；只记问题前20字符——
        # 完整用户内容属敏感数据，日志要克制（可观测性与隐私的权衡）
        logger.info("chat | session=%s | route=-- | cache=hit | q=%.20s | cost=%.0fms",
                    session_id, req.message, (time.perf_counter() - start) * 1000)
        return ChatResponse(answer=cached, session_id=session_id)   # 命中: 秒回，不打 LLM

    # 意图分流: 3.2 的函数在此接线
    route = route_by_keywords(req.message, KEYWORD_MAP, default="chat")

    if route == "agent":
        # 完整图: 工具 + 检索 + 记忆（thread_id 按会话隔离，checkpointer 续档）
        config = {"configurable": {"thread_id": session_id}}
        result = await run_in_threadpool(          # 重型 invoke 丢线程池，事件循环不被卡死
            request.app.state.agent.invoke,
            {"messages": [HumanMessage(req.message)]},
            config,
        )
        answer = result["messages"][-1].content
    else:
        # 轻量直答: 不进图、不背工具、不读向量库——省 token 省延迟
        # （代价: 闲聊无记忆，这是分流的权衡）
        messages = chat_prompt.format_messages(role="简洁的中文助手", question=req.message)
        response = await run_in_threadpool(request.app.state.chat_llm.invoke, messages)
        answer = response.content

    # 3.5: 请求完成日志——route/cache/cost 三元组让每条请求的路径一目了然
    logger.info("chat | session=%s | route=%s | cache=miss | q=%.20s | cost=%.0fms",
                session_id, route, req.message, (time.perf_counter() - start) * 1000)

    cache.set(cache_key, answer)
    return ChatResponse(answer=answer, session_id=session_id)

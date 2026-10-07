# 阶段3：工业级模式

> 目标：把阶段1/2 的能力封装成生产级 API，补齐缓存、路由、可观测性、评估。
> 前置：阶段2 全部任务完成。

## 3.1 任务总览

| 任务 | 文件 | 核心知识点 |
|---|---|---|
| 3.1 | [core/cache.py](../src/core/cache.py) | 缓存设计（TTL/LRU） |
| 3.2 | [routing/router.py](../src/capabilities/routing/router.py) | 意图路由 |
| 3.3 | [api/routers/chat.py](../src/api/routers/chat.py) | FastAPI 集成 Graph |
| 3.4 | [tests/eval/](../tests/eval/) | 评估体系（Ragas） |
| 3.5 | core/logging + LangSmith | 可观测性 |

## 3.2 任务 3.1：TTL 缓存

**要求**：实现 `TTLCache`（get/set/clear），`set` 时记录过期时间，超过 `max_size` 淘汰最旧条目。

**验收**：`pytest tests/unit/test_cache.py -v` 通过。

**延伸思考**：生产环境换成 Redis 需要改哪些地方？——只需替换实现，保持接口不变（这就是封装的意义）。

**线程安全思考题（答案）**：TTLCache 挂进 FastAPI 安全吗？——**取决于路由是同步还是异步**：
- `def`（同步）路由：FastAPI 默认把它们丢进**线程池**（anyio threadpool）并发执行 → 多线程同时踩 `get`/`set` 同一个 OrderedDict → 撞车风险（两个线程同时淘汰、遍历时被改结构）。GIL 只保证单条字节码原子，管不住"查-再-改"这类复合操作。
- `async def` 路由：跑在事件循环（**单线程**）上 → 天然串行、安全——但同步 get/set 会阻塞事件循环（微秒级操作，可接受；换 Redis 网络调用就必须放线程池）。
- 工业解法：`threading.Lock` 包住 get/set/clear（**已加固**，见 cache.py——用 Lock 而非 RLock，因三方法互不嵌套）；或直接换 Redis——原子命令，还顺带解决多 worker 部署下的缓存共享。

## 3.3 任务 3.2：意图路由

**要求**：实现 `route_by_keywords`，根据关键词把问题路由到 `rag` / `agent` / `default` 等处理链路。

**验收**：

```python
from capabilities.routing.router import route_by_keywords
m = {"rag": ["知识库", "文档"], "agent": ["计算", "工具"]}
assert route_by_keywords("怎么计算2+2", m) == "agent"
```

**延伸**：关键词路由 → LLM 语义路由（用一次小模型调用判断意图）。

## 3.4 任务 3.3：API 全链路

**要求**：实现 `/api/v1/chat`，做到：

1. 根据 `req.session_id` 恢复/新建会话记忆；
2. 用 `route_by_keywords` 路由到 RAG Graph 或 Agent；
3. 返回答案与 `session_id`。

**运行**：

```bash
uvicorn api.main:app --reload
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "s1"}'
```

**验收**：`/health` 返回 ok；连续两次 `/chat` 第二次能记忆上文。

## 3.5 任务 3.4：评估体系（本阶段重点）

**要求**

1. 在 `data/` 下准备一份问答测试集（问题 + 标准答案 + 参考文档片段），存入 `tests/eval/`。
2. 在 [tests/eval/](../tests/eval/) 实现批量评测脚本，覆盖指标：
   - 忠实度（faithfulness）：回答是否基于文档
   - 相关性（relevance）：回答是否切题
   - 答案正确性（correctness）
3. 输出评测报告（每问得分 + 平均分），记录到 `tests/eval/report.md`。

**验收**：评测脚本可运行并产出报告；至少 5 条测试用例。

## 3.6 任务 3.5：可观测性

**要求**

1. 确保所有关键链路输出结构化日志（用 [core/log.py](../src/core/log.py) 的 `get_logger`）。
2. （可选）接入 LangSmith：配置 `LANGSMITH_API_KEY` 后，链/图自动产生追踪。

**自测**：线上出问题，你凭什么定位？——日志 + 追踪 + 评估数据。

## 3.7 综合任务：交付一个"生产级"问答服务

整合 3.1~3.5，交付：

- 可运行 API（记忆 + 路由 + RAG/Agent 双链路）
- 缓存生效（重复问题秒回）
- 评测报告（证明质量）
- 一份简短的使用说明

**验收标准**
- 接口文档：`http://localhost:8000/docs`（FastAPI 自动生成）
- 评测报告各项指标达到你设定的及格线

---

恭喜，完成本项目！可继续挑战的进阶方向：多 Agent 协作、人机协同（interrupt）、Self-RAG / CRAG、流式输出、结构化数据提取。

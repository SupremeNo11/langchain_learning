"""批量评估 —— 阶段3 任务 3.4

流程: dataset.json 每条用例 -> POST /api/v1/chat -> LLM 裁判打分 -> tests/eval/report.md

设计决策:
    - 走 HTTP 而不是直调图: 评估的是真实产品（分流/缓存/记忆全链路）
    - session_id 每用例唯一(eval-{id}): 用例互不污染；同一用例 5 分钟内重跑会命中缓存，
      结果逐字复现——评测可复现性是缓存的红利
    - LLM 裁判用 with_structured_output（结构化输出的第一次真实落地）
    - 裁判 temperature=0: 评估要可复现，不要创造性
    - 单一分数(0/1/2)是简化版; Ragas 三维指标(忠实度/相关性/正确性)是延伸方向

前置: uvicorn api.main:app 必须在运行
用法: python tests/eval/run_eval.py   （项目根目录）
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Literal

import httpx
from pydantic import BaseModel, Field

from core.llm import create_llm

API_URL = "http://localhost:8000/api/v1/chat"
HERE = Path(__file__).parent
DATASET = HERE / "dataset.json"
REPORT = HERE / "report.md"


class Verdict(BaseModel):
    """裁判的结构化输出。"""
    score: Literal[0, 1, 2] = Field(description="0=错误/编造, 1=部分正确, 2=完全正确")
    reason: str = Field(description="一句话评分理由")


JUDGE_PROMPT = """你是严格的评估裁判，根据【标准答案要点】评估【实际回答】。

评分标准:
- 2 分: 要点全覆盖且事实正确。若标准答案要求"拒答"，实际回答正确拒答同样得 2 分
- 1 分: 部分正确、遗漏要点或表述含糊
- 0 分: 错误、答非所问；或标准答案要求拒答时却编造了内容

【问题】{question}
【标准答案要点】{expected}
【实际回答】{answer}

只输出评分结构。"""


def ask_api(question: str, session_id: str) -> str:
    """调用被测系统。"""
    resp = httpx.post(API_URL, json={"message": question, "session_id": session_id}, timeout=180)
    resp.raise_for_status()
    return resp.json()["answer"]


def judge(question: str, expected: str, answer: str) -> Verdict:
    """LLM 裁判打分。"""
    judge_llm = create_llm(temperature=0).with_structured_output(Verdict)
    return judge_llm.invoke(
        JUDGE_PROMPT.format(question=question, expected=expected, answer=answer)
    )


def main() -> None:
    cases = json.loads(DATASET.read_text(encoding="utf-8"))
    n = len(cases)
    print(f"载入 {n} 条用例\n")

    rows, total = [], 0
    for case in cases:
        cid = case["id"]
        print(f"[{cid}/{n}] {case['question']}")
        answer = ask_api(case["question"], f"eval-{cid}")
        verdict = judge(case["question"], case["expected"], answer)
        total += verdict.score
        rows.append((cid, case["question"], answer, verdict.score, verdict.reason))
        print(f"    得分 {verdict.score}/2: {verdict.reason}\n")

    avg = total / n
    lines = [
        "# 评估报告",
        "",
        f"- 时间: {datetime.now():%Y-%m-%d %H:%M}",
        f"- 用例数: {n}    总分: {total}/{n * 2}    平均: {avg:.2f}/2",
        "",
        "| ID | 用例 | 得分 | 裁判理由 | 实际回答(截断) |",
        "|---|---|---|---|---|",
    ]
    for cid, q, a, s, r in rows:
        lines.append(f"| {cid} | {q[:30]} | {s}/2 | {r} | {a.replace(chr(10), ' ')[:120]} |")

    lines += [
        "",
        "## 结论",
        "",
        f"平均 {avg:.2f}/2，" + ("达标。" if avg >= 1.5 else "未达标——优先修复低分用例。"),
        "",
        "> 5 分钟内重跑，缓存使命中结果逐字复现（可复现性是缓存的红利）。",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"报告已写入: {REPORT}")
    print(f"平均分: {avg:.2f}/2")


if __name__ == "__main__":
    main()

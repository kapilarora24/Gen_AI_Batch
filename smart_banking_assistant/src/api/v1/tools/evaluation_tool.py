"""
Runtime evaluation node for the Smart Banking Assistant LangGraph workflow.

This node evaluates the generated response after the output guardrail.
It is intentionally non-blocking: evaluation failures should never prevent
a valid banking response from being returned.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict


def _has_citations(state: Dict[str, Any]) -> bool:
    citations = state.get("citations") or state.get("response_sources")
    return bool(citations)


def _score_response(state: Dict[str, Any]) -> Dict[str, Any]:
    answer = str(state.get("answer") or "").strip()
    question = str(state.get("question") or "").strip()
    query_type = str(state.get("query_type") or "")
    confidence = float(state.get("confidence_score") or 0.0)
    citations_present = _has_citations(state)
    checks = {
        "answer_present": bool(answer),
        "question_present": bool(question),
        "routing_present": bool(query_type),
        "citations_present": citations_present,
        "confidence_available": confidence > 0.0,
    }
    # Lightweight runtime quality score. This is deliberately deterministic
    # and does not call another LLM during the user request.
    weights = {
        "answer_present": 0.35,
        "question_present": 0.10,
        "routing_present": 0.15,
        "citations_present": 0.20,
        "confidence_available": 0.20,
    }
    score = sum(weights[k] for k, passed in checks.items() if passed)
    score = round(min(max(score, 0.0), 1.0), 4)
    status = "passed" if score >= 0.70 else "needs_review"
    return {
        "score": score,
        "status": status,
        "checks": checks,
        "query_type": query_type,
        "confidence_score": confidence,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }


def evaluation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate the final response after output guardrail.
    Evaluation is observability/quality metadata only. It does not modify
    the user-facing answer and does not block the workflow.
    """
    try:
        evaluation = _score_response(state)
        state["evaluation"] = evaluation
        state["evaluation_score"] = evaluation["score"]
        state["evaluation_status"] = evaluation["status"]
        print(
            "EVALUATION:",
            f"status={evaluation['status']}",
            f"score={evaluation['score']}",
        )
    except Exception as exc:
        # Never break the banking assistant because evaluation failed.
        state["evaluation"] = {
            "score": 0.0,
            "status": "error",
            "error": str(exc),
        }
        state["evaluation_score"] = 0.0
        state["evaluation_status"] = "error"
        print("EVALUATION ERROR:", repr(exc))

    return state

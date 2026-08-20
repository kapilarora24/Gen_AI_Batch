"""
Offline-friendly evaluation runner for the Smart Banking Assistant.
Usage:
    uv run python -m evaluation.evaluator
    uv run python -m evaluation.evaluator --dataset evaluation/dataset.json
The runner evaluates:
- query routing accuracy
- expected keyword presence
- citation presence when required
- confidence score
- end-to-end pass rate
Set EVAL_ACCOUNT_ID to an account that is safe to use for SQL test cases.
For SQL/hybrid cases the dataset is intentionally small and should be adapted
to the test database schema/data.
"""

from __future__ import annotations
import argparse
import json
import os
import statistics
import sys
from pathlib import Path
from typing import Any
from src.api.v1.services.query_service import query_documents

# Allow `python evaluation/evaluator.py` from project root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_dataset(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def evaluate_case(case: dict[str, Any], account_id: str | None) -> dict[str, Any]:
    try:
        result = query_documents(
            question=case["question"],
            account_id=account_id,
            thread_id=f"eval-{case['id']}",
        )
        answer = str(result.get("answer", ""))
        query_type = result.get("query_type", "")
        citations = result.get("citations") or []
        confidence = float(result.get("confidence_score") or 0)
        keyword_hits = [
            kw
            for kw in case.get("expected_keywords", [])
            if kw.lower() in answer.lower()
        ]
        type_ok = query_type == case.get("expected_query_type")
        keywords_ok = len(keyword_hits) == len(case.get("expected_keywords", []))
        citation_ok = (not case.get("must_have_citation", False)) or bool(citations)
        return {
            "id": case["id"],
            "question": case["question"],
            "query_type": query_type,
            "expected_query_type": case.get("expected_query_type"),
            "type_ok": type_ok,
            "keyword_hits": keyword_hits,
            "keywords_ok": keywords_ok,
            "citation_ok": citation_ok,
            "confidence_score": confidence,
            "passed": type_ok and keywords_ok and citation_ok and bool(answer.strip()),
            "answer": answer,
            "citations": citations,
            "error": None,
        }
    except Exception as exc:
        return {
            "id": case["id"],
            "question": case["question"],
            "passed": False,
            "error": repr(exc),
        }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    passed = [r for r in results if r.get("passed")]
    scores = [r["confidence_score"] for r in results if "confidence_score" in r]
    return {
        "cases": len(results),
        "passed": len(passed),
        "pass_rate": round(len(passed) / len(results), 4) if results else 0,
        "routing_accuracy": (
            round(sum(bool(r.get("type_ok")) for r in results) / len(results), 4)
            if results
            else 0
        ),
        "citation_compliance": (
            round(sum(bool(r.get("citation_ok")) for r in results) / len(results), 4)
            if results
            else 0
        ),
        "mean_confidence": round(statistics.mean(scores), 4) if scores else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        default=str(ROOT / "evaluation" / "dataset.json"),
    )
    parser.add_argument("--account-id", default=os.getenv("EVAL_ACCOUNT_ID"))
    parser.add_argument("--output", default=str(ROOT / "evaluation" / "results.json"))
    args = parser.parse_args()
    dataset = load_dataset(args.dataset)
    results = [evaluate_case(case, account_id=args.account_id) for case in dataset]
    summary = summarize(results)
    payload = {"summary": summary, "results": results}
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2))
    print(f"Detailed results: {args.output}")


if __name__ == "__main__":
    main()

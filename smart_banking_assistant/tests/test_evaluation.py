from evaluation.evaluator import summarize


def test_evaluation_summary():
    results = [
        {"passed": True, "type_ok": True, "citation_ok": True, "confidence_score": 0.9},
        {"passed": False, "type_ok": False, "citation_ok": True, "confidence_score": 0.4},
    ]
    summary = summarize(results)
    assert summary["cases"] == 2
    assert summary["passed"] == 1
    assert summary["pass_rate"] == 0.5
    assert summary["routing_accuracy"] == 0.5

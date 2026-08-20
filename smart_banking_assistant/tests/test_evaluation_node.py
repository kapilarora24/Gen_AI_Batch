from src.api.v1.tools.evaluation_tool import evaluation_node


def test_evaluation_node_passes_complete_response():
    state = {
        "question": "What is an SIP?",
        "query_type": "rag",
        "answer": "An SIP is a systematic investment plan.",
        "citations": [{"source": "faq.pdf"}],
        "confidence_score": 0.9,
    }

    result = evaluation_node(state)

    assert "evaluation" in result
    assert result["evaluation_status"] == "passed"
    assert 0.0 <= result["evaluation_score"] <= 1.0


def test_evaluation_node_is_non_blocking():
    state = {
        "question": "hello",
        "query_type": "conversation",
        "answer": "Hello!",
    }

    result = evaluation_node(state)

    assert "evaluation" in result
    assert result["evaluation_status"] in {"passed", "needs_review"}

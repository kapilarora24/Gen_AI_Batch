from functools import lru_cache
from transformers import pipeline
from src.api.v1.states.rag_state import RAGState

TOXICITY_THRESHOLD = 0.80
MODEL_NAME = "unitary/toxic-bert"


@lru_cache(maxsize=1)
def get_toxicity_classifier():
    """
    Load the toxicity model once and reuse it.
    """
    return pipeline(
        "text-classification",
        model=MODEL_NAME,
        top_k=None,
    )


def check_input_toxicity(question: str) -> dict:
    """
    Standalone toxicity classification.
    """
    if not question or not question.strip():
        return {
            "guardrail_status": "safe",
            "toxicity_score": 0.0,
            "label": "non_toxic",
        }
    classifier = get_toxicity_classifier()
    results = classifier(question)
    if results and isinstance(results[0], list):
        results = results[0]
    scores = {item["label"].lower(): float(item["score"]) for item in results}
    toxicity_labels = {
        "toxic",
        "severe_toxic",
        "obscene",
        "threat",
        "insult",
        "identity_hate",
    }
    toxicity_score = max(
        (scores.get(label, 0.0) for label in toxicity_labels),
        default=0.0,
    )
    is_blocked = toxicity_score >= TOXICITY_THRESHOLD
    return {
        "guardrail_status": ("blocked" if is_blocked else "safe"),
        "toxicity_score": round(toxicity_score, 4),
        "label": ("toxic" if is_blocked else "non_toxic"),
    }


def input_guardrail(state: RAGState) -> RAGState:
    """
    LangGraph input guardrail node.
    """
    result = check_input_toxicity(state["question"])
    state["input_guardrail_status"] = result["guardrail_status"]
    state["input_toxicity_score"] = result["toxicity_score"]
    if result["guardrail_status"] == "blocked":
        state["answer"] = "I’m unable to help with that request."
        state["confidence_score"] = 0.0
    return state

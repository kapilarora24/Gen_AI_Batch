from guardrails import Guard
from guardrails.hub import DetectPII
from src.api.v1.states.rag_state import RAGState

pii_guard = Guard().use(
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="fix")
)


def output_guardrail(state: RAGState) -> RAGState:
    """
    Output PII protection using Guardrails AI.
    """
    answer = state.get("answer", "")
    if not answer:
        state["output_guardrail_status"] = "clean"
        state["detected_pii"] = []
        return state
    result = pii_guard.validate(answer)
    state["answer"] = result.validated_output
    if result.validation_passed:
        state["output_guardrail_status"] = "clean"
        state["detected_pii"] = []
    else:
        state["output_guardrail_status"] = "masked"
        state["detected_pii"] = ["email", "phone"]
    return state

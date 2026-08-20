from src.api.v1.states.rag_state import RAGState
from src.memory.mem0_service import mem0_service


def load_memory(state: RAGState) -> RAGState:
    """Load relevant long-term memories before query classification."""
    memories = mem0_service.search(
        query=state["question"],
        account_id=state.get("account_id"),
        thread_id=state.get("thread_id"),
        limit=5,
    )
    state["memories"] = memories
    state["memory_context"] = "\n".join(
        f"- {item['memory']}" for item in memories if item.get("memory")
    )
    return state


def save_memory(state: RAGState) -> RAGState:
    """Persist the completed turn to Mem0 when memory is enabled."""
    saved = mem0_service.add_turn(
        question=state.get("question", ""),
        answer=state.get("answer", ""),
        account_id=state.get("account_id"),
        thread_id=state.get("thread_id"),
    )
    state["memory_saved"] = saved
    return state

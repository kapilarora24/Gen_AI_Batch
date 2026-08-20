# Integrating mem0 (cloud hosted SaaS platform) into the Agentic RAG System

Adds long-term, per-user memory to the existing LangGraph pipeline using the **mem0 SaaS platform** — storage, fact extraction, and embeddings all run on mem0's side. Nothing new to host.

Current flow:

```
router → vector_search → rerank → generate_answer → END
       → nl2sql → END
```

Target flow:

```
recall_memory → router → vector_search → rerank → generate_answer → save_memory → END
                       → nl2sql ───────────────────────────────────→ save_memory → END
```

`recall_memory` fetches facts about the user before answering. `save_memory` stores the turn afterwards.

> Implemented on the **`mem0-integration`** branch. Files touched:
>
> | File                                   | Change                                  |
> | -------------------------------------- | --------------------------------------- |
> | `src/core/memory.py`                   | new — cached `MemoryClient`             |
> | `src/api/v1/states/rag_state.py`       | `user_id`, `memory_context`             |
> | `src/api/v1/agents/agents.py`          | 2 nodes, 2 prompts, graph, both runners |
> | `src/api/v1/schemas/query_schema.py`   | `user_id` on `QueryRequest`             |
> | `src/api/v1/services/query_service.py` | thread `user_id`                        |
> | `src/api/v1/routes/query.py`           | thread `user_id`                        |
> | `.env.example`                         | `MEM0_API_KEY`                          |

---

## Step 1 — Install

```bash
uv add mem0ai
```

Same package as the open-source version — the hosted client ships inside it. No database driver, no vector store, no extra dependency.

> Verified against **mem0ai 2.0.17**. The 2.x client changed its call signatures — code written for 1.x (`search(..., user_id=...)`) raises `ValueError` on 2.x. The snippets below are the 2.x forms.

---

## Step 2 — Get an API key

1. Sign up at <https://app.mem0.ai>
2. **API Keys** → create a key (starts with `m0-`)

Append to `.env.example`:

```bash
# mem0 hosted platform
MEM0_API_KEY=m0-your-key-here
```

Put the real key in `.env`.

> Queries and generated answers are sent to mem0's cloud for fact extraction. Use non-sensitive data for the course demo.

---

## Step 3 — Create `src/core/memory.py`

```python
import os
from functools import lru_cache
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()


@lru_cache(maxsize=1)
def get_memory() -> MemoryClient:
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise ValueError("MEM0_API_KEY is not set. Check your .env")
    return MemoryClient(api_key=api_key)
```

That is the whole setup — no vector store config, no embedding dimensions, no LLM config. The platform handles all of it.

`lru_cache` reuses one client (and its HTTP connection pool) across requests.

---

## Step 4 — Extend the state

`src/api/v1/states/rag_state.py`:

```python
class RAGState(TypedDict):
    query: str
    retrieved_docs: List[Document]
    reranked_docs: List[Document]
    response: dict
    route: str
    generated_sql: str
    sql_result: str
    user_id: str          # who is asking
    memory_context: str   # recalled facts, injected into prompts
```

---

## Step 5 — Add the memory nodes

In `src/api/v1/agents/agents.py`, import the helper:

```python
from src.core.memory import get_memory
```

Then add two nodes:

```python
def recall_memory_node(state: RAGState) -> RAGState:
    memory = get_memory()
    hits = memory.search(
        state["query"], filters={"user_id": state["user_id"]}, top_k=5
    )
    facts = [h["memory"] for h in hits.get("results", [])]

    print(f"[recall_memory_node] {len(facts)} memories recalled for {state['user_id']}")
    for f in facts:
        print("  -", f)

    memory_context = "\n".join(f"- {f}" for f in facts) if facts else "No prior context."
    return {**state, "memory_context": memory_context}


def save_memory_node(state: RAGState) -> RAGState:
    memory = get_memory()
    # only the user's turn — see "What gets remembered" below
    messages = [{"role": "user", "content": state["query"]}]
    memory.add(messages, user_id=state["user_id"])
    print(f"[save_memory_node] Turn saved for {state['user_id']}")
    return state
```

Two API details that are easy to get wrong on 2.x:

- `search()` **rejects** a top-level `user_id=` — it must go in `filters`. The row limit is `top_k`, not `limit`.
- `add()` is the opposite: it takes `user_id=` directly as a kwarg.

`memory.add()` does not store the raw text. mem0's platform runs an LLM over the turn, extracts durable facts ("is a contract employee", "based in Chennai"), and deduplicates them against what it already knows about that `user_id`.

### What gets remembered

Feeding the **assistant's** answer into `add()` as well seems natural, but it pollutes memory with document content. Measured on this project's data — the same turn saved both ways, then queried with `"What is my notice period?"`:

| Saved            | Extracted memories                                                        | score     |
| ---------------- | ------------------------------------------------------------------------- | --------- |
| user + assistant | `Contract employees in Chennai receive 12 leave days per the 2026 policy` | **0.238** |
|                  | `User is a contract employee based in Chennai`                            | 0.171     |
|                  | `User prefers answers in short bullet points`                             | 0.086     |
| user only        | `User is a contract employee`                                             | 0.164     |
|                  | `User is based in Chennai`                                                | 0.088     |
|                  | `User prefers answers in short bullet points`                             | 0.086     |

In the first case the top-ranked "memory" is a fragment of the HR policy — it outranks both real preferences on a question it has nothing to do with, and it will be injected into every future prompt as a fact about the user. Saving only the user turn keeps memory to actual preferences.

---

## Step 6 — Use the recalled memory in the prompts

**`generate_answer_node`** — insert the block after the first two lines of the system prompt, before the existing `IMPORTANT:` section:

```python
                    You are a helpful assistant. Answer the user's question using only the
                    provided context.

                    Known facts about this user (use these to personalise the answer -
                    e.g. which policy applies to them - but NEVER treat them as a source
                    of policy truth. The context below is the only source of truth):
                    {memory_context}

                    IMPORTANT:
                    ... rest of the existing prompt unchanged ...
```

```python
    result = chain.invoke(
        {
            "context": context,
            "query": state["query"],
            "memory_context": state["memory_context"],
        }
    )
```

**`nl2sql_node`** — same idea in the SQL prompt, so "show my orders" can resolve to a customer. Insert above the existing `Rules:` line:

```python
                    You are a PostgreSQL expert. Given the database schema below,
                    write a single valid SELECT query that answers the user's question.

                    Known facts about this user (use to resolve "my", "mine" etc.):
                    {memory_context}

                    Rules:
                    ... rest of the existing prompt unchanged ...
```

```python
    raw_sql = sql_chain.invoke(
        {
            "schema": schema_info,
            "question": state["query"],
            "memory_context": state["memory_context"],
        }
    )
```

> Careful: these prompts use `{}` placeholders. Any literal braces you add (none here) would need escaping as `{{ }}`.

---

## Step 7 — Rewire the graph

In `build_rag_graph()`:

```python
    workflow.add_node("recall_memory", recall_memory_node)
    workflow.add_node("router", router_node)
    workflow.add_node("nl2sql", nl2sql_node)
    workflow.add_node("vector_search", vector_search_node)
    workflow.add_node("rerank", rerank_node)
    workflow.add_node("generate_answer", generate_answer_node)
    workflow.add_node("save_memory", save_memory_node)

    workflow.set_entry_point("recall_memory")
    workflow.add_edge("recall_memory", "router")

    workflow.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {"VECTOR_DB": "vector_search", "RDBMS": "nl2sql"},
    )

    workflow.add_edge("vector_search", "rerank")
    workflow.add_edge("rerank", "generate_answer")
    workflow.add_edge("generate_answer", "save_memory")
    workflow.add_edge("nl2sql", "save_memory")
    workflow.add_edge("save_memory", END)
```

The entry point moves from `router` to `recall_memory`, and both branches now end at `save_memory`.

---

## Step 8 — Pass `user_id` end to end

**`src/api/v1/schemas/query_schema.py`:**

```python
class QueryRequest(BaseModel):
    query: str = Field(description="The user's question")
    user_id: str = Field(default="demo_user", description="Identifies the memory owner")
```

**`src/api/v1/agents/agents.py`** — both runners:

```python
def run_search_agent(query: str, user_id: str):
    initial_state = {
        "query": query,
        "retrieved_docs": [],
        "reranked_docs": [],
        "response": {},
        "user_id": user_id,
        "memory_context": "",
    }
    final_state = rag_graph.invoke(initial_state)
    return final_state["response"]


async def run_search_agent_stream(query: str, user_id: str):
    initial_state = {
        "query": query,
        "retrieved_docs": [],
        "reranked_docs": [],
        "response": {},
        "user_id": user_id,
        "memory_context": "",
    }
    async for event in rag_graph.astream_events(initial_state, version="v1"):
        ...  # unchanged
```

**`src/api/v1/services/query_service.py`:**

```python
def query_documents(query: str, user_id: str):
    return run_search_agent(query, user_id)


async def query_documents_stream(query: str, user_id: str):
    return run_search_agent_stream(query, user_id)
```

**`src/api/v1/routes/query.py`:**

```python
@router.post("/")
def query_endpoint(request: QueryRequest) -> QueryResponse:
    return query_documents(request.query, request.user_id)


@router.post("/stream")
async def stream_query_endpoint(request: QueryRequest):
    generator = await query_documents_stream(request.query, request.user_id)
    return StreamingResponse(generator, media_type="text/event-stream")
```

---

## Step 9 — Test

```bash
uv run uvicorn main:app --reload
```

Teach it something:

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "I am a contract employee based in Chennai. How many leave days do I get?", "user_id": "arun"}'
```

Then ask a follow-up in a _new_ request:

```bash
curl -X POST http://localhost:8000/api/v1/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What about my notice period?", "user_id": "arun"}'
```

The logs should show `[recall_memory_node] 2 memories recalled for arun`, and the answer should account for the contract-employee fact without you repeating it.

**Leave a few seconds between the two calls.** `add()` returns `{"status": "PENDING"}` immediately and extraction finishes server-side — measured at 0.4s in one run and 4.5s in another. Back-to-back curls can show `0 memories recalled` even though the wiring is correct.

Inspect what was stored — on the **Memories** page of <https://app.mem0.ai>, or from code (note `get_all` needs `filters`, like `search`):

```python
from src.core.memory import get_memory

print(get_memory().get_all(filters={"user_id": "arun"}))
```

Reset a user between demos (`delete_all` takes `user_id` directly, and is also async):

```python
get_memory().delete_all(user_id="arun")
```

---

## Notes

- **Memory vs. checkpointer.** mem0 is long-term memory across sessions (facts). LangGraph's checkpointer is short-term memory within a thread (raw message history). Different problems; they can coexist.
- **Latency.** Both nodes are network calls to mem0. `recall_memory` is on the critical path; `save_memory` is not, and `add()` already returns in well under a second because extraction happens server-side.
- **Correctness.** Memory is user context, never a source of policy truth — the prompt in Step 6 says so explicitly. Without that line the model will happily answer from a stale memory instead of the retrieved document.
- **Async.** `AsyncMemoryClient` is a drop-in with the same methods if you want to `await` these calls inside the async streaming path.
- **Scoping.** `user_id` is the tenant boundary — memories never leak across ids. `agent_id` and `run_id` are available if you later want to scope memory per agent or per session.
- **Free tier.** The hosted platform is metered; each `add()` costs an extraction call. Fine for a course demo, worth watching in a batch run.
"""
=============================================================
  PYTHON CODING CHALLENGE
  Topic   : LangGraph · Advanced RAG · Multimodal RAG
  Level   : Intermediate → Advanced
  Tasks   : 10  (project-style, grouped by topic)
=============================================================

SETUP — install dependencies before you begin
----------------------------------------------
  pip install langgraph langchain langchain-openai
              langchain-community langchain-core
              psycopg2-binary python-dotenv numpy

ENVIRONMENT VARIABLES — create a .env file:
  OPENAI_API_KEY       = "sk-..."
  PG_CONNECTION_STRING = "postgresql+psycopg2://user:pass@localhost:5432/vectordb"

TOPIC SECTIONS
--------------
  Section A — LangGraph
  Section B — Advanced RAG
  Section C — Multimodal RAG

RULES
-----
  - Implement every function stub below.
  - Keep function signatures exactly as given.
  - Handle API errors gracefully with try/except.
  - For multimodal tasks a sample image is auto-created
    in the setup block — no external files needed.
=============================================================
"""

import os
import base64
import numpy as np
from dotenv import load_dotenv

load_dotenv()


# ─────────────────────────────────────────────────────────────
# SETUP — auto-creates a tiny sample PNG for multimodal tasks
# (already implemented — do NOT modify)
# ─────────────────────────────────────────────────────────────


def create_sample_image(path: str) -> str:
    """
    Writes a minimal valid 1x1 red pixel PNG to `path`.
    Returns the path. Used by Section C tasks.
    """
    # Minimal 1×1 red-pixel PNG (67 bytes, base64-encoded)
    PNG_B64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
        "z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
    )
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(base64.b64decode(PNG_B64))
    return path


# ─────────────────────────────────────────────────────────────
# SECTION A — LangGraph  (Tasks 1 – 4)
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# TASK 4 — LangGraph with MemorySaver (Checkpointing)
# ─────────────────────────────────────────────────────────────
"""
TASK 4: LangGraph with Checkpointing
---------------------------------------
Add MemorySaver to the ReAct graph from Task 3 (or build a
simpler chat graph) so conversations persist across invocations
using a thread_id.

Requirements:
  - Use MemorySaver as the checkpointer.
  - Simulate a 2-turn chat on the SAME thread_id:
      Turn 1: "My favourite number is 42. Remember it."
      Turn 2: "What is my favourite number multiplied by 2?"
  - The second turn should recall 42 from memory → answer 84.
  - Return both answers as a list: [answer_turn1, answer_turn2]

HINT:
  from langgraph.checkpoint.memory import MemorySaver
  memory   = MemorySaver()
  graph    = builder.compile(checkpointer=memory)
  config   = {"configurable": {"thread_id": "session-1"}}

  # Invoke with the same config both times to share state.
  result1  = graph.invoke({"messages": [HumanMessage(turn1)]}, config)
  result2  = graph.invoke({"messages": [HumanMessage(turn2)]}, config)
"""


def graph_with_checkpointing() -> list:
    """Runs a 2-turn chat graph with memory. Returns [answer1, answer2]."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# SECTION B — Advanced RAG  (Tasks 5 – 7)
# ─────────────────────────────────────────────────────────────

RAG_DOCS = [
    "LangGraph is a library for building stateful, multi-actor LLM applications using graph-based workflows.",
    "Corrective RAG (CRAG) grades retrieved documents and falls back to web search if they are irrelevant.",
    "Multi-query RAG generates several rephrased versions of a user query and merges the retrieved results.",
    "Self-RAG uses reflection tokens to decide when to retrieve, and grades its own generated output.",
    "Query rewriting improves RAG by transforming an ambiguous question into a clearer retrieval query.",
    "pgvector supports three distance metrics: L2 distance, inner product, and cosine distance.",
    "LangSmith can log every retrieval step, making it easy to debug RAG pipeline quality.",
    "Multimodal RAG extends retrieval to images by embedding image descriptions alongside text chunks.",
]


# ─────────────────────────────────────────────────────────────
# TASK 5 — Query Rewriting RAG
# ─────────────────────────────────────────────────────────────
"""
TASK 5: Query Rewriting RAG
-----------------------------
Before retrieving, rewrite the user's ambiguous query into a
clearer, more specific retrieval query.  Then run standard RAG.

Pipeline:
  original query
       ↓
  [rewrite_node]  — LLM rewrites into a better search query
       ↓
  [retrieve_node] — retrieves top-3 docs with the rewritten query
       ↓
  [answer_node]   — answers using retrieved context
       ↓
  returns {"original": str, "rewritten": str, "answer": str}

Test query:  "How does the graph thing work with memory?"

HINT:
  rewrite_prompt = ChatPromptTemplate.from_template(
      "Rewrite this query to be more specific for a technical "
      "knowledge base search. Return ONLY the rewritten query.\n"
      "Original: {query}"
  )
  # Then use the rewritten query for retrieval, not the original.
"""


def query_rewriting_rag(query: str, documents: list) -> dict:
    """Rewrites query then runs RAG. Returns original, rewritten, and answer."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 6 — Multi-Query RAG
# ─────────────────────────────────────────────────────────────
"""
TASK 6: Multi-Query RAG
-------------------------
Generate 3 different rephrasings of the user query, retrieve
documents for each, deduplicate, then generate a final answer.

Steps:
  1. Use an LLM to generate 3 query variants (return as list).
  2. Retrieve top-2 docs for EACH variant.
  3. Deduplicate by page_content (use a set).
  4. Answer with the merged unique context.
  5. Return:
     {
       "original_query"   : str,
       "generated_queries": list[str],
       "unique_doc_count" : int,
       "answer"           : str,
     }

Test query:  "What techniques improve RAG accuracy?"

HINT:
  multi_query_prompt = ChatPromptTemplate.from_template(
      "Generate 3 different search queries for this question. "
      "Return them as a numbered list (1. ... 2. ... 3. ...).\n"
      "Question: {question}"
  )
  # Parse the numbered list from the LLM output.
  # Use a set of page_content strings to deduplicate.
"""


def multi_query_rag(query: str, documents: list) -> dict:
    """Multi-query RAG with deduplication. Returns queries, doc count, answer."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 7 — Self-RAG with Document Grading
# ─────────────────────────────────────────────────────────────
"""
TASK 7: Self-RAG with Document Grading
-----------------------------------------
After retrieval, grade each document as relevant or irrelevant
to the query.  Only use relevant docs to generate the answer.
If ZERO relevant docs are found, return "I don't know."

Steps:
  1. Retrieve top-4 docs for the query.
  2. For each doc, ask the LLM: "Is this document relevant to
     answering: '{query}'? Answer YES or NO only."
  3. Keep only docs where the answer is YES.
  4. If no relevant docs → return "I don't know."
  5. Otherwise answer from the relevant docs.
  6. Return:
     {
       "query"           : str,
       "retrieved_count" : int,
       "relevant_count"  : int,
       "answer"          : str,
     }

Test with:
  query_relevant  = "What distance metrics does pgvector support?"
  query_irrelevant = "What is the capital of France?"

HINT:
  grade_prompt = ChatPromptTemplate.from_template(
      "Is the following document relevant to answering: '{query}'?\n"
      "Document: {document}\n"
      "Answer YES or NO only."
  )
"""


def self_rag_with_grading(query: str, documents: list) -> dict:
    """Grades retrieved docs for relevance before answering."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# SECTION C — Multimodal RAG  (Tasks 8 – 10)
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# TASK 10 — Multimodal RAG Query with Source Attribution
# ─────────────────────────────────────────────────────────────
"""
TASK 10: Multimodal RAG Query
-------------------------------
Query the multimodal index (built in Task 9) and return an
answer that identifies whether each source was TEXT or IMAGE.

Steps:
  1. Connect to the existing "multimodal_index" PGVector store.
  2. Retrieve top-3 most relevant documents for the query.
  3. Build context from the retrieved docs.
  4. Generate an answer using ChatOpenAI.
  5. Return:
     {
       "query"  : str,
       "answer" : str,
       "sources": [
           {"type": "text"|"image", "content": str, "score": float},
           ...
       ]
     }

Test queries:
  "What does the image show?"
  "What techniques extend RAG to images?"

HINT:
  store = PGVector(
      collection_name="multimodal_index",
      connection_string=os.environ["PG_CONNECTION_STRING"],
      embedding_function=embeddings,
  )
  results = store.similarity_search_with_score(query, k=3)
  for doc, score in results:
      source_type = doc.metadata.get("type", "text")
"""


def multimodal_rag_query(query: str) -> dict:
    """Queries the multimodal index and returns answer with source types."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# =============================================================
#  MAIN — test harness for all 10 tasks
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("LangGraph · Advanced RAG · Multimodal RAG")
    print("10-Task Coding Challenge")
    print("=" * 60)

    # Setup: sample image for Section C
    SAMPLE_IMAGE = create_sample_image("challenge_assets/sample.png")

    # ── Section A: LangGraph ─────────────────────────────────
    print("\n── SECTION A: LangGraph ───────────────────────────────\n")

    print("\n[Task 4] Graph with Checkpointing")
    r4 = graph_with_checkpointing()
    print("  Turn 1:", str(r4[0])[:80] if r4 else "")
    print("  Turn 2:", str(r4[1])[:80] if len(r4) > 1 else "")

    # ── Section B: Advanced RAG ──────────────────────────────
    print("\n── SECTION B: Advanced RAG ────────────────────────────\n")

    print("[Task 5] Query Rewriting RAG")
    r5 = query_rewriting_rag("How does the graph thing work with memory?", RAG_DOCS)
    print("  Original :", r5.get("original", "")[:60])
    print("  Rewritten:", r5.get("rewritten", "")[:60])
    print("  Answer   :", r5.get("answer", "")[:100])

    print("\n[Task 6] Multi-Query RAG")
    r6 = multi_query_rag("What techniques improve RAG accuracy?", RAG_DOCS)
    print("  Variants generated:", r6.get("generated_queries"))
    print("  Unique docs used  :", r6.get("unique_doc_count"))
    print("  Answer            :", r6.get("answer", "")[:100])

    print("\n[Task 7] Self-RAG with Grading")
    r7a = self_rag_with_grading(
        "What distance metrics does pgvector support?", RAG_DOCS
    )
    print("  [Relevant query]")
    print(
        f"  Retrieved: {r7a.get('retrieved_count')}  Relevant: {r7a.get('relevant_count')}"
    )
    print(f"  Answer: {r7a.get('answer', '')[:100]}")

    r7b = self_rag_with_grading("What is the capital of France?", RAG_DOCS)
    print("  [Irrelevant query]")
    print(
        f"  Retrieved: {r7b.get('retrieved_count')}  Relevant: {r7b.get('relevant_count')}"
    )
    print(f"  Answer: {r7b.get('answer', '')[:60]}")

    # ── Section C: Multimodal RAG ────────────────────────────
    print("\n── SECTION C: Multimodal RAG ──────────────────────────\n")

    print("\n[Task 10] Multimodal RAG Query")
    r10 = multimodal_rag_query("What techniques extend RAG to images?")
    print("  Answer  :", r10.get("answer", "")[:120])
    print("  Sources :")
    for s in r10.get("sources", []):
        print(
            f"    [{s.get('type','?').upper()}  score={s.get('score', 0):.4f}]"
            f" {s.get('content', '')[:60]}"
        )

    print("\n" + "=" * 60)
    print("All 5 tasks complete!")
    print("=" * 60)

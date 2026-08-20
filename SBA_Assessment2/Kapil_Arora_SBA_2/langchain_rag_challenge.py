"""
=============================================================
  PYTHON CODING CHALLENGE
  Topic   : LangChain v1 · RAG Agents · pgvector ·
            Embeddings · LangSmith
  Level   : Intermediate
  Tasks   : 8  (project-style, grouped by topic)
=============================================================

SETUP — install dependencies before you begin
----------------------------------------------
  pip install langchain langchain-openai langchain-community
              langchain-core langsmith psycopg2-binary numpy
              python-dotenv

ENVIRONMENT VARIABLES — create a .env file or export these:
  OPENAI_API_KEY       = "sk-..."
  LANGCHAIN_API_KEY    = "ls__..."        # LangSmith
  LANGCHAIN_TRACING_V2 = "true"
  LANGCHAIN_PROJECT    = "rag-challenge"
  PG_CONNECTION_STRING = "postgresql+psycopg2://user:pass@localhost:5432/vectordb"


RULES
-----
  - Implement every function stub below.
  - Do NOT add extra libraries beyond those listed in Setup.
  - Keep function signatures exactly as given.
  - For tasks that call an LLM, handle API errors gracefully
    with try/except.
=============================================================
"""

import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────
# TASK 1 — Basic LCEL Chain with PromptTemplate
# ─────────────────────────────────────────────────────────────
"""
TASK 1: Basic LCEL Chain
--------------------------
Build a simple LangChain Expression Language (LCEL) chain that:
  1. Accepts a topic as input.
  2. Fills it into a PromptTemplate.
  3. Sends the prompt to ChatOpenAI (gpt-4o-mini).
  4. Parses the output as a plain string.
  5. Returns the result.

Use the pipe operator  |  to chain components.

Expected usage:
  result = basic_lcel_chain("quantum computing")
  print(result)
  # "Quantum computing uses quantum bits (qubits)..."

HINT:
  from langchain_core.prompts import ChatPromptTemplate
  from langchain_openai import ChatOpenAI
  from langchain_core.output_parsers import StrOutputParser

  chain = prompt | llm | parser
  chain.invoke({"topic": "..."})
"""

def basic_lcel_chain(topic: str) -> str:
    """Returns a one-paragraph explanation of the given topic."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass  # Remove this line when you start coding

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 2 — Conversation Chain with Memory
# ─────────────────────────────────────────────────────────────
"""
TASK 2: Conversation Chain with Memory
----------------------------------------
Build a conversational chain that:
  - Maintains chat history across multiple turns.
  - Uses ChatPromptTemplate with a MessagesPlaceholder
    for the history.
  - Returns a list of (role, content) tuples representing
    the full conversation after all turns.

Simulate this 3-turn conversation:
  Turn 1 — user: "My name is Alex. What is machine learning?"
  Turn 2 — user: "Can you give me a real-world example?"
  Turn 3 — user: "What is my name?"   ← tests memory

Expected (partial):
  [("human", "My name is Alex..."),
   ("ai",    "Machine learning is..."),
   ...
   ("ai",    "Your name is Alex.")]

HINT:
  from langchain_core.chat_history import InMemoryChatMessageHistory
  from langchain_core.runnables.history import RunnableWithMessageHistory
  Use session_id to scope the history.
"""

def conversation_with_memory() -> list:
    """Runs a 3-turn conversation and returns the full message history."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 3 — Agent with Custom Tools
# ─────────────────────────────────────────────────────────────
"""
TASK 3: Agent with Custom Tools
---------------------------------
Create a LangChain agent that uses two custom tools:
  Tool 1 — word_count(text: str) → int
            Returns the number of words in a text.
  Tool 2 — reverse_text(text: str) → str
            Returns the text reversed word-by-word.

Build the agent using the @tool decorator and
create_react_agent, then run it with AgentExecutor.

Test query:
  "How many words are in 'The quick brown fox'?
   Also reverse it."

HINT:
  from langchain.agents import create_react_agent, AgentExecutor
  from langchain.tools import tool
  from langchain import hub
  prompt = hub.pull("hwchase17/react")
"""

def agent_with_tools(query: str) -> str:
    """Runs a ReAct agent with custom tools and returns the final answer."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────



# ─────────────────────────────────────────────────────────────
# TASK 4 — Generate and Inspect Embeddings
# ─────────────────────────────────────────────────────────────
"""
TASK 4: Generate and Inspect Embeddings
-----------------------------------------
Use OpenAIEmbeddings (text-embedding-3-small) to embed a list
of sentences. Return a dict with:
  {
    "num_sentences" : int,
    "embedding_dim" : int,
    "first_5_values": list[float],   # first 5 values of sentence[0]
    "vectors"       : list[list[float]]
  }

sentences = [
  "LangChain simplifies LLM application development.",
  "pgvector adds vector search to PostgreSQL.",
  "RAG grounds language models with external knowledge.",
]

HINT:
  from langchain_openai import OpenAIEmbeddings
  embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
  vectors = embeddings.embed_documents(sentences)
  A single vector is a plain Python list of floats.
"""

def generate_embeddings(sentences: list) -> dict:
    """Embeds a list of sentences and returns metadata + vectors."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# TASK 5 — Insert Document Embeddings into pgvector
# ─────────────────────────────────────────────────────────────
"""
TASK 5: Insert Document Embeddings
--------------------------------------
Given a list of (content, metadata) tuples, embed each document
using OpenAIEmbeddings and insert them into the "documents"
table created in Task 9.  Return the count of inserted rows.

documents = [
  ("LangChain enables LLM pipelines.", {"source": "docs", "page": 1}),
  ("pgvector stores vector embeddings.", {"source": "docs", "page": 2}),
  ("RAG retrieves relevant context.",   {"source": "paper", "page": 5}),
  ("LangSmith traces LLM calls.",       {"source": "blog",  "page": 1}),
]

HINT:
  import json
  vector = embeddings.embed_query(content)
  # Convert list to string for psycopg2:  str(vector)  or  json.dumps(vector)
  cursor.execute(
      "INSERT INTO documents (content, metadata, embedding) VALUES (%s, %s, %s)",
      (content, json.dumps(metadata), str(vector))
  )
"""

def insert_documents(documents: list) -> int:
    """Embeds and inserts documents. Returns count of inserted rows."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 6 — Metadata Filtering in pgvector
# ─────────────────────────────────────────────────────────────
"""
TASK 6: Metadata Filtering
------------------------------
Extend the similarity search to filter by a metadata field.
Only return documents whose metadata->>'source' matches the
given source value.

Example:
  results = filtered_search("LLM tracing", source_filter="blog", top_k=2)

HINT:
  Add a WHERE clause using JSONB operators:
  WHERE metadata->>'source' = %s
  Parameters: (vector_str, source_filter, top_k)
"""

def filtered_search(query: str, source_filter: str, top_k: int = 3) -> list:
    """Returns top-k similar docs filtered by metadata source."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 7 — Create a LangSmith Dataset
# ─────────────────────────────────────────────────────────────
"""
TASK 7: Create a LangSmith Dataset and Add Examples
------------------------------------------------------
Use the LangSmith SDK to:
  1. Create a dataset named "rag-eval-dataset".
  2. Add 3 question-answer example pairs to it.
  3. Return the dataset id as a string.

Examples to add:
  Q: "What does RAG stand for?"
     A: "Retrieval-Augmented Generation"
  Q: "What PostgreSQL extension enables vector search?"
     A: "pgvector"
  Q: "What LangChain tool provides observability?"
     A: "LangSmith"

HINT:
  from langsmith import Client
  client = Client()

  dataset = client.create_dataset("rag-eval-dataset")
  client.create_examples(
      inputs=[{"question": q} for q in questions],
      outputs=[{"answer": a} for a in answers],
      dataset_id=dataset.id
  )
"""

def create_langsmith_dataset() -> str:
    """Creates a LangSmith dataset with 3 examples. Returns dataset id."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# TASK 8 — Run an Evaluation with LangSmith
# ─────────────────────────────────────────────────────────────
"""
TASK 8: LangSmith Evaluation (evaluate)
------------------------------------------
Run an automated evaluation of your RAG pipeline using the
dataset created in Task 19.

Steps:
  1. Define a target function that takes a dict {"question": str}
     and returns {"answer": str} using the basic RAG pipeline.
  2. Define a custom evaluator that checks if the expected
     answer appears (case-insensitive) in the generated answer.
  3. Run the evaluation using langsmith.evaluate().
  4. Return the evaluation results summary dict:
     {"dataset": str, "num_examples": int, "pass_rate": float}

HINT:
  from langsmith.evaluation import evaluate, LangChainStringEvaluator

  def target(inputs: dict) -> dict:
      return {"answer": basic_rag_pipeline(RAG_DOCUMENTS, inputs["question"])}

  results = evaluate(
      target,
      data="rag-eval-dataset",
      evaluators=[...],
      experiment_prefix="rag-challenge-eval",
  )
"""

def run_langsmith_evaluation() -> dict:
    """Evaluates the RAG pipeline on the LangSmith dataset."""
    # ── YOUR CODE BELOW ──────────────────────────────────────

    pass

    # ── END OF YOUR CODE ─────────────────────────────────────


# =============================================================
#  MAIN — run and print results for each task
# =============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("LANGCHAIN · RAG · PGVECTOR · EMBEDDINGS · LANGSMITH")
    print("20-Task Coding Challenge")
    print("=" * 60)

    # ── Section A ─────────────────────────────────────────────
    print("\n── SECTION A: LangChain Core ──────────────────────────\n")

    print("[Task 1] Basic LCEL Chain")
    result = basic_lcel_chain("vector databases")
    print(result)

    print("\n[Task 2] Conversation with Memory")
    history = conversation_with_memory()
    for role, msg in history:
        print(f"  [{role.upper()}] {msg[:80]}")

    print("\n[Task 3] Agent with Custom Tools")
    ans = agent_with_tools("How many words are in 'The quick brown fox'? Also reverse it.")
    print(ans)

    # ── Section B ─────────────────────────────────────────────
    print("\n── SECTION B: Embeddings ──────────────────────────────\n")

    sentences = [
        "LangChain simplifies LLM application development.",
        "pgvector adds vector search to PostgreSQL.",
        "RAG grounds language models with external knowledge.",
    ]

    print("[Task 4] Generate Embeddings")
    emb_info = generate_embeddings(sentences)
    print(f"  Sentences : {emb_info.get('num_sentences')}")
    print(f"  Dimensions: {emb_info.get('embedding_dim')}")
    print(f"  First 5   : {emb_info.get('first_5_values')}")


   
    # ── Section C ─────────────────────────────────────────────
    print("\n── SECTION C: pgvector ────────────────────────────────\n")

    docs_to_insert = [
        ("LangChain enables LLM pipelines.", {"source": "docs", "page": 1}),
        ("pgvector stores vector embeddings.", {"source": "docs", "page": 2}),
        ("RAG retrieves relevant context.",   {"source": "paper", "page": 5}),
        ("LangSmith traces LLM calls.",       {"source": "blog",  "page": 1}),
    ]

    print("\n[Task 5] Insert Documents")
    inserted = insert_documents(docs_to_insert)
    print(f"  Rows inserted: {inserted}")

    print("\n[Task 6] Filtered Search")
    fresults = filtered_search("LLM tracing", source_filter="blog", top_k=2)
    for r in fresults:
        print(f"  [{r.get('distance', 0):.4f}] {r.get('content')}")


    # ── Section E ─────────────────────────────────────────────
    print("\n── SECTION E: LangSmith ───────────────────────────────\n")


    print("\n[Task 7] Create LangSmith Dataset")
    dataset_id = create_langsmith_dataset()
    print(f"  Dataset ID: {dataset_id}")

    print("\n[Task 8] Run LangSmith Evaluation")
    eval_summary = run_langsmith_evaluation()
    print(f"  Dataset     : {eval_summary.get('dataset')}")
    print(f"  # Examples  : {eval_summary.get('num_examples')}")
    print(f"  Pass rate   : {eval_summary.get('pass_rate')}")

    print("\n" + "=" * 60)
    print("All tasks complete!")
    print("=" * 60)

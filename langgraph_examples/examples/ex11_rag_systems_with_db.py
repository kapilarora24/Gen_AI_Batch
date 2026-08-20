from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.tools import tool
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
import psycopg
from psycopg.rows import dict_row

load_dotenv()


llm = ChatOpenAI(
    model="gpt-5.5",
)


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)


DATABASE_URL = (
    "postgresql://postgres:Pass%40123@localhost:5433/regulatory_compliance_db"
)


def get_db_connection():
    """
    PostgreSQL database connection.
    """

    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row,
    )


LONG_TERM_MEMORY = ["user prefers simple explanations"]


class AgentState(TypedDict):
    query: str
    memory: List[str]
    messages: Annotated[
        List[BaseMessage],
        add_messages,
    ]
    context: str
    answer: str
    is_good: bool
    attempts: int


@tool
def vector_search(query: str) -> str:
    """
    Search regulatory document chunks using semantic vector similarity.
    """

    print("\n VECTOR SEARCH ")
    print("Query:", query)
    query_embedding = embeddings.embed_query(query)
    embedding_string = "[" + ",".join(str(value) for value in query_embedding) + "]"
    sql = """
        SELECT
            dc.id,
            dc.document_id,
            dc.chunk_index,
            dc.content,
            dc.metadata,
            1 - (dc.embedding <=> %s::vector) AS similarity
        FROM document_chunks dc
        WHERE dc.embedding IS NOT NULL
        ORDER BY dc.embedding <=> %s::vector
        LIMIT 5;
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    embedding_string,
                    embedding_string,
                ),
            )
            rows = cursor.fetchall()

    if not rows:
        return "No relevant documents found using vector search."

    results = []

    for row in rows:
        results.append(
            {
                "document_id": str(row["document_id"]),
                "chunk_index": row["chunk_index"],
                "content": row["content"],
                "metadata": row["metadata"],
                "similarity": float(row["similarity"]),
            }
        )

    return json.dumps(
        results,
        ensure_ascii=False,
        default=str,
    )


@tool
def fts_search(query: str) -> str:
    """
    Search regulatory document chunks using PostgreSQL full-text search.
    """
    print("\n FTS SEARCH")
    print("Query:", query)
    sql = """
        SELECT
            dc.id,
            dc.document_id,
            dc.chunk_index,
            dc.content,
            dc.metadata,
            ts_rank_cd(
                to_tsvector('english', dc.content),
                plainto_tsquery('english', %s)
            ) AS rank
        FROM document_chunks dc
        WHERE to_tsvector(
            'english',
            dc.content
        ) @@ plainto_tsquery(
            'english',
            %s
        )
        ORDER BY rank DESC
        LIMIT 5;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    query,
                    query,
                ),
            )
            rows = cursor.fetchall()

    if not rows:
        return "No relevant documents found using full-text search."

    results = []

    for row in rows:
        results.append(
            {
                "document_id": str(row["document_id"]),
                "chunk_index": row["chunk_index"],
                "content": row["content"],
                "metadata": row["metadata"],
                "rank": float(row["rank"]),
            }
        )

    return json.dumps(
        results,
        ensure_ascii=False,
        default=str,
    )


@tool
def hybrid_search(query: str) -> str:
    """
    Perform hybrid search by combining semantic vector search and PostgreSQL full-text search.
    """
    print("\n HYBRID SEARCH")
    print("Query:", query)
    query_embedding = embeddings.embed_query(query)
    embedding_string = "[" + ",".join(str(value) for value in query_embedding) + "]"
    sql = """
        WITH vector_results AS
        (
            SELECT
                dc.id,
                dc.document_id,
                dc.chunk_index,
                dc.content,
                dc.metadata,
                1 - (
                    dc.embedding <=> %s::vector
                ) AS vector_score
            FROM document_chunks dc
            WHERE dc.embedding IS NOT NULL
            ORDER BY dc.embedding <=> %s::vector
            LIMIT 20
        ),
        fts_results AS
        (
            SELECT
                dc.id,
                ts_rank_cd(
                    to_tsvector('english', dc.content),
                    plainto_tsquery('english', %s)
                ) AS fts_score
            FROM document_chunks dc
            WHERE to_tsvector(
                'english',
                dc.content
            ) @@ plainto_tsquery(
                'english',
                %s
            )
            LIMIT 20
        )
        SELECT
            vr.id,
            vr.document_id,
            vr.chunk_index,
            vr.content,
            vr.metadata,
            vr.vector_score,
            COALESCE(fr.fts_score, 0) AS fts_score,
            (
                0.7 * vr.vector_score
                +
                0.3 * COALESCE(fr.fts_score, 0)
            ) AS hybrid_score
        FROM vector_results vr
        LEFT JOIN fts_results fr
            ON vr.id = fr.id
        ORDER BY hybrid_score DESC
        LIMIT 5;
    """

    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    embedding_string,
                    embedding_string,
                    query,
                    query,
                ),
            )
            rows = cursor.fetchall()

    if not rows:
        return "No relevant documents found using hybrid search."

    results = []

    for row in rows:
        results.append(
            {
                "document_id": str(row["document_id"]),
                "chunk_index": row["chunk_index"],
                "content": row["content"],
                "metadata": row["metadata"],
                "vector_score": float(row["vector_score"]),
                "fts_score": float(row["fts_score"]),
                "hybrid_score": float(row["hybrid_score"]),
            }
        )

    return json.dumps(
        results,
        ensure_ascii=False,
        default=str,
    )


TOOLS = [
    vector_search,
    fts_search,
    hybrid_search,
]


llm_with_tools = llm.bind_tools(TOOLS)


# LangGraph ToolNode
tool_node = ToolNode(TOOLS)


def retrieve_memory_node(state: AgentState):
    print("\n RETRIEVING MEMORY")
    return {"memory": LONG_TERM_MEMORY}


def agent_node(state: AgentState):
    print("\n AGENT NODE")
    memory_text = "\n".join(state["memory"])
    system_prompt = f"""
        You are a Regulatory Compliance RAG Agent.
        Your job is to answer questions ONLY using information
        retrieved from the regulatory document database.
        User preferences: {memory_text}
        You have access to these tools:
        1. vector_search
        Use for semantic/conceptual questions.
        2. fts_search
        Use for exact keywords, regulation names,
        section numbers, or specific terminology.
        3. hybrid_search
        Use when both semantic meaning and exact
        regulatory terminology are important.
        IMPORTANT RULES:
        - You MUST retrieve information before answering.
        - Do not answer from your own knowledge.
        - If the query is ambiguous, prefer hybrid_search.
        - Use the retrieved document content as the source of truth.
        - Do not invent regulatory requirements.
        - Include source/document metadata when available.
        - If no relevant information is found, clearly update that.
        """

    messages = state["messages"]
    # First agent call
    if not messages:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state["query"]),
        ]

    else:
        messages = [SystemMessage(content=system_prompt)] + messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def route_after_agent(state: AgentState):
    print("\n ROUTING AFTER AGENT")
    last_message = state["messages"][-1]
    # If LLM requested tools, execute ToolNode
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "generate"


def generate_node(state: AgentState):
    print("\n GENERATING FINAL ANSWER")
    memory_text = "\n".join(state["memory"])
    system_prompt = f"""
        You are a strict Retrieval-Augmented Generation assistant.
        User preferences:
        {memory_text}
        Answer the user's question using ONLY the retrieved
        information contained in the tool results.
        Rules:
        1. Do not use outside knowledge.
        2. Do not hallucinate.
        3. If the retrieved context does not contain the answer,
        say that the information was not found.
        4. Keep the explanation simple and clear.
        5. Cite the relevant document_id and chunk_index
        when available.
        """
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {
        "answer": response.content,
        "attempts": state["attempts"] + 1,
    }


def evaluate_node(state: AgentState):
    print("\n EVALUATING ANSWER")
    prompt = f"""
        Evaluate whether the answer is fully supported
        by the retrieved context.
        Question:
        {state["query"]}
        Answer:
        {state["answer"]}
        Return ONLY:yes or no
        Return yes if the answer is grounded in the retrieved
        documents and directly answers the question.
        Return no if the answer contains unsupported information
        or the retrieved documents do not adequately answer it.
        """

    result = llm.invoke(prompt).content.strip().lower()
    return {"is_good": result == "yes"}


def route_after_evaluation(state: AgentState):
    if state["is_good"] or state["attempts"] >= 3:
        return "END"
    return "RETRY"


workflow = StateGraph(AgentState)
workflow.add_node("memory", retrieve_memory_node)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_node("generate", generate_node)
workflow.add_node("evaluate", evaluate_node)

workflow.add_edge(START, "memory")
workflow.add_edge("memory", "agent")

workflow.add_conditional_edges(
    "agent",
    route_after_agent,
    {
        "tools": "tools",
        "generate": "generate",
    },
)

workflow.add_edge("tools", "agent")
workflow.add_edge("generate", "evaluate")

workflow.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "RETRY": "agent",
        "END": END,
    },
)

app = workflow.compile()

graph_image = app.get_graph().draw_mermaid_png()
with open(
    "examples/ex11_rag_system_with_db.png",
    "wb",
) as f:
    f.write(graph_image)

result = app.invoke(
    {
        "query": "What are the auction norms for gold loans?",
        "memory": [],
        "messages": [],
        "context": "",
        "answer": "",
        "is_good": False,
        "attempts": 0,
    }
)

print(result["answer"])

import os
from dotenv import load_dotenv
import psycopg
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def filtered_search(query: str, source_filter: str, top_k: int = 3) -> list:
    """Returns top-k similar docs filtered by metadata source."""

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        query_vector = embeddings.embed_query(query)

        vector_str = str(query_vector)

        db_url = os.getenv("PG_CONNECTION_STRING")

        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id, content, metadata
                    FROM documents
                    WHERE metadata->>'source' = %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (source_filter, vector_str, top_k),
                )

                results = cursor.fetchall()

        return results

    except Exception as exception:
        print(f"Error while performing filtered search: {exception}")
        return []


results = filtered_search("LLM tracing", source_filter="blog", top_k=2)

print(results)

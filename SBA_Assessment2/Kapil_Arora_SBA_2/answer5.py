import json
import uuid
import os
from dotenv import load_dotenv
import psycopg
from langchain_openai import OpenAIEmbeddings

load_dotenv()


def insert_documents(documents: list) -> int:
    """Embeds and inserts documents. Returns count of inserted rows."""

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        db_url = os.getenv("PG_CONNECTION_STRING")

        inserted_count = 0

        # Connect to DB
        with psycopg.connect(db_url) as conn:

            with conn.cursor() as cursor:

                for content, metadata in documents:

                    vector = embeddings.embed_query(content)
                    document_id = str(uuid.uuid4())

                    cursor.execute(
                        """
                        INSERT INTO documents
                        (id, content, metadata, embedding)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (document_id, content, json.dumps(metadata), str(vector)),
                    )

                    inserted_count += 1

                conn.commit()

        return inserted_count

    except Exception as exception:
        print(f"Error while inserting documents: {str(exception)}")
        return 0


documents = [
    ("LangChain enables LLM pipelines.", {"source": "docs", "page": 1}),
    ("pgvector stores vector embeddings.", {"source": "docs", "page": 2}),
    ("RAG retrieves relevant context.", {"source": "paper", "page": 5}),
    ("LangSmith traces LLM calls.", {"source": "blog", "page": 1}),
]

count = insert_documents(documents)

print("Inserted rows:", count)

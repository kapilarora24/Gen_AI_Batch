import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

sentences = [
    "LangChain simplifies LLM application development.",
    "pgvector adds vector search to PostgreSQL.",
    "RAG grounds language models with external knowledge.",
]


def generate_embeddings(sentences: list) -> dict:
    """Embeds a list of sentences."""

    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        vectors = embeddings.embed_documents(sentences)

        return {
            "num_sentences": len(sentences),
            "embedding_dim": len(vectors[0]) if vectors else 0,
            "first_5_values": vectors[0][:5] if vectors else [],
            "vectors": vectors,
        }

    except Exception as exception:
        return {
            "num_sentences": 0,
            "embedding_dim": 0,
            "first_5_values": [],
            "vectors": [],
            "error": f"Error while generating embeddings: {str(exception)}",
        }


result = generate_embeddings(sentences)

print("Number of sentences:", result["num_sentences"])
print("Embedding dimension:", result["embedding_dim"])
print("First 5 values:", result["first_5_values"])

# This is only for Vector Search
# build a hybrid retrieval for keyword and vector search (FTS

from app.core.db import get_vector_store


def retrive(query: str, k: int = 5):
    """gets the query and searches in the PGVector DB
    and finds top-k similar document chunks"""
    print(query)
    vector_score = get_vector_store(collection_name="hr_support_desk")
    results = vector_score.similarity_search(query, k)
    print(results)
    return results


if __name__ == "__main__":
    user_query = "how to apply off"
    retrive(user_query)

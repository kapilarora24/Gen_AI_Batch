from regulatory_compliance.retrievers.hybrid_retrievers import HybridRetriever

retriever = HybridRetriever(top_k=5)


query = "auction norms for gold loans on default"


documents = retriever.search(query)


print("\n====== HYBRID SEARCH ======\n")


for doc in documents:

    print("----------------")

    print(doc.page_content[:300])

    print(doc.metadata)

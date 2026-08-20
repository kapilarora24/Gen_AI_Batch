import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

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


llm = ChatOpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
    model=os.getenv("OPENAI_MODEL"),)


def query_rewriting_rag(query: str, documents: list) -> dict:
    """
    Rewrites query then runs RAG.
    """
    try:
        rewrite_prompt = ChatPromptTemplate.from_template(
            """
            Rewrite this query to be more specific for a technical
            knowledge base search. Return ONLY the rewritten query.
            
            Original: 
            {query}
            """
            )
        rewrite_chain = rewrite_prompt | llm
        rewrite_response = rewrite_chain.invoke({"query": query})
        rewritten_query = rewrite_response.content.strip()
        # retrieve top-3        
        query_words = set(rewritten_query.lower().split())
        scored_docs = []
        for doc in documents:
            content = (
                doc.page_content
                if hasattr(doc, "page_content")
                else str(doc)
            )
            doc_words = set(content.lower().split())
            score = len(query_words.intersection(doc_words))
            scored_docs.append((score, content))
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        top_docs = [
            content
            for score, content in scored_docs[:3]
        ]
        # generate answer
        context = "\n\n".join(top_docs)
        answer_prompt = ChatPromptTemplate.from_template(
            """
            Answer the question using ONLY the supplied context.
            If the answer is not present in the context, 
            say: "I don't know."

            Question:
            {query}

            Context:
            {context}
            """
            )
        answer_chain = answer_prompt | llm
        answer_response = answer_chain.invoke(
            {
                "query": query,
                "context": context
            }
        )
        return {
            "original": query,
            "rewritten": rewritten_query,
            "answer": answer_response.content.strip()
        }
    except Exception as error:
        print(f"RAG error: {error}")
        return {
            "original": query,
            "rewritten": "",
            "answer": "Unable to process the query."
        }

if __name__ == "__main__":
    result = query_rewriting_rag(
        "How does the graph thing work with memory?",
        RAG_DOCS
    )
    print(result)


def multi_query_rag(query: str, documents: list) -> dict:
    """
    Multi-query RAG with retries.
    """
    try:
        multi_query_prompt = ChatPromptTemplate.from_template(
            """
            Generate 3 different search queries for this question.
            Return them as list.
            Question: 
            {question}
            """
            )
        response = (multi_query_prompt | llm).invoke
        ({"question": query})
        generated_queries = []
        for line in response.content.splitlines():
            line = line.strip()
            if not line:
                continue
            if "." in line:
                prefix, text = line.split(".", 1)
                if prefix.strip().isdigit():
                    text = text.strip()
                    if text:
                        generated_queries.append(text)
        if len(generated_queries) < 3:
            generated_queries = [
                query,
                f"RAG techniques for improving accuracy: {query}",
                f"methods to improve retrieval augmented generation: {query}"
            ]
        generated_queries = generated_queries[:3]
        # retrieve top-2
        unique_docs = set()
        for generated_query in generated_queries:
            query_words = set(
                generated_query.lower().split()
            )
            scored_docs = []
            for doc in documents:
                content = (
                    doc.page_content
                    if hasattr(doc, "page_content")
                    else str(doc)
                )
                doc_words = set(content.lower().split())
                score = len(
                    query_words.intersection(doc_words)
                )
                scored_docs.append((score, content))
            scored_docs.sort(
                key=lambda x: x[0],
                reverse=True
            )
            top_two = scored_docs[:2]
            for score, content in top_two:
                unique_docs.add(content)
        # generate answer
        context = "\n\n".join(unique_docs)
        answer_prompt = ChatPromptTemplate.from_template(
            """
            Answer the question using ONLY the supplied context.
            If the answer cannot be found in the context, 
            say : "I don't know."

            Question:
            {question}

            Context:
            {context}
            """
            )
        answer_response = (answer_prompt | llm).invoke(
            {
                "question": query,
                "context": context
            }
        )
        return {
            "original_query": query,
            "generated_queries": generated_queries,
            "unique_doc_count": len(unique_docs),
            "answer": answer_response.content.strip()
        }
    except Exception as exception:
        print(f"error: {exception}")
        return {
            "original_query": query,
            "generated_queries": [],
            "unique_doc_count": 0,
            "answer": "Unable to process the query."
        }

if __name__ == "__main__":
    result = multi_query_rag(
        "What techniques improve RAG accuracy?",
        RAG_DOCS
    )
    print(result)


def self_rag_with_grading(query: str, documents: list) -> dict:
    """
    Grades retrieved docs for relevance before answering.
    """
    try:
        query_words = set(query.lower().split())
        scored_docs = []
        for doc in documents:
            content = (
                doc.page_content
                if hasattr(doc, "page_content")
                else str(doc)
            )
            doc_words = set(content.lower().split())
            score = len(
                query_words.intersection(doc_words)
            )
            scored_docs.append((score, content))
        scored_docs.sort(
            key=lambda x: x[0],
            reverse=True
        )
        retrieved_docs = [
            content
            for score, content in scored_docs[:4]
        ]
        retrieved_count = len(retrieved_docs)
        # document grade
        grade_prompt = ChatPromptTemplate.from_template(
            """
            Is the following document relevant to answering: 
            '{query}'?
            
            Document:
            {document}
            Answer YES or NO only.
            """
            )
        grade_chain = grade_prompt | llm
        relevant_docs = []
        for document in retrieved_docs:
            grade_response = grade_chain.invoke(
                {
                    "query": query,
                    "document": document
                }
            )
            grade = grade_response.content.strip().upper()
            if grade.startswith("YES"):
                relevant_docs.append(document)
        relevant_count = len(relevant_docs)
        if relevant_count == 0:
            return {
                "query": query,
                "retrieved_count": retrieved_count,
                "relevant_count": 0,
                "answer": "I don't know."
            }
        # generate answer
        context = "\n\n".join(relevant_docs)
        answer_prompt = ChatPromptTemplate.from_template(
            """
            Answer the question using ONLY the relevant documents
            provided below.
            Question:
            {query}

            Relevant documents:
            {context}
            """
            )
        answer_response = (answer_prompt | llm).invoke
        (
            {
                "query": query,
                "context": context
            }
        )
        return {
            "query": query,
            "retrieved_count": retrieved_count,
            "relevant_count": relevant_count,
            "answer": answer_response.content.strip()
        }
    except Exception as error:
        print(f"Self-RAG grading error: {error}")
        return {
            "query": query,
            "retrieved_count": 0,
            "relevant_count": 0,
            "answer": "Unable to process the query."
        }

if __name__ == "__main__":
    result= self_rag_with_grading(
        "What distance metrics does pgvector support?",
        RAG_DOCS
    )
    print(result)
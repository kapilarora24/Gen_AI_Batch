# Load the pdf froom Data folder
# extract content of the file
# Arrive at the chunking STartegy

# load the embedding model
# embed the chunks
# connect to postgress and activate pgvector extension
# save the vctor embeddings and original text in DB

# uv add python-dotenv
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

from app.core.db import get_vector_store

load_dotenv()


def ingest_pdf(filepath):
    print("Ingestion Started")

    # 1. Load the file
    loader = PyPDFLoader(filepath)
    docs = loader.load()

    # 2.  metadat enrhcment for citiation
    for doc in docs:
        doc.metadata.update(
            {
                "source": filepath,
                "document_extension": "pdf",
                "page": doc.metadata.get("page"),
                "last_updated": os.path.getmtime(filepath),
            }
        )

    print(docs)
    print("Before chunking")

    # 3. Chunking

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(docs)

    print("Total Chunk")
    print(len(chunks))

    # 4. load the model and 5. Embed the chunks
    # save it in DB
    vector_store = get_vector_store(collection_name="hr_support_desk")
    vector_store.add_documents(chunks)

    print("Ingestion Completed")


ingest_pdf("data/HR_Support_Desk_KnowledgeBase.pdf")

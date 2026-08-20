from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import os

load_dotenv()

PG_RAG_CONNECTION = os.getenv("PG_CONNECTION_STRING")
if not PG_RAG_CONNECTION:
    raise ValueError("PG_CONNECTION_STRING is not configured.")
checkpointer_context = PostgresSaver.from_conn_string(PG_RAG_CONNECTION)
checkpointer = checkpointer_context.__enter__()
checkpointer.setup()

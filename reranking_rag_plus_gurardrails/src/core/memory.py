import os
from functools import lru_cache
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()


@lru_cache(maxsize=1)
def get_memory() -> MemoryClient:
    """
    hosted mem0 client for long-term per-user memory.
    cached so we reuse one http connection pool across requests.
    """
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise ValueError("MEM0_API_KEY is not set. Check your .env")
    return MemoryClient(api_key=api_key)
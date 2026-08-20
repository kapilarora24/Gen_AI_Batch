from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: str
    success: bool = True


class Source(BaseModel):

    document_id: Optional[str] = None
    chunk_index: Optional[int] = None
    hybrid_score: Optional[float] = None


class Citation(BaseModel):

    document_id: Optional[str] = None
    file_name: Optional[str] = None
    page_number: Optional[int] = None
    section_number: Optional[str] = None
    regulation_type: Optional[str] = None
    chunk_index: Optional[int] = None
    retrieval_method: Optional[str] = None
    vector_score: Optional[float] = None
    fts_score: Optional[float] = None
    hybrid_score: Optional[float] = None
    snippet: Optional[str] = None


class QueryResponse(BaseModel):

    answer: str
    query_type: Optional[str] = None
    tool_used: Optional[str] = None
    confidence: Optional[float] = None
    latency_ms: Optional[float] = None
    sources: List[Citation] = []

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class RetrievalFilter(BaseModel):
    document_ids: Optional[List[str]] = Field(
        None, 
        description="Optional list of document IDs to filter search results within the course"
    )

class RetrievalRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query string")
    top_k: int = Field(5, ge=1, le=50, description="Number of top relevant chunks to retrieve")
    filters: Optional[RetrievalFilter] = Field(None, description="Document level filters")

class ChunkProvenance(BaseModel):
    chunk_id: str
    document_id: str
    page_number: Optional[int] = None
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)

class RetrievalResultItem(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    score: float
    provenance: ChunkProvenance

class RetrievalResponse(BaseModel):
    course_id: str
    query: str
    total_results: int
    results: List[RetrievalResultItem]

    model_config = ConfigDict(from_attributes=True)
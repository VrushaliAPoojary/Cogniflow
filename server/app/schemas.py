from pydantic import BaseModel
from typing import Optional

class DocumentCreate(BaseModel):
    filename: str
    path: str
    content_summary: Optional[str] = None

class DocumentOut(DocumentCreate):
    id: int
    created_at: str

    class Config:
        orm_mode = True

class QueryRequest(BaseModel):
    query: str
    use_kb: bool = True
    workflow_id: Optional[str] = None

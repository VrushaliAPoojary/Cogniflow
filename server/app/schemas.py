# server/app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    filename: str
    path: str
    content_summary: Optional[str] = None

class DocumentOut(DocumentCreate):
    id: int
    created_at: datetime   # use proper datetime instead of str

    class Config:
        from_attributes = True  # ✅ updated for Pydantic v2

class QueryRequest(BaseModel):
    query: str
    use_kb: bool = True
    workflow_id: Optional[str] = None

from fastapi import APIRouter, Depends
from ..schemas import QueryRequest
from ..services.workflow_runner import run_query_pipeline

router = APIRouter(prefix="/api", tags=["api"])

@router.post("/query")
async def query(req: QueryRequest):
    out = run_query_pipeline(req.query, use_kb=req.use_kb)
    return out

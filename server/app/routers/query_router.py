from fastapi import APIRouter
from ..schemas import QueryRequest
from ..services.workflow_runner import run_query_pipeline

router = APIRouter()

@router.post("/query")
def query(req: QueryRequest):
    """
    Endpoint for running a query through the workflow.
    Request body: { "query": "your text", "use_kb": true }
    """
    out = run_query_pipeline(req.query, use_kb=req.use_kb)
    return out

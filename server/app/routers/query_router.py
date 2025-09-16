# server/app/routers/query_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from ..services.workflow_runner import run_workflow

router = APIRouter(prefix="/api", tags=["Queries"])

class QueryRequest(BaseModel):
    query: str
    use_kb: bool = True
    workflow: dict | None = None

@router.post("/query")
def query(req: QueryRequest):
    # if workflow provided, run it; otherwise use built-in default pipeline
    if req.workflow:
        return run_workflow(req.workflow, input_query=req.query)
    else:
        # default small pipeline: run kb -> llm
        wf = {
            "nodes": [
                {"id":"user", "type":"input", "data":{"label":"User"}},
                {"id":"kb", "data":{"label":"KnowledgeBase"}},
                {"id":"llm", "data":{"label":"LLM Engine"}},
                {"id":"out", "type":"output", "data":{"label":"Output"}},
            ],
            "edges": [
                {"id":"e1","source":"user","target":"kb"},
                {"id":"e2","source":"kb","target":"llm"},
                {"id":"e3","source":"llm","target":"out"},
            ]
        }
        return run_workflow(wf, input_query=req.query)

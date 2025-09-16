# server/app/routers/workflows_router.py
from fastapi import APIRouter, HTTPException
import os, json, uuid

from ..services.workflow_runner import run_workflow

router = APIRouter(prefix="/workflows", tags=["Workflows"])

SAVE_DIR = "./data/workflows"
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/save")
def save_workflow(workflow: dict):
    uid = str(uuid.uuid4())
    path = os.path.join(SAVE_DIR, f"{uid}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(workflow, f, indent=2)
    return {"status": "saved", "id": uid, "path": path}

@router.post("/run")
def run_saved_workflow(payload: dict):
    """
    payload: {
      workflow: { nodes: [...], edges: [...] },
      query: "user text"
    }
    """
    workflow = payload.get("workflow")
    query = payload.get("query","")
    if not workflow:
        raise HTTPException(status_code=400, detail="workflow required")
    out = run_workflow(workflow, input_query=query)
    return out

# server/app/routers/chat_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ..services.workflow_runner import run_query_pipeline
from ..services.pdf_processor import extract_text_from_pdf
from ..services.embeddings import create_embeddings_for_text
import os, uuid, shutil

router = APIRouter(prefix="/chat", tags=["Chat"])

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/query")
async def chat_query(query: str = Form(...), use_kb: bool = Form(True)):
    """
    Form-encoded POST used by frontend: query + use_kb flag.
    """
    out = run_query_pipeline(query, use_kb=use_kb, use_web=True)
    return out

@router.post("/upload")
async def chat_upload(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF supported")
    uid = str(uuid.uuid4())
    filename = f"{uid}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = extract_text_from_pdf(path)
    # chunk & embed as in docs upload
    max_chunk = 1500
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    ids = [f"{uid}_{i}" for i in range(len(chunks))]
    metadatas = [{"filename": file.filename, "chunk_index": i} for i in range(len(chunks))]

    create_embeddings_for_text(chunks, metadatas, ids)
    return {"status": "uploaded", "filename": file.filename}

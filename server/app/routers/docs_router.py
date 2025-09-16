# server/app/routers/docs_router.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, uuid, shutil
from sqlalchemy.orm import Session
from ..services.pdf_processor import extract_text_from_pdf
from ..services.embeddings import create_embeddings_for_text
from .. import crud, schemas
from ..db import get_db

router = APIRouter(prefix="/docs", tags=["Documents"])

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=schemas.DocumentOut)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    uid = str(uuid.uuid4())
    filename = f"{uid}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text_from_pdf(path)
    if not text:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
    chunks = [text[i:i+2000] for i in range(0,len(text),2000)]
    ids = [f"{uid}_{i}" for i in range(len(chunks))]
    metadatas = [{"filename": file.filename} for _ in chunks]
    create_embeddings_for_text(chunks, metadatas, ids)
    doc_in = schemas.DocumentCreate(filename=file.filename, path=path, content_summary=(text[:200]+"..."))
    doc = crud.create_document(db, doc_in)
    return doc

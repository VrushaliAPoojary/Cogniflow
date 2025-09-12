from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, uuid
from ..services.pdf_processor import extract_text_from_pdf
from ..services.embeddings import create_embeddings_for_text
from .. import crud, schemas
from ..db import get_db
from sqlalchemy.orm import Session
from ..config import settings

router = APIRouter(prefix="/docs", tags=["documents"])

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=schemas.DocumentOut)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save file
    ext = os.path.splitext(file.filename)[1]
    uid = str(uuid.uuid4())
    filename = f"{uid}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text_from_pdf(path)
    # Simple split into chunks (naive)
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    ids = [f"{uid}_{i}" for i in range(len(chunks))]
    metadatas = [{"filename": file.filename} for _ in chunks]

    # Create embeddings and store in Chroma
    create_embeddings_for_text(chunks, metadatas, ids)

    doc_in = schemas.DocumentCreate(filename=file.filename, path=path, content_summary=(text[:200] + "...") if text else "")
    doc = crud.create_document(db, doc_in)
    return doc

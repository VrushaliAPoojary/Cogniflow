from sqlalchemy.orm import Session
from . import models, schemas

def create_document(db: Session, doc_in: schemas.DocumentCreate):
    db_doc = models.Document(filename=doc_in.filename, path=doc_in.path, content_summary=doc_in.content_summary)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def get_document(db: Session, doc_id: int):
    return db.query(models.Document).filter(models.Document.id == doc_id).first()

def list_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

# server/app/services/embeddings.py
import logging
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from ..config import settings

# initialize model (local)
EMBED_MODEL = settings.LOCAL_EMBED_MODEL
try:
    model = SentenceTransformer(EMBED_MODEL)  # local model
except Exception as e:
    logging.error("Failed to load sentence-transformer model: %s", e)
    model = None

# chroma persistent client
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
COL_NAME = "documents"

def get_or_create_collection():
    try:
        return chroma_client.get_collection(COL_NAME)
    except Exception:
        return chroma_client.create_collection(COL_NAME)

def create_embeddings_for_text(texts, metadatas, ids):
    if not model:
        raise RuntimeError("Embedding model not initialized")
    vectors = model.encode(texts, convert_to_numpy=True).tolist()
    col = get_or_create_collection()
    col.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=vectors)
    return True

def query_similar(query, k=3):
    if not model:
        return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    qvec = model.encode([query], convert_to_numpy=True).tolist()[0]
    col = get_or_create_collection()
    results = col.query(query_embeddings=[qvec], n_results=k, include=["documents","metadatas","distances"])
    return results

import os
from typing import List, Optional
from ..config import settings
import openai
import chromadb
from chromadb.config import Settings as ChromaSettings

openai.api_key = settings.OPENAI_API_KEY

# create chroma client (local persistence)
chroma_client = chromadb.Client(ChromaSettings(chroma_db_impl="duckdb+parquet", persist_directory=settings.CHROMA_PERSIST_DIR))

# collection name
COL_NAME = "documents"

def get_or_create_collection():
    try:
        col = chroma_client.get_collection(COL_NAME)
    except Exception:
        col = chroma_client.create_collection(COL_NAME)
    return col

def create_embeddings_for_text(texts: List[str], metadatas: List[dict], ids: List[str]):
    # using OpenAI embeddings API
    res = openai.Embedding.create(model="text-embedding-3-small", input=texts)
    vectors = [r["embedding"] for r in res["data"]]
    col = get_or_create_collection()
    col.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=vectors)
    chroma_client.persist()
    return True

def query_similar(query: str, k: int = 3):
    res = openai.Embedding.create(model="text-embedding-3-small", input=[query])
    qvec = res["data"][0]["embedding"]
    col = get_or_create_collection()
    results = col.query(query_embeddings=[qvec], n_results=k, include=["metadatas", "documents", "distances"])
    return results

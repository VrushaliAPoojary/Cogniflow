# server/app/services/embeddings.py
import openai
import chromadb
from ..config import settings

openai.api_key = settings.OPENAI_API_KEY

# ✅ Use PersistentClient with path
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

COL_NAME = "documents"

def get_or_create_collection():
    try:
        col = chroma_client.get_collection(COL_NAME)
    except:
        col = chroma_client.create_collection(COL_NAME)
    return col

def create_embeddings_for_text(texts, metadatas, ids):
    res = openai.Embedding.create(model="text-embedding-3-small", input=texts)
    vectors = [r["embedding"] for r in res["data"]]
    col = get_or_create_collection()
    col.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=vectors)
    return True

def query_similar(query, k=3):
    res = openai.Embedding.create(model="text-embedding-3-small", input=[query])
    qvec = res["data"][0]["embedding"]
    col = get_or_create_collection()
    results = col.query(query_embeddings=[qvec], n_results=k, include=["metadatas", "documents", "distances"])
    return results

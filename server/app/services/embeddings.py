# server/app/services/embeddings.py
import chromadb
from sentence_transformers import SentenceTransformer
from ..config import settings

# ✅ Load local embedding model (fast + small, no API needed)
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Persistent Chroma client
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

COL_NAME = "documents"

def get_or_create_collection():
    """Get or create a Chroma collection for documents"""
    try:
        col = chroma_client.get_collection(COL_NAME)
    except:
        col = chroma_client.create_collection(COL_NAME)
    return col

def create_embeddings_for_text(texts, metadatas, ids):
    """Generate embeddings locally and store them in ChromaDB"""
    vectors = model.encode(texts, convert_to_numpy=True).tolist()
    col = get_or_create_collection()
    col.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=vectors)
    return True

def query_similar(query, k=3):
    """Find k most similar docs in ChromaDB for a query"""
    qvec = model.encode([query], convert_to_numpy=True).tolist()[0]
    col = get_or_create_collection()
    results = col.query(
        query_embeddings=[qvec],
        n_results=k,
        include=["metadatas", "documents", "distances"]
    )
    return results

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from .routers import docs_router, query_router, workflows_router

# Create database tables (in production use Alembic migrations)
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Workflow Stack API",
    description="API for document workflows, embeddings, and LLM queries",
    version="1.0.0",
)

# Enable CORS so frontend can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ⚠️ in production restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefixes
app.include_router(docs_router.router, prefix="/docs", tags=["Documents"])
app.include_router(query_router.router, prefix="/api", tags=["Queries"])
app.include_router(workflows_router.router, prefix="/workflows", tags=["Workflows"])

# Root endpoint
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Workflow Stack API is running 🚀"}

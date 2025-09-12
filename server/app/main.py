from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from .routers import docs_router, query_router, workflows_router
import os

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workflow Stack API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# include routers
app.include_router(docs_router.router)
app.include_router(query_router.router)
app.include_router(workflows_router.router)

@app.get("/")
def read_root():
    return {"status": "ok"}

# server/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from .routers import docs_router, query_router, workflows_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workflow Stack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs_router.router)
app.include_router(query_router.router)
app.include_router(workflows_router.router)

@app.get("/")
def root():
    return {"status":"ok", "message":"Workflow Stack API running"}

# server/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .db import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)  # limit length for safety
    content_summary = Column(Text, nullable=True)
    path = Column(String(500), nullable=False)  # allow longer paths
    created_at = Column(DateTime(timezone=True), server_default=func.now())

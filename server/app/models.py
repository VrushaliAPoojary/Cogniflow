from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .db import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_summary = Column(Text)
    path = Column(String, nullable=False)  # storage path
    created_at = Column(DateTime, server_default=func.now())

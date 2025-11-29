from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class DocumentType(str, Enum):
    """Supported document types"""
    MARKDOWN = "md"
    TEXT = "txt"
    JSON = "json"
    PDF = "pdf"
    HTML = "html"


class DocumentUploadResponse(BaseModel):
    """Response after document upload"""
    success: bool
    message: str
    document_count: int
    chunks_created: int


class KnowledgeBaseStatus(BaseModel):
    """Status of the knowledge base"""
    is_built: bool
    document_count: int
    total_chunks: int
    collection_exists: bool


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    qdrant_connected: bool
    ollama_available: bool
    embedding_model_loaded: bool
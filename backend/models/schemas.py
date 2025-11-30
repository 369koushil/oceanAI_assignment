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
    
class TestCase(BaseModel):
    """Individual test case model"""
    test_id: str = Field(..., description="Unique test case identifier")
    feature: str = Field(..., description="Feature being tested")
    test_scenario: str = Field(..., description="Detailed test scenario")
    test_type: str = Field(..., description="Type: positive/negative/edge-case")
    preconditions: Optional[str] = Field(None, description="Pre-conditions for test")
    test_steps: List[str] = Field(..., description="Step-by-step test execution")
    expected_result: str = Field(..., description="Expected outcome")
    grounded_in: str = Field(..., description="Source document reference")
    priority: Optional[str] = Field("Medium", description="Priority: High/Medium/Low")


class TestCaseGenerationRequest(BaseModel):
    """Request to generate test cases"""
    query: str = Field(..., description="User query for test case generation")
    max_test_cases: Optional[int] = Field(10, description="Maximum test cases to generate")


class TestCaseGenerationResponse(BaseModel):
    """Response with generated test cases"""
    success: bool
    test_cases: List[TestCase]
    total_generated: int
    sources_used: List[str]


class SeleniumScriptRequest(BaseModel):
    """Request to generate Selenium script"""
    test_case: TestCase
    html_content: str


class SeleniumScriptResponse(BaseModel):
    """Response with generated Selenium script"""
    success: bool
    script: str
    test_case_id: str
    language: str = "python"
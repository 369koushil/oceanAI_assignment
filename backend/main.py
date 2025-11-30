from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from loguru import logger
import os
from dotenv import load_dotenv

# services
from backend.services.document_processor import document_processor
from backend.services.vector_store import vector_store_service
from backend.services.embeddings import embedding_service
from backend.services.test_case_generator import test_case_generator
from backend.services.selenium_generator import selenium_generator

# models
from backend.models.schemas import (
    DocumentUploadResponse,
    KnowledgeBaseStatus,
    TestCaseGenerationRequest,
    TestCaseGenerationResponse,
    SeleniumScriptRequest,
    SeleniumScriptResponse,
    HealthCheck
)

load_dotenv()

BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("logs/app.log", rotation="500 MB", retention="10 days")

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous QA Agent API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for HTML content
html_content_store = {"checkout_html": ""}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Autonomous QA Agent API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint to verify all services"""
    try:
        # Check Qdrant connection
        qdrant_connected = vector_store_service.health_check()
        
        # Check Ollama
        LLM_available = True
        
        # Check embedding model
        embedding_model_loaded = embedding_service.embeddings is not None
        
        return HealthCheck(
            status="healthy" if all([qdrant_connected, LLM_available, embedding_model_loaded]) else "degraded",
            qdrant_connected=qdrant_connected,
            LLM_available=LLM_available,
            embedding_model_loaded=embedding_model_loaded
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-documents", response_model=DocumentUploadResponse)
async def upload_documents(
    files: List[UploadFile] = File(...)
):
    try:
        logger.info(f"Received {len(files)} files for upload")
        
        documents = []
        
        for file in files:
            content = await file.read()
            
            filename = file.filename
            file_extension = filename.split('.')[-1].lower()
            
            if file_extension in ['md', 'txt', 'html', 'json']:
                content = content.decode('utf-8')
            
            documents.append({
                'content': content,
                'filename': filename,
                'file_type': file_extension
            })
        
        chunks = document_processor.process_multiple_documents(documents)
        
        chunks_stored = vector_store_service.add_documents(chunks)
        
        logger.info(f"Successfully processed {len(documents)} documents into {chunks_stored} chunks")
        
        return DocumentUploadResponse(
            success=True,
            message=f"Successfully processed {len(documents)} documents",
            document_count=len(documents),
            chunks_created=chunks_stored
        )
        
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-html")
async def upload_html(
    file: UploadFile = File(...)
):
    try:
        logger.info(f"Received HTML file: {file.filename}")
        
        content = await file.read()
        html_content = content.decode('utf-8')
        
        html_content_store["checkout_html"] = html_content
        
        chunks = document_processor.process_document(
            content=html_content,
            filename=file.filename,
            file_type='html'
        )
        
        vector_store_service.add_documents(chunks)
        
        logger.info(f"Successfully stored HTML file: {file.filename}")
        
        return {
            "success": True,
            "message": f"HTML file {file.filename} uploaded successfully",
            "chunks_created": len(chunks)
        }
        
    except Exception as e:
        logger.error(f"Error uploading HTML: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-base/status", response_model=KnowledgeBaseStatus)
async def get_knowledge_base_status():
    """Get status of the knowledge base"""
    try:
        collection_info = vector_store_service.get_collection_info()
        
        return KnowledgeBaseStatus(
            is_built=collection_info.get("exists", False) and collection_info.get("points_count", 0) > 0,
            document_count=collection_info.get("points_count", 0),
            total_chunks=collection_info.get("vectors_count", 0),
            collection_exists=collection_info.get("exists", False)
        )
    except Exception as e:
        logger.error(f"Error getting knowledge base status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-test-cases", response_model=TestCaseGenerationResponse)
async def generate_test_cases(request: TestCaseGenerationRequest):
    try:
        logger.info(f"Generating test cases for query: {request.query}")
        
        result = test_case_generator.generate_test_cases(
            query=request.query,
            max_results=request.max_test_cases
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to generate test cases"))
        
        return TestCaseGenerationResponse(
            success=True,
            test_cases=result["test_cases"],
            total_generated=result["total_generated"],
            sources_used=result["sources_used"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating test cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-selenium-script", response_model=SeleniumScriptResponse)
async def generate_selenium_script(request: SeleniumScriptRequest):
    try:
        logger.info(f"Generating Selenium script for test case: {request.test_case.test_id}")
        
        html_content = request.html_content or html_content_store.get("checkout_html", "")
        
        if not html_content:
            raise HTTPException(
                status_code=400,
                detail="No HTML content available. Please upload checkout.html first."
            )
        
        result = selenium_generator.generate_script(
            test_case=request.test_case,
            html_content=html_content
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to generate script"))
        
        return SeleniumScriptResponse(
            success=True,
            script=result["script"],
            test_case_id=result["test_case_id"],
            language="python"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating Selenium script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/knowledge-base/reset")
async def reset_knowledge_base():
    try:
        vector_store_service.delete_collection()
        html_content_store["checkout_html"] = ""
        
        logger.info("Knowledge base reset successfully")
        
        return {
            "success": True,
            "message": "Knowledge base reset successfully"
        }
    except Exception as e:
        logger.error(f"Error resetting knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/test-rag")
async def test_rag(query: str):
    try:
        results = vector_store_service.similarity_search(
            query=query,
            k=5
        )
        
        return {
            "query": query,
            "results_found": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error testing RAG: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
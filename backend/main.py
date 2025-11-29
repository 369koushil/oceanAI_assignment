from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import logging
from loguru import logger

# services
from backend.services.document_processor import document_processor
from backend.services.vector_store import vector_store_service
from backend.services.embeddings import embedding_service

# models
from backend.models.schemas import (
    DocumentUploadResponse,
    KnowledgeBaseStatus,
    HealthCheck
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("logs/app.log", rotation="500 MB", retention="10 days")

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous QA Agent API",
    description="AI-powered test case and Selenium script generation",
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
        llm_available = True
        
        # Check embedding model
        embedding_model_loaded = embedding_service.embeddings is not None
        
        return HealthCheck(
            status="healthy" if all([qdrant_connected, llm_available, embedding_model_loaded]) else "degraded",
            qdrant_connected=qdrant_connected,
            llm_available=llm_available,
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



if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Autonomous QA Agent API...")
    logger.info(f"Qdrant URL: {settings.qdrant_url}")
    logger.info(f"Model: {settings.ollama_model}")
    
    uvicorn.run(
        "backend.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True
    )
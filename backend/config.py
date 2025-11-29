from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Qdrant Cloud Configuration
    qdrant_url: str = "https://9d1bba16-8d90-425e-bcae-e7c1f172b312.us-east-1-1.aws.cloud.qdrant.io"
    qdrant_api_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.x5JZbkUvtJXajJ0Wm2E5bVHJvS82SsvVJ139nF6AfO4"
    qdrant_collection_name: str = "qa_agent_knowledge_base"
    
    
    # HuggingFace Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # FastAPI Configuration
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    

    
    # Chunking Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200

    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
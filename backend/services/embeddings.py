from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import settings
from typing import List
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    
    def __init__(self):
        self.model_name = settings.embedding_model
        self.embeddings = None
        self._initialize_model()
    
    def _initialize_model(self):
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            
            logger.info("Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_embedding_dimension(self) -> int:
        return settings.embedding_dimension


# Global embedding service instance
embedding_service = EmbeddingService()
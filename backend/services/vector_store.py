from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_core.documents import Document
from backend.services.embeddings import embedding_service
from typing import List, Dict, Any
import logging
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "qa_agent_knowledge_base")


logger = logging.getLogger(__name__)

class VectorStoreService:
    
    def __init__(self):
        self.client = None
        self.collection_name = QDRANT_COLLECTION_NAME
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            logger.info(f"Connecting to Qdrant Cloud: {QDRANT_URL}")
            
            self.client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
            )
            
            # Test connection
            collections = self.client.get_collections()
            logger.info(f"Connected to Qdrant. Collections: {collections}")
            
        except Exception as e:
            logger.error(f"Error connecting to Qdrant: {str(e)}")
            raise
    
    def create_collection(self):
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return
            
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=embedding_service.get_embedding_dimension(),
                    distance=Distance.COSINE
                )
            )
            
            logger.info(f"Created collection '{self.collection_name}'")
            
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> int:
        try:
            if not documents:
                return 0
            
            self.create_collection()
            
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            
            logger.info(f"Generating embeddings for {len(texts)} documents...")
            embeddings = embedding_service.embed_documents(texts)
            
            points = []
            for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": text,
                        "source": metadata.get("source", "unknown"),
                        "file_type": metadata.get("file_type", "unknown"),
                        "chunk_index": metadata.get("chunk_index", 0),
                        "total_chunks": metadata.get("total_chunks", 1)
                    }
                )
                points.append(point)
            
            logger.info(f"Uploading {len(points)} points to Qdrant...")
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Successfully added {len(points)} documents to vector store")
            return len(points)
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 5,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        
        try:
            query_embedding = embedding_service.embed_text(query)
            
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=k,
                score_threshold=score_threshold
            )
            
            results = []
            for result in search_results:
                results.append({
                    "text": result.payload.get("text", ""),
                    "source": result.payload.get("source", "unknown"),
                    "file_type": result.payload.get("file_type", "unknown"),
                    "chunk_index": result.payload.get("chunk_index", 0),
                    "score": result.score,
                    "metadata": result.payload
                })
            
            logger.info(f"Found {len(results)} similar documents for query")
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "exists": True,
                "vectors_count": collection_info.vectors_count,
                "points_count": collection_info.points_count,
                "status": collection_info.status
            }
        except Exception as e:
            logger.warning(f"Collection info error: {str(e)}")
            return {
                "exists": False,
                "vectors_count": 0,
                "points_count": 0
            }
    
    def delete_collection(self):
        """Delete the collection (useful for testing/reset)"""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise
    
    def health_check(self) -> bool:
        """Check if Qdrant is accessible"""
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False


# Global vector store service instance
vector_store_service = VectorStoreService()
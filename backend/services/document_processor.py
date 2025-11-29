from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Any
import json
import markdown
from bs4 import BeautifulSoup
import pymupdf
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def process_document(self, content: str, filename: str, file_type: str) -> List[Document]:
        
        try:
            if file_type == "md":
                text = self._process_markdown(content)
            elif file_type == "txt":
                text = content
            elif file_type == "json":
                text = self._process_json(content)
            elif file_type == "pdf":
                text = self._process_pdf(content)
            elif file_type == "html":
                text = self._process_html(content)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            doc = Document(
                page_content=text,
                metadata={
                    "source": filename,
                    "file_type": file_type
                }
            )
            
            chunks = self.text_splitter.split_documents([doc])
            
            for idx, chunk in enumerate(chunks):
                chunk.metadata["chunk_index"] = idx
                chunk.metadata["total_chunks"] = len(chunks)
            
            logger.info(f"Processed {filename}: {len(chunks)} chunks created")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing document {filename}: {str(e)}")
            raise
    
    def _process_markdown(self, content: str) -> str:
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator='\n', strip=True)
    
    def _process_json(self, content: str) -> str:
        try:
            data = json.loads(content)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            return content
    
    def _process_pdf(self, content: bytes) -> str:
        try:
            doc = pymupdf.open(stream=content, filetype="pdf")
            text_parts = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text_parts.append(page.get_text())
            
            doc.close()
            return "\n\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
    
    def _process_html(self, content: str) -> str:
        """Extract text from HTML"""
        soup = BeautifulSoup(content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator='\n', strip=True)
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def process_multiple_documents(
        self, 
        documents: List[Dict[str, Any]]
    ) -> List[Document]:
        all_chunks = []
        
        for doc in documents:
            chunks = self.process_document(
                content=doc['content'],
                filename=doc['filename'],
                file_type=doc['file_type']
            )
            all_chunks.extend(chunks)
        
        logger.info(f"Processed {len(documents)} documents: {len(all_chunks)} total chunks")
        return all_chunks


# Global document processor instance
document_processor = DocumentProcessor()
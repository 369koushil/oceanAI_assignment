
# 🤖 Autonomous QA Agent

An intelligent, AI-powered QA automation system that generates comprehensive test cases and executable Selenium scripts from project documentation using **Retrieval Augmented Generation (RAG)**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.122.0-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 🎥 Demo Video
Watch the complete working demonstration of the Autonomous QA Agent:

<video src="https://github.com/user-attachments/assets/56d0847e-dad7-41d7-8997-f227ded94c90" controls width="100%" style="max-width: 900px;">
  Your browser does not support the video tag.
</video>

---

## 📋 Table of Contents
- Overview  
- Demo Video  
- Architecture  
- Features  
- Tech Stack  
- System Requirements  
- Project Structure  
- Installation  
- Configuration  
- Usage  
- How It Works  
- API Documentation  
- Testing  
- Deployment  
- Limitations  
- Future Enhancements  
- Author  
- Support  

---

## 🎯 Overview
This system automates the QA testing workflow through:

1. Ingesting and parsing documentation  
2. Creating a vector-based knowledge base using Qdrant  
3. Generating grounded test cases using RAG  
4. Creating executable Selenium Python scripts  

---

## 🏗️ Architecture

### High-Level Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│                     (Streamlit Frontend)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                           │
│   ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│   │ Document       │  │   Test Case    │  │  Selenium Script │   │
│   │ Processor      │  │   Generator    │  │    Generator     │   │
│   └────────────────┘  └────────────────┘  └──────────────────┘   │
└─────────┬──────────────────────┬──────────────────────┬──────────┘
          │                      │                      │
          ▼                      ▼                      ▼
   ┌─────────────┐      ┌─────────────┐        ┌─────────────┐
   │ HuggingFace │      │   Qdrant     │        │   OpenAI     │
   │ Embeddings  │      │ Vector Store │        │ GPT-4o-mini  │
   └─────────────┘      └─────────────┘        └─────────────┘
```

---

## ✨ Features
- Multi-document ingestion  
- Vector-based semantic search  
- Grounded test case generation  
- Automatic Selenium script creation  
- HTML element parsing for selectors  
- Real-time validation  
- Clean modular backend  

---

## 🛠️ Tech Stack

### Backend
- FastAPI  
- Qdrant Cloud  
- HuggingFace Embeddings  
- OpenAI GPT‑4o‑mini  
- LangChain Orchestration  
- Pydantic v2  

### Frontend
- Streamlit  
- Requests  

### File Processing
- PyMuPDF  
- BeautifulSoup4  
- python-markdown  

---

## 💻 System Requirements
- Python 3.10+  
- Minimum 4GB RAM  
- Stable Internet  
- OpenAI API key  
- Qdrant Cloud instance  

---

## 📁 Project Structure
```
autonomous-qa-agent/
│
├── backend/
│   ├── main.py
│   ├── services/
│   │   ├── document_processor.py       # Parses MD, PDF, TXT, JSON, HTML
│   │   ├── embeddings.py               # Generates HuggingFace embeddings
│   │   ├── vector_store.py             # Qdrant operations
│   │   ├── llm_service.py              # OpenAI service wrapper
│   │   ├── test_case_generator.py      # RAG-based generation
│   │   └── selenium_generator.py       # Selenium Python generator
│   ├── models/
│   │   └── schemas.py
│   └── utils/
│       └── helpers.py
│
├── frontend/
│   └── app.py                          # Streamlit UI
│
├── project_assets/
│   ├── checkout.html
│   ├── product_specs.md
│   ├── ui_ux_guide.txt
│   ├── api_endpoints.json
│   └── test_scenarios.md
│
├── tests/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Installation

### Clone Repo
```bash
git clone <your-repo-url>
cd autonomous-qa-agent
```

### Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Create `.env`
```bash
cp .env.example .env
```

Fill environment variables:
```env
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=qa_agent_knowledge_base

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

---

## 📖 Usage

### Run From Project Root

#### Backend
```bash
uvicorn backend.main:app --reload
```

#### Frontend
```bash
streamlit run frontend/app.py
```

### Workflow
1. Upload documents  
2. Upload target HTML  
3. Build knowledge base  
4. Generate test cases  
5. Generate Selenium scripts  

---

## 🔄 How It Works

### Document Pipeline
1. Extract text  
2. Chunk using RecursiveCharacterTextSplitter  
3. Embed using MiniLM  
4. Store vectors in Qdrant  

### Test Case Generation
1. User query → embedding  
2. Similarity search  
3. Retrieve context  
4. GPT‑4o‑mini generates grounded test cases  

### Selenium Script Generation
1. HTML parsing  
2. Identify selectors  
3. Inject context  
4. Generate optimized Python Selenium script  

---

## 📚 API Documentation

### Health Check
```http
GET /health
```

### Upload Documents
```http
POST /api/upload-documents
```

### Generate Test Cases
```http
POST /api/generate-test-cases
```

### Generate Selenium Script
```http
POST /api/generate-selenium-script
```

---

## 🧪 Testing
```
pytest tests/ -v
```

---

## 🚢 Deployment (No Docker Needed)

Run manually:

### Backend
```bash
uvicorn backend.main:app --reload
```

### Frontend
```bash
streamlit run frontend/app.py
```

---

## ⚠️ Limitations
- Requires cloud APIs  
- Limited to English  
- Minor script adjustments may be needed  

---

## 🔮 Future Enhancements
- Multi-LLM backend  
- API test automation  
- Mobile automation  
- Integrated test runner  
- CI/CD plugins  

---

## 👤 Author  
**Koushil**  
Generative AI Developer  
Email: **koushil463@gmail.com**

---

## 📞 Support  
- Review documentation  
- Use `/docs`  
- Open GitHub issues  

---

_Last Updated: December 2025_

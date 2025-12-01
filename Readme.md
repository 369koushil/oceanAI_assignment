
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
- Installation  
- Configuration  
- Usage  
- Project Structure  
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

1. **Document ingestion** — MD, TXT, JSON, PDF, HTML  
2. **Vector-based knowledge base creation**  
3. **RAG-based grounded test case generation**  
4. **Auto-generated Selenium test scripts**  

**Zero hallucination policy:** All test cases are strictly grounded in the uploaded documentation.

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

### Core
- Multi-format document ingestion  
- Vector knowledge base using Qdrant  
- RAG-powered grounded test cases  
- Automated Selenium Python script generation  
- Source attribution for every test case  
- Real-time validation  

### Technical
- Async FastAPI backend  
- LangChain v0.3.14 pipelines  
- Pydantic v2 models  
- HuggingFace MiniLM embeddings  
- Clean architecture separation  
- Extensive logging & error handling  

---

## 🛠️ Tech Stack

### Backend
| Component | Technology |
|----------|------------|
| Framework | FastAPI |
| LLM | OpenAI GPT‑4o‑mini |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | Qdrant Cloud |
| Orchestration | LangChain |
| Validation | Pydantic v2 |

### Frontend
| Component | Technology |
|----------|------------|
| UI Framework | Streamlit |
| HTTP Client | Requests |

### Document Parsing
- PyMuPDF (PDF)
- BeautifulSoup4 (HTML)
- python-markdown (MD)
- LangChain RecursiveCharacterTextSplitter

---

## 💻 System Requirements
- Python 3.10+
- 4GB RAM (8GB recommended)
- Internet (for API + Qdrant)
- Qdrant Cloud (free tier)
- OpenAI API key

---

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd autonomous-qa-agent
```

### 2. Create Virtual Env
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
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

Fill values:
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

#### Start Backend
```bash
uvicorn backend.main:app --reload
```

#### Start Frontend
```bash
streamlit run frontend/app.py
```

### Workflow

#### Step 1 — Build Knowledge Base
- Upload documents  
- Upload HTML  
- Click Build  
- Vectors stored in Qdrant  

#### Step 2 — Generate Test Cases
Example query:
```
Generate positive and negative test cases for discount code validation
```

#### Step 3 — Generate Selenium Scripts
- Select test case  
- Generate Python Selenium script  
- Download + execute  

---

## 📁 Project Structure
```
autonomous-qa-agent/
│
├── backend/
│   ├── main.py
│   ├── services/
│   │   ├── document_processor.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── llm_service.py
│   │   ├── test_case_generator.py
│   │   └── selenium_generator.py
│   ├── models/
│   │   └── schemas.py
│   └── utils/
│       └── helpers.py
│
├── frontend/
│   └── app.py
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

## 🔄 How It Works

### Document Processing
1. Extract text  
2. Chunk using RecursiveCharacterTextSplitter  
3. Generate embeddings  
4. Store vectors in Qdrant  

### RAG Test Case Generation
1. Query → embedding  
2. Vector similarity search  
3. Top‑K docs returned  
4. Context injected  
5. LLM generates grounded test cases  

### Selenium Script Generation
1. Parse HTML  
2. Extract selectors  
3. Retrieve relevant docs  
4. Prompt OpenAI  
5. Output refined Python Selenium code  

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

### Run Tests
```bash
pytest tests/ -v
```

---

## 🚢 Deployment (No Docker)

Run directly:

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
- LLM dependency  
- Requires internet  
- Occasional script refinement needed  
- English-only context  

---

## 🔮 Future Enhancements
- Multi‑LLM support  
- API test case generation  
- CI/CD integration  
- Mobile automation (Appium)  
- Visual test reporting  

---

## 👤 Author
**Koushil**  
Generative AI Developer  
Email: **koushil463@gmail.com**

---

## 📞 Support
- Read this README  
- Check `/docs`  
- Create GitHub issue  

---

_Last Updated: December 2025_

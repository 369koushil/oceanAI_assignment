# Autonomous QA Agent

An intelligent QA agent that generates comprehensive test cases and executable Selenium scripts from project documentation using **RAG (Retrieval Augmented Generation)** and **LLM technology**.

## Table of Contents

* Overview
* Features
* Tech Stack
* Prerequisites
* Installation
* Environment Variables
* Usage
* Project Structure
* API Documentation
* Included Assets
* Demo Video
* Troubleshooting

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│                     (Streamlit Frontend)                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Document   │  │  Test Case   │  │   Selenium   │         │
│  │  Processor   │  │  Generator   │  │  Generator   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────┬───────────────┬───────────────┬──────────────────┘
              │               │               │
              ▼               ▼               ▼
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  HuggingFace│  │   Qdrant    │  │   OpenAI    │
    │  Embeddings │  │   Vector    │  │  GPT-4o     │
    │             │  │     DB      │  │    mini     │
    └─────────────┘  └─────────────┘  └─────────────┘
```

### Data Flow

```
1. Document Upload
   ├── User uploads MD/TXT/JSON/PDF/HTML
   ├── Document Processor extracts text
   ├── RecursiveCharacterTextSplitter chunks text
   ├── HuggingFace generates embeddings (384-dim)
   └── Qdrant Cloud stores vectors + metadata

2. Test Case Generation (RAG)
   ├── User query converted to embedding
   ├── Vector similarity search in Qdrant
   ├── Top-K relevant chunks retrieved
   ├── Chunks + query sent to OpenAI
   ├── LLM generates structured test cases
   └── Response parsed and validated

3. Selenium Script Generation
   ├── Test case selected
   ├── HTML parsed for element selectors
   ├── Relevant docs retrieved from Qdrant
   ├── Test case + HTML + docs sent to OpenAI
   ├── LLM generates Python Selenium code
   └── Script cleaned and validated
```

### Component Diagram

```
Frontend (Streamlit)
    │
    ├─ Step 1: Knowledge Base Building
    │    ├─ File upload interface
    │    ├─ Progress indicators
    │    └─ Status notifications
    │
    ├─ Step 2: Test Case Generation
    │    ├─ Query input
    │    ├─ Test case display
    │    └─ Source attribution
    │
    └─ Step 3: Script Generation
         ├─ Test case selection
         ├─ Script preview
         └─ Download functionality

Backend (FastAPI)
    │
    ├─ Services Layer
    │    ├─ document_processor.py → Text extraction & chunking
    │    ├─ embeddings.py → Vector generation
    │    ├─ vector_store.py → Qdrant operations
    │    ├─ llm_service.py → OpenAI integration
    │    ├─ test_case_generator.py → RAG-based generation
    │    └─ selenium_generator.py → Script creation
    │
    ├─ Models Layer
    │    └─ schemas.py → Pydantic models
    │
    └─ API Endpoints
         ├─ POST /api/upload-documents
         ├─ POST /api/upload-html
         ├─ POST /api/generate-test-cases
         ├─ POST /api/generate-selenium-script
         └─ GET /health

External Services
    │
    ├─ Qdrant Cloud → Vector storage & search
    ├─ OpenAI API → LLM for generation
    └─ HuggingFace → Embedding models
```

---

## Overview

This system automates the QA process by:

1. Ingesting project documentation
2. Building a knowledge base using embeddings + vector search (Qdrant)
3. Generating grounded test cases using RAG
4. Creating executable Selenium scripts

Outputs are grounded in documentation — no hallucinations.

## ✨ Features

* Multi-format document parsing
* Qdrant-based vector search
* RAG-powered test generation
* Selenium script generation
* Streamlit UI
* Source references
* Strict grounding

## Tech Stack

### Backend

* FastAPI
* LangChain
* OpenAI API (gpt-4o-mini)
* Qdrant Cloud
* Sentence Transformers

### Frontend

* Streamlit

### Other

* Selenium

## Prerequisites

### Python

Python 3.10+

### OpenAI

Get API key from [https://platform.openai.com/](https://platform.openai.com/)

Model used: `gpt-4o-mini`

### Qdrant

Create free cluster and get credentials.

## Installation

### Clone

```
git clone <your-repo-url>
cd autonomous-qa-agent
```

### Virtual Environment

```
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate  # macOS/Linux
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Create `.env`

```
cp .env.example .env
```

Update:

```
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini
QDRANT_URL=your-url
QDRANT_API_KEY=your-key
QDRANT_COLLECTION_NAME=qa_agent_knowledge_base
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

## Environment Variables

Config is loaded directly from `.env` using:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Usage

### Start Backend

```
cd backend
python main.py
```

### Start Frontend

```
cd frontend
streamlit run app.py
```

### Build Knowledge Base

Upload documents → Upload HTML → Click Build.

### Generate Test Cases

Enter prompt → Generate.

### Generate Selenium Script

Select test case → Generate.

## Project Structure

```
backend/
  main.py
  services/
  models/
  utils/
frontend/
project_assets/
README.md
.env
```

## API Documentation

Available at:

```
http://localhost:8000/docs
```

## Included Assets

* checkout.html
* product_specs.md
* ui_ux_guide.txt
* api_endpoints.json
* test_scenarios.md

## Demo Video

Record steps:

1. Health check
2. Upload docs
3. Build KB
4. Generate test cases
5. Generate Selenium script

## Troubleshooting

### OpenAI Errors

401 = invalid API key.

### Qdrant Errors

Check URL & key.

### Missing Results

Reset & rebuild KB.

## Security

* Never commit `.env`
* Rotate keys
* Set OpenAI usage limits

## Author

Koushil


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

1. **Document ingestion**  
2. **Vector-based knowledge base creation**  
3. **RAG-based grounded test case generation**  
4. **Auto-generated Selenium test scripts**  

---

## 🏗️ Architecture
(Architecture text unchanged, omitted here for brevity)

---

## ✨ Features
(Features section unchanged, full content included in earlier file)

---

## 🛠️ Tech Stack
(Tech stack unchanged)

---

## 💻 Project Requirements
- Python 3.10+  
- 4GB RAM (8GB recommended)  
- Internet for Qdrant & OpenAI  
- Qdrant Cloud free tier  
- OpenAI API key  

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
│       └── schemas.py
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

### Create Virtual Environment
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

Create `.env` file:
```bash
cp .env.example .env
```

Fill values:
```
QDRANT_URL=
QDRANT_API_KEY=
OPENAI_API_KEY=
```

---

## 📖 Usage

### Run Backend
```bash
uvicorn backend.main:app --reload
```

### Run Frontend
```bash
streamlit run frontend/app.py
```

---

## 🔄 How It Works
(Document processing, RAG, Selenium generation — unchanged from previous version)

---

## 📚 API Documentation
(unchanged)

---

## 🧪 Testing
```bash
pytest tests/ -v
```

---

## 🚢 Deployment (No Docker)
Run directly:

```bash
uvicorn backend.main:app --reload
streamlit run frontend/app.py
```

---

## ⚠️ Limitations
(unchanged)

---

## 🔮 Future Enhancements
(unchanged)

---

## 👤 Author
**Koushil**  
Email: **koushil463@gmail.com**

---

## 📞 Support
- Check README  
- View `/docs`  
- Open GitHub issue  

_Last Updated: December 2025_

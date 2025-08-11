# Real Estate Research Assistant

An AI-powered real estate research assistant built using Retrieval-Augmented Generation (RAG) architecture.  
The assistant processes property listings and related documents to provide semantic search and context-aware answers.

---

## Features
- Upload and process property listings from PDF, DOCX, and TXT documents
- Semantic search using Hugging Face embeddings
- Vector database storage with ChromaDB for efficient retrieval
- Natural language queries powered by LangChain and RAG
- Interactive user interface built with Streamlit

---

## Tech Stack
- Python  
- LangChain  
- ChromaDB  
- Hugging Face Transformers  
- Streamlit  

---

## Installation
```bash
git clone https://github.com/yourusername/real-estate-research-assistant.git
cd real-estate-research-assistant
pip install -r requirements.txt
streamlit run app.py

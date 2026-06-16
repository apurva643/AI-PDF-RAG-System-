# AI-Powered PDF Question Answering System

An AI-powered Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions based on their contents.

## Features

* PDF Upload using FastAPI
* Text Extraction from PDF files
* Text Chunking
* Semantic Embeddings using Sentence Transformers
* Vector Storage using ChromaDB
* Similarity Search
* Gemini 2.5 Flash Integration
* Context-Aware Answer Generation
* Error Handling
* Professional Modular Architecture

## Tech Stack

* Python
* FastAPI
* ChromaDB
* Sentence Transformers
* Google Gemini API
* PyPDF

## Project Structure

```
RAG/
│
├── main.py
├── pdf_parser.py
├── chunking.py
├── embeddings.py
├── vector_store.py
├── rag_pipeline.py
├── config_example.py
├── test.py
├── .gitignore
└── README.md
```

## Architecture

```
PDF
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
ChromaDB
↓
Similarity Search
↓
Gemini 2.5 Flash
↓
Answer
```

## Example Workflow

1. Upload a PDF document.
2. Ask questions related to the uploaded PDF.
3. Retrieve relevant chunks using vector similarity.
4. Generate context-aware answers using Gemini.

## Future Improvements

* Multi-PDF Support
* Source Citations
* Page Number References
* Streamlit Frontend
* Conversation Memory
* Deployment using Docker
* Cloud Deployment

## Author

Apurva

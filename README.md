# UniGuide - AI-Powered University Assistant

## Overview

UniGuide is an AI-powered university assistant chatbot designed to help students access academic information quickly and efficiently. The project combines Retrieval-Augmented Generation (RAG), Hybrid Retrieval techniques, and Large Language Models (LLMs) to answer university-related questions in Arabic.

The chatbot can provide information about:

* College regulations and academic information.
* Lecture and exam schedules.
* Student-related inquiries.
* Questions based on university documents and structured data.

---

## Features

* Arabic language support.
* Retrieval-Augmented Generation (RAG).
* Hybrid Retrieval using FAISS and BM25.
* Semantic and lexical search capabilities.
* Intelligent query routing.
* Structured data retrieval from JSON files.
* Support for academic PDFs and exam schedules.
* Modular and scalable architecture.

---

## Technologies Used

* Python
* LangChain
* Groq API
* FAISS Vector Store
* BM25
* HuggingFace Embeddings
* Large Language Models (LLMs)

---

## Project Structure

```
UniGuide/
│
├── app/
│   ├── config.py
│   ├── ingestion.py
│   ├── learn.py
│   ├── main.py
│   ├── normalizer.py
│   ├── prompts.py
│   ├── responder.py
│   ├── retrieval.py
│   ├── router.py
│   └── ui.py
│
├── data/
│   ├── College/
│   ├── Tables/
│   └── tables.json
│
├── .env.example
├── .gitignore
└── README.md
```

---

## How It Works

1. The user submits a question in Arabic.
2. The Router determines the type of query.
3. Structured questions are answered using JSON data.
4. Document-based questions are processed using RAG.
5. Hybrid Retrieval combines:

   * FAISS (semantic search)
   * BM25 (keyword-based search)
6. The selected context is sent to the LLM to generate an answer.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/UniGuide.git
```

Move into the project directory:

```bash
cd UniGuide
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file based on `.env.example` and add your API key.

Example:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
MODEL_NAME=llama-3.1-8b-instant
VISION_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

---

## Running the Project

Run the application using:

```bash
python app/main.py
```

---

## Example Questions

* What exams do I have this week?
* What is the grading system in the college?
* What are the university regulations?
* What is my lecture schedule?
* Tell me about the Intelligent Systems program.

---

## Future Improvements

* Multi-query retrieval.
* Reranking techniques.
* Context compression.
* Conversation memory.
* Web interface deployment.
* Support for multiple universities.

---

## License

This project is intended for educational and research purposes.

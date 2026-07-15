# UniGuide

An NLP-powered university assistant chatbot designed to help students answer questions about their college, lecture schedules, and exam timetables using a hybrid retrieval architecture (RAG + Structured Data Retrieval).

---

## Project Overview

UniGuide is an intelligent chatbot that lets students select the type of question they're asking, and routes it to the appropriate retrieval pipeline.

The system supports:

- College information questions.
- Lecture schedules.
- Exam timetables.
- Retrieval-Augmented Generation (RAG) for PDF documents.
- Structured JSON retrieval for tabular data.
- OCR and Vision-based ingestion pipelines.
- Arabic and multilingual semantic search.

---

## Features

- Hybrid Retrieval Architecture.
- User-selected query mode with dedicated retrieval pipelines.
- FAISS Vector Database.
- Structured JSON Database.
- OCR + Groq Vision ingestion pipeline.
- Semantic document search.
- Arabic query support.
- Modular Python architecture.

---

## System Architecture

The following diagram shows the high-level architecture of UniGuide.

![Full System Architecture](assets/Full%20System%20Architecture.png)

The user interacts with the Gradio UI, which sends the question to the Chat Pipeline. The Router determines the query type and forwards it to the Retrieval Module. Depending on the query, the system retrieves information from either the FAISS Vector Database or the JSON database before generating the final response using Groq LLM.

---

# How UniGuide Works

The chatbot processes questions through multiple stages.

![Query Processing Flow](assets/Query%20Processing%20Flow.png)

The workflow is:

1. Receive the user's question.
2. User selects the query mode (Schedules/Exams or College Info) from the interface.
3. Route it to the appropriate retrieval pipeline.
4. Retrieve relevant information.
5. Generate the response.
6. Return the final answer.

---

# Router Decision Flow

The Router receives the query mode selected by the user in the interface and directs the request to the corresponding pipeline.

![Router & Mode Flowchart](assets/Router%20&%20Mode%20Flowchart.png)

The Router supports two modes:

### Structured Retrieval

Used for:

- Exam schedules.
- Lecture schedules.
- Tabular information.

Pipeline:

```
Question
↓

Extract Query
↓

Search JSON Database
↓

Generate Response
```

---

### RAG Retrieval

Used for:

- College information.
- PDF documents.
- General university-related questions.

Pipeline:

```
Question
↓

Search FAISS Vector Store
↓

Retrieve Context
↓

Generate Response
```

---

# System Context

The following diagram illustrates how UniGuide interacts with its databases.

![System Context Diagram](assets/System%20Context%20Diagram.png)

UniGuide communicates with:

- JSON Database for structured data.
- FAISS Vector Database for semantic document retrieval.
- User interface for question handling.

---

# Data Ingestion Pipeline

UniGuide uses two separate ingestion pipelines.

![Data Ingestion Pipeline](assets/Data%20Ingestion%20Pipeline.png)

### Image Pipeline

Schedule images are processed using:

- Groq Vision Model.
- JSON extraction.
- Record normalization.
- JSON storage.

The extracted schedules are stored inside:

```
tables.json
```

---

### PDF Pipeline

PDF documents are processed using:

- OCR (Tesseract).
- Text normalization.
- Document chunking.
- Embedding generation.
- FAISS indexing.

The resulting embeddings are stored inside:

```
vector_store/
```

---

# Module Dependencies

The following diagram illustrates the relationships between the project's modules.

![Module Dependency](assets/Module%20Dependency.png)

Main modules include:

- main.py
- router.py
- retrieval.py
- responder.py
- ingestion.py
- normalizer.py
- config.py
- prompts.py

This modular design makes the system easier to maintain and extend.

---

# Package Structure

The package-level architecture is shown below.

![PackageClass Structure Diagram](assets/PackageClass%20Structure%20Diagram.png)

The project separates:

- Routing logic.
- Retrieval logic.
- Response generation.
- Ingestion pipeline.
- Configuration management.
- Prompt engineering.

---

# Query Handling Sequence

The following sequence diagram describes how a user query travels through the system.

![Sequence Diagram – Query Handling](assets/Sequence%20Diagram%20%E2%80%93%20Query%20Handling.png)

Sequence:

1. User submits a question.
2. UI sends the query to the Chat Pipeline.
3. Router determines the query type.
4. Retrieval module processes the request.
5. The appropriate database is queried.
6. Relevant context is retrieved.
7. Response Generator creates the final answer.
8. The answer is returned to the user.

---

# Technologies Used

| Component | Technology |
|----------|----------|
| LLM | Groq |
| Vision Model | Llama 4 Scout |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 |
| Vector Store | FAISS |
| OCR | Tesseract OCR |
| UI | Gradio |
| Language | Python |
| Retrieval | RAG + Structured Retrieval |

---

# Project Structure

```
UniGuide
│
├── app/
│   ├── config.py
│   ├── ingestion.py
│   ├── main.py
│   ├── normalizer.py
│   ├── prompts.py
│   ├── responder.py
│   ├── retrieval.py
│   ├── router.py
│   └── ui.py
│
├── assets/
├── data/
├── vector_store/
│
├── .env.example
├── .gitignore
└── README.md
```

---

# Running the Project

1. Clone the repository.

```bash
git clone https://github.com/MostafaHikal/UniGuide.git
```

2. Install the required dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` file.

```env
GROQ_API_KEY=your_api_key

MODEL_NAME=llama-3.1-8b-instant

VISION_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct

EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2
```

4. Run the application.

```bash
python app/ui.py
```

---

# Future Improvements

Potential enhancements include:

- Hybrid Search (BM25 + FAISS).
- Multi-query Retrieval.
- Re-ranking techniques.
- Context Compression.
- Parent-Child Retrieval.
- Conversation Memory.

---

# Author

**Mostafa Heikal**

Faculty of Computers and Information  
Machine Learning & NLP Enthusiast

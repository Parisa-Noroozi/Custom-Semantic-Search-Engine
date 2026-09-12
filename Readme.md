# Semantic Search Engine (Built from Scratch)

A lightweight semantic search engine developed entirely in Python without relying on pretrained embedding models or external NLP libraries.

This project was created as a research-oriented implementation to better understand how modern search engines combine lexical retrieval, semantic similarity, query understanding, and knowledge-based ranking.

---

## Project Goals

Instead of simply matching keywords, this engine attempts to understand the meaning of a user's query by combining several retrieval techniques.

The project demonstrates how semantic search can be implemented from scratch using handcrafted knowledge representations.

---

## Features

### Tokenization

Converts raw user input into normalized search tokens.

- Lowercasing
- Cleaning punctuation
- Preparing query terms

---

### Intent Detection

Detects the user's search intention.

Examples:

- Learning
- Documentation
- PDF search

Intent information is later used during ranking.

---

### Query Expansion

Expands the original query using manually designed synonym dictionaries.

Example:


python
↓

python
numpy
pandas
tensorflow
pytorch

This increases recall without requiring pretrained language models.

---

### Custom Semantic Embedding

Instead of pretrained embeddings, this project builds semantic vectors manually.

Each concept is represented by a handcrafted topic vector stored inside a custom Knowledge Base.

Example:


Python

↓

Programming
Machine Learning
Deep Learning
Backend
Data Science
...

These vectors are later used for semantic similarity.

---

### Semantic Similarity

Computes cosine similarity between

- Query embedding
- Document embedding

This allows the engine to retrieve semantically related documents instead of relying only on keyword overlap.

---

### Relation Bonus

A manually designed knowledge graph stores relationships between concepts.

Example:


Python

↓

TensorFlow
PyTorch
NumPy
Pandas

Related concepts receive additional ranking scores.

---

### Category Bonus

Documents sharing similar semantic categories also receive ranking improvements.

Example:


Programming

↓

Python
TensorFlow
PyTorch
FastAPI

---

### BM25 Ranking

Lexical relevance is calculated using the BM25 ranking algorithm.

This ensures strong keyword-based retrieval while semantic techniques improve overall ranking.

---

### Explainable Ranking

Every search result includes an explanation showing why it was selected.

Displayed information includes:

- BM25 score
- Semantic score
- Relation bonus
- Category bonus
- Intent bonus
- Final ranking score

This makes the ranking process fully transparent.

---

## Technologies

- Python
- FastAPI
- JavaScript
- HTML
- CSS

No pretrained NLP models were used.

---

## Getting Started

### Requirements

Before running the project, make sure the following tools are installed:

- Python 3.13
- pip
- Git

### Clone the Repository

Clone the project and move into the repository directory:

```bash
git clone https://github.com/Parisa-Noroozi/Custom-Semantic-Search-Engine.git
cd Custom-Semantic-Search-Engine
```

### Create a Virtual Environment

Using a virtual environment keeps the project dependencies isolated from other Python projects on your system.

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

To install only the dependencies required to run the application:

```bash
python -m pip install -r requirements.txt
```

For development and testing, install the development requirements instead:

```bash
python -m pip install -r requirements-dev.txt
```

The development requirements also install the runtime dependencies automatically.

### Run the Tests

Run the backend test suite from the project root:

```bash
python -m pytest backend/tests -q
```

### Start the API Server

Start the FastAPI application with Uvicorn:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI provides interactive API documentation automatically.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

### Main API Endpoints

The main API endpoints are:

```text
GET /health
GET /search?q=<query>
GET /suggest?q=<prefix>
```

---

## Project Structure


backend/

    tokenizer/

    search/

    embeddings/

    ranking/

    query_expander/

    semantic_ranker/

frontend/

    HTML

    CSS

    JavaScript

---

## Future Improvements

- Dense vector indexing
- Hybrid Retrieval
- ANN Search
- Transformer Embeddings
- FAISS Integration
- Sentence Transformers
- Learning-to-Rank

---

## Educational Purpose

This project was intentionally implemented from scratch to understand the internal mechanics behind semantic search engines instead of relying on high-level NLP frameworks.




## Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Search Results

![Search Results](screenshots/search.png)

### Developer Mode

![Developer Mode](screenshots/Developer_mode.png)

### Full Page

![Full Page](screenshots/full_page.png)
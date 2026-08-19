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
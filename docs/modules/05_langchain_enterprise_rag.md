# Module 05: Subproject I — Enterprise RAG Service with LangChain & Vector Search

## Objectives
Architect and implement a production-ready, cloud-deployable Retrieval-Augmented Generation (RAG) microservice using LangChain Expression Language (LCEL), PostgreSQL `pgvector`, hybrid search, and streaming FastAPI endpoints.

---

## Subproject Scope & Architecture

```text
┌─────────────────┐      ┌─────────────────────────┐      ┌───────────────────────┐
│ Document Source │ ───> │ Ingestion Pipeline      │ ───> │ PostgreSQL (pgvector) │
│ (PDF / Markdown)│      │ Semantic Chunker + Embed│      │ Dense Vectors + FTS   │
└─────────────────┘      └─────────────────────────┘      └───────────────────────┘
                                                                      ▲
                                                                      │ Hybrid Search
┌─────────────────┐      ┌─────────────────────────┐      ┌───────────┴───────────┐
│ Client (Web/UI) │ <─── │ FastAPI Streaming (SSE) │ <─── │ LangChain LCEL RAG    │
│ Token Stream    │      │ Real-time Token chunks  │      │ Cross-Encoder Rerank  │
└─────────────────┘      └─────────────────────────┘      └───────────────────────┘
```

---

## Core Topics
1. **LangChain Expression Language (LCEL) & Streaming:**
   - Composing chains declaratively using `Runnable` abstractions and the pipe `|` operator.
   - Managing async execution with `.ainvoke()`, `.abatch()`, and real-time streaming with `.astream()`.
   - Dynamic prompt templates with formatting, partial parameters, and structured JSON output parsers.
2. **Document Ingestion & Semantic Chunking:**
   - Text splitting strategies: token-aware recursive character chunking and markdown header splitting.
   - Metadata enrichment: Document tags, page numbers, timestamps, and access-control scopes.
   - Generating vector embeddings with rate-limit retries and batching.
3. **Database & Hybrid Vector Search:**
   - Storing embeddings directly in PostgreSQL using `pgvector` and SQLAlchemy.
   - Hybrid retrieval: Combining dense vector similarity (cosine / dot product distance) with sparse keyword matching (`tsvector` and `tsquery`) using Reciprocal Rank Fusion (RRF).
   - Re-ranking top candidates using cross-encoder models for high precision context injection.
4. **FastAPI Streaming Delivery:**
   - Exposing LLM generation over HTTP using Server-Sent Events (SSE) via `StreamingResponse`.
   - Streaming citation metadata, source references, and latency metrics alongside token output.
5. **Observability & RAG Evaluation:**
   - End-to-end tracing with LangSmith / OpenTelemetry to inspect prompt templates and token costs.
   - Evaluating RAG quality using the `RAGAS` framework (evaluating Faithfulness, Context Precision, and Answer Relevance).

---

## Planned Directory Structure
```text
Module_05_LangChain_Enterprise_RAG_Subproject/
├── README.md
├── pyproject.toml
├── src/
│   └── rag_service/
│       ├── __init__.py
│       ├── main.py              # FastAPI app with SSE streaming endpoint
│       ├── config.py            # LLM API keys, DB connection strings, models
│       ├── ingestion/           # Chunking, metadata tagging, embedding pipeline
│       ├── vectorstore/         # pgvector SQLAlchemy schema & search queries
│       ├── chains/              # LCEL chains, prompt templates, reranker logic
│       └── evaluation/          # RAGAS evaluation harness & test dataset
└── tests/
    ├── test_chunking.py
    ├── test_vector_search.py
    └── test_streaming_api.py
```

---

## Verification Criteria
- [ ] Ingestion pipeline cleanly embeds and indexes documents in PostgreSQL `pgvector`.
- [ ] Hybrid search returns ranked documents with accurate citations.
- [ ] FastAPI endpoint streams token chunks in real-time over SSE without buffering delays.
- [ ] Automated evaluation tests pass threshold criteria for faithfulness and relevance.

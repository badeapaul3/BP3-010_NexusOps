# Enterprise Cloud Platform: Production Python Engineering

Welcome to the **Enterprise Cloud Platform** repository. This is a single, unified, production-grade Python (3.12+) codebase designed to demonstrate how an enterprise backend evolves—from modern static typing and packaging foundations, to asynchronous high-throughput engines, clean architecture APIs, cloud deployment (AWS & GCP), stateful AI agent workflows, and deep SRE observability.

---

## Complete Master Plan & Technical Setup

- 👉 **[ROADMAP.md](./ROADMAP.md)**: The 10-Milestone Master Curriculum & Architecture.
- 🎓 **[LEARNING_GUIDELINES.md](./docs/LEARNING_GUIDELINES.md)**: Pair-programming operating model (You build, I guide).
- 📋 **[setup_info.md](./setup_info.md)**: Technical audit of the current environment, tooling decisions, and foundational implementation.

---

## Architecture & Unified Codebase Layout

Rather than isolated toy micro-repos, this repository is built as **one cohesive, production system** where each module progressively establishes a key architectural layer:

```text
Learning/Python/
├── README.md                      # Unified repository guide & architecture entrypoint
├── ROADMAP.md                     # Master 10-Milestone Architectural Plan
├── pyproject.toml                 # Single source of truth (PEP 517/518/621, Hatchling, Ruff, Mypy)
├── uv.lock                        # Deterministic cross-platform lockfile
├── .gitignore                     # Production Git ignore rules
│
├── docs/modules/                  # Detailed Architectural Milestone Guides:
│   ├── 01_tooling_typing_pydantic.md
│   ├── 02_asyncio_concurrency_resilience.md
│   ├── 03_fastapi_database_clean_architecture.md
│   ├── 04_testing_paradigms_testcontainers.md
│   ├── 05_langchain_enterprise_rag.md
│   ├── 06_langgraph_multiagent_workflows.md
│   ├── 07_production_containers_images.md
│   ├── 08_orchestration_cloud_infrastructure.md
│   ├── 09_cicd_release_engineering.md
│   └── 10_observability_sre_cloud_operations.md
│
├── src/cloud_platform/            # The Unified Production Package
│   ├── __init__.py
│   ├── core/                      # M1 & M2: Pydantic Settings, Typing, Protocols, Async Engine, Resilience
│   │   ├── config.py              # 12-factor configuration & secret management
│   │   ├── protocols.py           # Structural typing interfaces (typing.Protocol)
│   │   ├── decorators.py          # Type-safe Generics & ParamSpec decorators
│   │   └── concurrency.py         # Structured concurrency, TaskGroups & queues
│   ├── domain/                    # M1 & M3: Pure domain models, entities, validation
│   ├── infrastructure/            # M3: PostgreSQL (SQLAlchemy 2.0 Async), Redis, Alembic
│   ├── api/                       # M3: FastAPI routers, dependencies, middlewares, schemas
│   ├── ai/                        # M5 & M6: AI systems & workflows
│   │   ├── rag/                   # M5 Subproject: LangChain LCEL, pgvector hybrid search, SSE
│   │   └── agents/                # M6 Subproject: LangGraph multi-agent, checkpointing, HITL
│   └── observability/             # M10: OpenTelemetry tracing, Prometheus RED metrics, structlog
│
├── tests/                         # M4: Comprehensive Testing Suite
│   ├── unit/                      # Fast in-memory unit tests
│   ├── property/                  # Hypothesis generative property tests
│   ├── integration/               # Testcontainers (Postgres, Redis)
│   └── performance/               # Locust load test scenarios
│
├── migrations/                    # M3: Alembic async database migrations
├── docker/                        # M7: Hardened multi-stage Dockerfile, Distroless runtime
├── k8s/ & terraform/              # M8: Kubernetes manifests & AWS / GCP Terraform IaC
└── .github/                       # M9: GitHub Actions CI/CD pipelines
```

---

## The 10 Progressive Modules & Milestones

| # | Milestone & Guide | Production Layer Built in `src/cloud_platform/` |
| :-: | :--- | :--- |
| **01** | [01: Tooling, Packaging, Typing & Pydantic v2](docs/modules/01_tooling_typing_pydantic.md) | `pyproject.toml`, `core/config.py`, `core/protocols.py`, `domain/models.py` |
| **02** | [02: Asyncio, Concurrency & Resilience](docs/modules/02_asyncio_concurrency_resilience.md) | `core/concurrency.py`, `core/resilience/` (TaskGroups, queues, circuit breakers) |
| **03** | [03: FastAPI, Async Database & Clean Architecture](docs/modules/03_fastapi_database_clean_architecture.md) | `api/`, `infrastructure/database/`, `infrastructure/cache/`, `migrations/` |
| **04** | [04: Testing Paradigms & Testcontainers](docs/modules/04_testing_paradigms_testcontainers.md) | `tests/unit/`, `tests/property/`, `tests/integration/` (Testcontainers) |
| **05** | [05: Subproject I — Enterprise RAG (LangChain)](docs/modules/05_langchain_enterprise_rag.md) | `ai/rag/` (LCEL pipeline, pgvector hybrid search, FastAPI SSE stream) |
| **06** | [06: Subproject II — Multi-Agent Workflows (LangGraph)](docs/modules/06_langgraph_multiagent_workflows.md) | `ai/agents/` (StateGraph, PostgreSQL checkpointing, HITL approval gate) |
| **07** | [07: Production Containers & Image Engineering](docs/modules/07_production_containers_images.md) | `docker/Dockerfile` (multi-stage, BuildKit uv cache, non-root Distroless) |
| **08** | [08: Container Orchestration & Cloud Infrastructure](docs/modules/08_orchestration_cloud_infrastructure.md) | `k8s/` manifests, `terraform/aws/`, `terraform/gcp/` (ECS/Cloud Run + Aurora/Cloud SQL) |
| **09** | [09: Enterprise CI/CD Automation & GitOps](docs/modules/09_cicd_release_engineering.md) | `.github/workflows/` (cached CI, private artifact publishing, Canary rollouts) |
| **10** | [10: Observability, SRE & Cloud Operations](docs/modules/10_observability_sre_cloud_operations.md) | `observability/` (OpenTelemetry traces, Prometheus RED metrics, `structlog`) |

---

## Toolchain Setup

We utilize **Astral `uv`** for universal, hermetic package and virtual environment management:

```bash
# Sync all dependencies and install the project in editable mode
uv sync --all-extras

# Run strict type checking across the entire repo
uv run mypy

# Run Ruff linter and formatter checks
uv run ruff check .
uv run ruff format --check .

# Run the test suite
uv run pytest
```

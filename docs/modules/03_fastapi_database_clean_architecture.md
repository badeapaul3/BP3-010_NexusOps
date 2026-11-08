# Module 03: Enterprise REST APIs with FastAPI, Async Database & Clean Architecture

## Objectives
Design and implement a production-grade asynchronous REST API service using FastAPI, PostgreSQL with async SQLAlchemy 2.0, Alembic migrations, Redis caching, and Clean/Hexagonal Architecture.

---

## Core Topics
1. **Advanced FastAPI Architecture:**
   - Dependency Injection tree (`Depends`): scoping, stateful dependencies, and context managers (`yield` syntax).
   - Middleware pipeline: Request ID tracing, timing, CORS, and standardized RFC 7807 error responses.
   - Application lifecycle management with `@asynccontextmanager` (lifespan events for database connection warm-up and graceful resource release).
2. **PostgreSQL Persistence with SQLAlchemy 2.0 (Async):**
   - Modern `DeclarativeBase` and `Mapped[T]` syntax with `mapped_column`.
   - `AsyncSession`, async engines with `asyncpg`, and connection pool tuning (`pool_size`, `max_overflow`, `pool_recycle`, `pool_pre_ping`).
   - Unit of Work pattern: Atomic transactions, rollbacks, and explicit transaction boundary control.
3. **Zero-Downtime Database Migrations with Alembic:**
   - Async migration recipe (`env.py` configured for async engine).
   - Expand-and-Contract database schema evolution (forward and backward compatibility).
4. **Distributed Caching with Redis:**
   - Redis connection pool management (`redis-py` async).
   - Cache-aside pattern with TTL, distributed rate-limiting, and key namespacing.
5. **Clean / Hexagonal Architecture:**
   - Strict separation of layers:
     - `Domain`: Pure business entities and domain exceptions (zero framework dependencies).
     - `Application / Use Cases`: Orchestration logic and repository interfaces (Protocols).
     - `Infrastructure`: SQLAlchemy repository implementations, Redis client, external service adapters.
     - `Presentation / API`: FastAPI routers, request/response Pydantic DTOs, dependency providers.

---

## Planned Directory Structure
```text
Module_03_FastAPI_Database_CleanArchitecture/
├── README.md
├── pyproject.toml
├── alembic.ini
├── migrations/                  # Alembic async migration environment
│   ├── env.py
│   └── versions/
├── src/
│   └── service/
│       ├── __init__.py
│       ├── main.py              # FastAPI app factory & lifespan handler
│       ├── core/                # Config, logging, exceptions
│       ├── domain/              # Entities, business rules, interfaces
│       ├── application/         # Use cases / services
│       ├── infrastructure/      # SQLAlchemy repos, database session engine, Redis cache
│       └── api/                 # Routers, DTO schemas, dependencies, middlewares
└── tests/
    ├── unit/
    └── integration/
```

---

## Verification Criteria
- [ ] Database migrations execute cleanly via `alembic upgrade head`.
- [ ] All API endpoints follow Clean Architecture (domain logic has 0 framework imports).
- [ ] Connection pool handles concurrent load without connection exhaustion.
- [ ] Redis caching reduces database hits on high-read endpoints.

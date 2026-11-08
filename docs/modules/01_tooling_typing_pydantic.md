# Module 01: Modern Python Tooling, Packaging, Typing & Pydantic v2

## Objectives
Master the modern Python developer toolchain and static typing ecosystem to build deterministic, type-safe, production-ready Python packages and services.

---

## Core Topics
1. **Tooling & Package Management with `uv`:**
   - Setting up isolated virtual environments with `uv venv`.
   - Managing dependencies with `uv add`, `uv lock`, and `uv sync`.
   - Running scripts in isolated hermetic environments with `uv run`.
2. **Standard Packaging & Distribution (PEP 517/518/621):**
   - Authoring `pyproject.toml` with `hatchling` as the build backend.
   - Understanding wheels (`.whl`) vs source distributions (`sdist`).
   - Distribution mechanics: Publishing and consuming from private artifact repositories (AWS CodeArtifact, GCP Artifact Registry, private indexes).
   - `pip` in production containers: `--no-cache-dir`, `--break-system-packages`, wheel installation.
3. **Strict Static Typing with Mypy & Pyright:**
   - Structural subtyping with `typing.Protocol` vs nominal subtyping with `abc.ABC`.
   - Advanced Generics: `TypeVar`, `Generic[T]`, `ParamSpec` for type-safe function decorators.
   - Modern unions (`|`), `Literal`, `Annotated`, `TypeGuard`, and `TypeIs`.
4. **Pydantic v2 Architecture:**
   - The Rust-powered `pydantic-core` validation engine.
   - Field validators (`@field_validator(mode='before'|'after')`) and model validators (`@model_validator(mode='wrap'|'after')`).
   - Custom serialization with `@field_serializer` and computed fields with `@computed_field`.
   - Configuration & secret management using `pydantic-settings` (12-Factor principles, `.env` file resolution, environment variable overriding).

---

## Planned Directory Structure
```text
Module_01_Tooling_Packaging_Typing_Pydantic/
├── README.md
├── pyproject.toml               # PEP 621 packaging metadata & tool configurations (ruff, mypy)
├── uv.lock                      # Deterministic lockfile
├── src/
│   └── core_package/
│       ├── __init__.py
│       ├── config.py            # Pydantic v2 Settings (12-Factor, SecretStr, env mapping)
│       ├── domain/
│       │   ├── models.py        # Pydantic v2 domain models with custom validators/serializers
│       │   └── protocols.py     # Structural typing interfaces (typing.Protocol)
│       └── utils/
│           └── decorators.py    # Generics and ParamSpec type-safe decorators
└── tests/
    ├── test_config.py
    ├── test_models.py
    └── test_protocols.py
```

---

## Verification Criteria
- [ ] Dependency resolution and environment synchronization completed via `uv sync`.
- [ ] Package builds successfully into `.whl` and `.tar.gz` via `uv build` / `hatchling`.
- [ ] Strict type checking passes (`mypy --strict` with zero errors).
- [ ] Linter & formatter clean (`ruff check` & `ruff format --check`).
- [ ] Pydantic v2 validation and serialization tests passing under `pytest`.

# Module 04: Enterprise Testing Paradigms: From Unit to Testcontainers & Property Testing

## Objectives
Build a resilient, comprehensive testing strategy across the test pyramid: fast unit tests, generative property-based tests with Hypothesis, and true integration tests with ephemeral Docker containers via Testcontainers.

---

## Core Topics
1. **Pytest Mastery for Enterprise Backends:**
   - Fixture lifecycles: `session`, `module`, `package`, and `function` scopes.
   - Asynchronous test orchestration with `pytest-asyncio` in strict mode.
   - Test suite categorization via custom markers (`@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`).
   - Parametrization (`@pytest.mark.parametrize`) for high data coverage with minimal boilerplate.
2. **Pragmatic Mocking & Network Isolation:**
   - The boundary between mock-based unit tests and real integration tests.
   - `pytest-mock` (`mocker` fixture) and `monkeypatch`.
   - Mocking asynchronous HTTP requests using `respx` and `httpx.MockTransport`.
3. **True Ephemeral Integration Testing with `testcontainers-python`:**
   - Automatically provisioning real PostgreSQL and Redis containers inside Docker during test runs.
   - Bootstrapping clean databases: executing Alembic migrations per test session and wrapping test cases in rollback transactions for speed and isolation.
   - Running containerized tests in CI/CD without hardcoded database credentials.
4. **Property-Based Testing with `Hypothesis`:**
   - Shifting from example-based testing to invariant and property verification.
   - Defining strategies for domain models, boundary numbers, and edge-case unicode strings.
   - Detecting state-machine regressions and edge-case overflows.
5. **Quality Gates, Mutation Testing & Load Testing:**
   - Measuring branch coverage with `pytest-cov` and enforcing minimum coverage thresholds in CI.
   - Assessing test assertion efficacy via mutation testing (`mutmut`).
   - Load and latency profiling with `locust`.

---

## Planned Directory Structure
```text
Module_04_Testing_Paradigms_Pytest_Integration/
├── README.md
├── pyproject.toml
├── conftest.py                  # Root pytest fixtures (async event loops, testcontainers)
├── src/                         # Subject under test (business logic & persistence)
└── tests/
    ├── unit/                    # Fast, pure Python tests (no I/O)
    ├── property/                # Hypothesis property-based fuzzing tests
    ├── integration/             # Testcontainers (real Postgres + Redis in Docker)
    └── performance/             # Locust load testing scripts
```

---

## Verification Criteria
- [ ] Ephemeral Docker containers start and tear down cleanly during test execution.
- [ ] `Hypothesis` passes across thousands of randomized parameter permutations.
- [ ] Test coverage exceeds 90% branch coverage with `pytest-cov`.
- [ ] Fast feedback: Unit test suite completes in under 3 seconds.

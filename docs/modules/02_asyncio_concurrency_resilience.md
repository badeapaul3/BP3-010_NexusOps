# Module 02: Advanced Asyncio, Concurrency & Production Resilience

## Objectives
Master the mechanics of Python's asynchronous event loop, implement structured concurrency, manage backpressure with bounded queues, and design resilient network communication with circuit breakers and graceful shutdown.

---

## Core Topics
1. **Event Loop Internals & Cooperative Multitasking:**
   - How the event loop schedules coroutines, tasks, and callbacks.
   - The Global Interpreter Lock (GIL): I/O bound vs CPU-bound considerations.
   - Production loop implementations (`uvloop` vs standard asyncio event loop).
2. **Structured Concurrency (Python 3.11+):**
   - The risks of `asyncio.gather` (orphaned background tasks on exception).
   - Mastering `asyncio.TaskGroup` for deterministic task lifecycles and exception groups (`ExceptionGroup`).
   - Timeouts using `asyncio.timeout` and cancelling with `asyncio.CancelledError`.
3. **Synchronization & Bounded Concurrency:**
   - Protecting shared async state with `asyncio.Lock` and coordinate via `asyncio.Event`.
   - Limiting concurrent requests with `asyncio.Semaphore` to protect downstream APIs.
   - Producer-Consumer architecture using bounded `asyncio.Queue` for backpressure management.
4. **Bridging Sync and Async:**
   - Delegating blocking legacy I/O to worker threads with `asyncio.to_thread`.
   - Offloading CPU-heavy tasks with `concurrent.futures.ProcessPoolExecutor`.
5. **Fault Tolerance & Resilience Patterns:**
   - Exponential backoff with randomized jitter using `tenacity`.
   - Building an async Circuit Breaker pattern (Closed -> Open -> Half-Open).
   - Signal handling (`SIGTERM`, `SIGINT`) for graceful shutdown without dropping in-flight tasks.

---

## Planned Directory Structure
```text
Module_02_Asyncio_Concurrency_Resilience/
├── README.md
├── pyproject.toml
├── src/
│   └── async_engine/
│       ├── __init__.py
│       ├── pipeline.py          # Producer-Consumer queue pipeline with bounded backpressure
│       ├── pool.py              # Thread/Process executor bridges for sync/CPU work
│       ├── resilience/
│       │   ├── circuit_breaker.py # Async stateful circuit breaker
│       │   └── retries.py       # Tenacity retry policies with exponential jitter
│       └── shutdown.py          # POSIX & Windows graceful signal handling
└── tests/
    ├── test_pipeline.py
    ├── test_circuit_breaker.py
    └── test_resilience.py
```

---

## Verification Criteria
- [ ] Bounded queue pipeline processes concurrent tasks without memory ballooning.
- [ ] Circuit breaker opens on error thresholds and recovers during half-open trial.
- [ ] Cancellation propagates cleanly through `TaskGroup` without orphan tasks.
- [ ] Graceful shutdown successfully drains active tasks on termination signal.

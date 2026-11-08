"""Type-safe decorators utilizing ParamSpec and TypeVar."""

import asyncio
import functools
import logging
import time
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def log_execution_time(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    """Measure and log async function latency while preserving exact type signatures."""

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        try:
            return await func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "Execution finished for %s in %.2fms",
                func.__qualname__,
                elapsed_ms,
                extra={"function": func.__qualname__, "latency_ms": elapsed_ms},
            )

    return wrapper


def retry_with_backoff(
    retries: int = 3,
    initial_delay: float = 0.1,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    """Async retry decorator with exponential backoff preserving exact parameter types."""

    def decorator(
        func: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            delay = initial_delay
            last_exception: Exception | None = None

            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    if attempt == retries:
                        logger.error(
                            "Failed %s after %d retries: %s",
                            func.__qualname__,
                            retries,
                            exc,
                        )
                        raise
                    logger.warning(
                        "Attempt %d/%d for %s failed (%s). Retrying in %.2fs...",
                        attempt,
                        retries,
                        func.__qualname__,
                        exc,
                        delay,
                    )
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

            assert last_exception is not None
            raise last_exception

        return wrapper

    return decorator

"""Unit tests verifying type-safe decorators and ParamSpec behavior."""

import pytest

from cloud_platform.core.decorators import log_execution_time, retry_with_backoff


@pytest.mark.asyncio
async def test_log_execution_time_returns_value() -> None:
    @log_execution_time
    async def sample_async_task(a: int, b: int) -> int:
        return a + b

    result = await sample_async_task(10, 20)
    assert result == 30


@pytest.mark.asyncio
async def test_retry_with_backoff_eventual_success() -> None:
    attempts = 0

    @retry_with_backoff(retries=3, initial_delay=0.01, backoff_factor=1.5)
    async def flaky_operation() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ConnectionError("Transient network failure")
        return "success"

    result = await flaky_operation()
    assert result == "success"
    assert attempts == 3


@pytest.mark.asyncio
async def test_retry_with_backoff_exhaustion_raises() -> None:
    @retry_with_backoff(retries=2, initial_delay=0.01)
    async def permanently_failing_operation() -> None:
        raise ValueError("Fatal invalid parameter")

    with pytest.raises(ValueError, match="Fatal invalid parameter"):
        await permanently_failing_operation()

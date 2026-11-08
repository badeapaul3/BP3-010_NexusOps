"""Structural typing interfaces (Protocols) for Clean Architecture decoupling."""

from collections.abc import Sequence
from datetime import datetime
from typing import (
    Any,
    Protocol,
    TypeVar,
    runtime_checkable,
)
from uuid import UUID

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


@runtime_checkable
class Entity(Protocol):
    """Protocol enforced on all domain entities."""

    id: UUID
    created_at: datetime
    updated_at: datetime


@runtime_checkable
class Auditable(Protocol[T_co]):
    """Structural protocol for objects that emit audit logs."""

    @property
    def audit_trail(self) -> Sequence[str]:
        """Sequence of human-readable audit records."""
        ...

    def get_audit_snapshot(self) -> dict[str, Any]:
        """Dictionary representation of state for compliance logging."""
        ...


@runtime_checkable
class Repository(Protocol[T]):
    """Generic async repository interface following Port-and-Adapter pattern."""

    async def get_by_id(self, entity_id: UUID) -> T | None:
        """Fetch entity by primary key."""
        ...

    async def list_all(self, limit: int = 100, offset: int = 0) -> Sequence[T]:
        """Fetch paginated sequence of entities."""
        ...

    async def add(self, entity: T) -> T:
        """Persist a new entity."""
        ...

    async def delete(self, entity_id: UUID) -> bool:
        """Delete entity by ID."""
        ...


@runtime_checkable
class EventPublisher(Protocol[T_contra]):
    """Generic structural interface for message brokers (Redis, SNS, PubSub)."""

    async def publish(self, topic: str, event: T_contra) -> None:
        """Publish an event to a given message channel or topic."""
        ...

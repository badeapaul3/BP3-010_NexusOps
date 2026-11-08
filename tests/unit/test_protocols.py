"""Unit tests verifying structural subtyping protocols."""

from collections.abc import Sequence
from uuid import UUID, uuid4

from cloud_platform.core.protocols import Auditable, Entity, Repository
from cloud_platform.domain.models import Workload, WorkloadStatus


class InMemoryWorkloadRepository:
    """In-memory adapter structurally satisfying Repository[Workload]."""

    def __init__(self) -> None:
        self._storage: dict[UUID, Workload] = {}

    async def get_by_id(self, entity_id: UUID) -> Workload | None:
        return self._storage.get(entity_id)

    async def list_all(self, limit: int = 100, offset: int = 0) -> Sequence[Workload]:
        items = list(self._storage.values())
        return items[offset : offset + limit]

    async def add(self, entity: Workload) -> Workload:
        self._storage[entity.id] = entity
        return entity

    async def delete(self, entity_id: UUID) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False


def test_workload_satisfies_entity_protocol() -> None:
    workload = Workload(
        tenant_id=uuid4(),
        name="batch-worker-prod",
    )
    # Checks runtime protocol checkable conformance
    assert isinstance(workload, Entity)
    assert hasattr(workload, "id")
    assert hasattr(workload, "created_at")
    assert hasattr(workload, "updated_at")


def test_workload_satisfies_auditable_protocol() -> None:
    workload = Workload(
        tenant_id=uuid4(),
        name="data-sync-job",
    )
    assert isinstance(workload, Auditable)
    snapshot = workload.get_audit_snapshot()
    assert snapshot["workload_id"] == str(workload.id)
    assert snapshot["status"] == WorkloadStatus.PENDING.value


def test_repository_structural_subtyping() -> None:
    repo = InMemoryWorkloadRepository()
    # Check that repo satisfies the Repository protocol without inheriting from it
    assert isinstance(repo, Repository)

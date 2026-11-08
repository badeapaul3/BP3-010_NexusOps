"""Production domain models for Pydantic v2 validation, immutability, and serialization."""

from collections.abc import Sequence
from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated, Any
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)


class TenantTier(StrEnum):
    """SLA and rate-limit tiers for multi-tenant isolation."""

    COMMUNITY = "community"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class WorkloadPriority(StrEnum):
    """Execution priority levels for asynchronous jobs."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class WorkloadStatus(StrEnum):
    """Lifecycle states of cloud workloads."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AuditEntry(BaseModel):
    """Immutable audit entry for compliance and observability."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    actor: str = Field(min_length=3, max_length=128)
    action: str = Field(min_length=2, max_length=64)
    details: dict[str, Any] = Field(default_factory=dict)


class Tenant(BaseModel):
    """Multi-tenant organization account entity."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=2, max_length=100)
    slug: str = Field(pattern=r"^[a-z0-9-]+$")
    tier: TenantTier = TenantTier.COMMUNITY
    max_concurrent_workloads: Annotated[int, Field(ge=1, le=1000)] = 5
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator("slug", mode="before")
    @classmethod
    def sanitize_slug(cls, v: str) -> str:
        """Sanitize slug before validation."""
        return v.lower().strip()


class Workload(BaseModel):
    """Cloud workload computing job entity."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    id: UUID = Field(default_factory=uuid4)
    tenant_id: UUID
    name: str = Field(min_length=3, max_length=120)
    priority: WorkloadPriority = WorkloadPriority.NORMAL
    status: WorkloadStatus = WorkloadStatus.PENDING
    cpu_limit: Annotated[float, Field(ge=0.1, le=64.0)] = 1.0
    memory_mb_limit: Annotated[int, Field(ge=128, le=262144)] = 1024
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    audit_log: list[AuditEntry] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name_not_reserved(cls, value: str) -> str:
        """Reject system-reserved prefixes."""
        reserved = ["system-", "internal-", "test-"]
        if any(value.lower().startswith(prefix) for prefix in reserved):
            raise ValueError(f"Workload name cannot start with reserved prefix ({reserved})")
        return value

    @model_validator(mode="after")
    def validate_critical_priority_resources(self) -> "Workload":
        """Ensure critical priority workloads allocate minimum required resources."""
        if self.priority == WorkloadPriority.CRITICAL and self.cpu_limit < 2.0:
            raise ValueError("Critical workloads require at least 2.0 CPUs for redundancy")
        return self

    @field_serializer("created_at", "updated_at")
    def serialize_datetime_iso(self, dt: datetime) -> str:
        """Serialize datetimes consistently in ISO 8601 format."""
        return dt.isoformat()

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_active(self) -> bool:
        """Return True if workload is in an active non-terminal state."""
        return self.status in (WorkloadStatus.PENDING, WorkloadStatus.RUNNING)

    @property
    def audit_trail(self) -> Sequence[str]:
        """Satisfies Auditable protocol: human-readable audit trail."""
        return [f"[{e.timestamp.isoformat()}] {e.actor}: {e.action}" for e in self.audit_log]

    def get_audit_snapshot(self) -> dict[str, Any]:
        """Satisfies Auditable protocol: state snapshot for audit logging."""
        return {
            "workload_id": str(self.id),
            "tenant_id": str(self.tenant_id),
            "status": self.status.value,
            "priority": self.priority.value,
            "audit_entries_count": len(self.audit_log),
        }

"""Unit tests for domain models, Pydantic v2 validators, and serialization."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from cloud_platform.domain.models import (
    AuditEntry,
    Tenant,
    TenantTier,
    Workload,
    WorkloadPriority,
)


def test_tenant_creation_and_slug_sanitization() -> None:
    tenant = Tenant(
        name="  Acme Cloud Corp  ",
        slug="  ACME-PROD-01  ",
        tier=TenantTier.ENTERPRISE,
    )
    assert tenant.slug == "acme-prod-01"
    assert tenant.name == "Acme Cloud Corp"
    assert tenant.tier == TenantTier.ENTERPRISE


def test_workload_name_reserved_prefix_rejected() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Workload(
            tenant_id=uuid4(),
            name="system-kernel-patch",
        )
    assert "reserved prefix" in str(exc_info.value)


def test_critical_workload_resource_validation() -> None:
    # Critical workload with under 2.0 CPUs should fail model-level validation
    with pytest.raises(ValidationError) as exc_info:
        Workload(
            tenant_id=uuid4(),
            name="payment-gateway-processor",
            priority=WorkloadPriority.CRITICAL,
            cpu_limit=1.0,
        )
    assert "Critical workloads require at least 2.0 CPUs" in str(exc_info.value)


def test_critical_workload_resource_validation_success() -> None:
    workload = Workload(
        tenant_id=uuid4(),
        name="payment-gateway-processor",
        priority=WorkloadPriority.CRITICAL,
        cpu_limit=4.0,
    )
    assert workload.cpu_limit == 4.0
    assert workload.priority == WorkloadPriority.CRITICAL


def test_workload_audit_trail_and_active_state() -> None:
    workload = Workload(
        tenant_id=uuid4(),
        name="customer-reporting-worker",
    )
    assert workload.is_active is True

    workload.audit_log.append(
        AuditEntry(
            actor="admin@enterprise.internal",
            action="WORKLOAD_INITIALIZED",
        )
    )
    assert len(workload.audit_trail) == 1
    assert "WORKLOAD_INITIALIZED" in workload.audit_trail[0]

    # Test serializer
    serialized = workload.model_dump(mode="json")
    assert isinstance(serialized["created_at"], str)
    assert "T" in serialized["created_at"]

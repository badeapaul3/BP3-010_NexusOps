"""Unit tests for Pydantic v2 application settings and configuration."""

import pytest

from cloud_platform.core.config import AppSettings, CloudProvider, Environment


def test_default_settings_instantiation() -> None:
    settings = AppSettings()
    assert settings.app_name == "enterprise-cloud-platform"
    assert settings.environment == Environment.DEVELOPMENT
    assert settings.cloud_provider == CloudProvider.LOCAL
    assert settings.is_production is False


def test_environment_case_normalization() -> None:
    settings = AppSettings(environment="PRODUCTION")  # type: ignore[arg-type]
    assert settings.environment == Environment.PRODUCTION
    assert settings.is_production is True


def test_secret_string_masking() -> None:
    settings = AppSettings()
    # Ensure raw secret string is not exposed when converting settings or field to string
    assert "postgres_insecure_default" not in str(settings.db.password)
    assert settings.db.password.get_secret_value() == "postgres_insecure_default"


def test_computed_async_postgres_dsn() -> None:
    settings = AppSettings()
    dsn = str(settings.db.async_dsn)
    assert dsn.startswith("postgresql+asyncpg://")
    assert "localhost:5432" in dsn
    assert "enterprise_db" in dsn


def test_invalid_pool_bounds_raise_validation_error() -> None:
    with pytest.raises(ValueError):
        AppSettings(db={"pool_size": 200})  # type: ignore[arg-type]

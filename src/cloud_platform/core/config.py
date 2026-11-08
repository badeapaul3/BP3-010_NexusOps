"""Enterprise 12-Factor application configuration with Pydantic v2."""

from enum import StrEnum
from functools import lru_cache
from typing import Annotated

from pydantic import (
    Field,
    PostgresDsn,
    SecretStr,
    computed_field,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    """Execution environment tiers."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class CloudProvider(StrEnum):
    """Supported cloud target providers."""

    AWS = "aws"
    GCP = "gcp"
    LOCAL = "local"


class DatabaseSettings(BaseSettings):
    """PostgreSQL async connection pool settings."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: SecretStr = SecretStr("postgres_insecure_default")
    name: str = "enterprise_db"
    pool_size: Annotated[int, Field(ge=5, le=100)] = 20
    max_overflow: Annotated[int, Field(ge=0, le=50)] = 10
    pool_timeout_seconds: float = 30.0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_dsn(self) -> PostgresDsn:
        """Build asyncpg-compatible PostgreSQL DSN."""
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            path=self.name,
        )


class RedisSettings(BaseSettings):
    """Distributed Redis caching and rate-limiting configuration."""

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 6379
    password: SecretStr | None = None
    ssl: bool = False
    default_ttl_seconds: int = 3600


class AppSettings(BaseSettings):
    """Root application configuration aggregating sub-settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_name: str = "enterprise-cloud-platform"
    app_version: str = "0.1.0"
    environment: Environment = Environment.DEVELOPMENT
    cloud_provider: CloudProvider = CloudProvider.LOCAL

    api_prefix: str = "/api/v1"
    debug: bool = False

    # Security & Tokens
    secret_key: SecretStr = SecretStr("change-me-in-production-super-secret-key-32b")
    access_token_expire_minutes: int = 60

    # Sub-settings
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_environment(cls, value: str | Environment) -> Environment:
        """Normalize environment strings case-insensitively."""
        if isinstance(value, str):
            return Environment(value.lower().strip())
        return value

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_production(self) -> bool:
        """Convenience flag for production mode checks."""
        return self.environment == Environment.PRODUCTION


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Return a cached, thread-safe singleton instance of application settings."""
    return AppSettings()

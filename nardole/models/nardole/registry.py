"""Registry models."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel

from nardole.core.registry.services import CallServiceStatus, ServicePermission
from nardole.models.integrations.manifest import IntegrationManifest


class Integration(BaseModel):
    """Model for an integration."""

    manifest: IntegrationManifest
    module_path: Path


class RegisteredIntegration(Integration):
    """Model for a registered and configured integration."""

    entry_id: str


class UnregisteredConfigEntry(BaseModel):
    """Model for an integration config entry before registering service."""

    integration: RegisteredIntegration
    user_config: dict


class ConfigEntry(UnregisteredConfigEntry):
    """Model for an integration config entry."""

    data_directory: Path


class LoadedIntegration(RegisteredIntegration):
    """Model for a loaded integration."""

    instance: object
    runtime_data: Any


class ServiceEntry(BaseModel):
    """Model for a single service entry."""

    service_domain: str
    service_name: str
    grant_opts: list[str] | None = None
    user_service: bool = True
    model_service: bool = False
    function: Callable
    service_schema: type[BaseModel] | None = None
    response: Literal["always", "never", "allowed"] = "never"


class ServiceCallResult(BaseModel):
    """Result from a service call."""

    status: CallServiceStatus
    message: str | None = None
    result: Any = None


class ServiceCallApprovalRecord(BaseModel):
    """Single user/AI permission status for a service call."""

    username: str  # Name of user or owner of bot
    model_name: str | None = None  # If permissions are for bot
    grant_opt: str | None = None
    is_model: bool
    permission: ServicePermission


class ServiceCallPermissionRecord(BaseModel):
    """Model for a single service call permission record."""

    service_domain: str
    service_name: str
    deny_all_models: bool
    permissions: list[ServiceCallApprovalRecord]

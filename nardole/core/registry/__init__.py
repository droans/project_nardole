"""Registries."""

from .config_entries import ConfigEntryRegistry, IntegrationRegistry
from .services import PermissionsRegistry, ServiceRegistry

__all__ = (
    "ConfigEntryRegistry",
    "IntegrationRegistry",
    "PermissionsRegistry",
    "ServiceRegistry",
)

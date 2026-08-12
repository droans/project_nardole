"""Integration registry."""

from .permission_registry import PermissionsRegistry
from .service_registry import ServiceRegistry

__all__ = (
    "PermissionsRegistry",
    "ServiceRegistry",
)

"""Service and Permission Registry."""

import logging
from pathlib import Path

from nardole.const import PERMISSIONS_FILE_PATH
from nardole.core.registry.permissions import PermissionsRegistry
from nardole.exceptions import ServiceCallRegistryError
from nardole.models.nardole.registry import ServiceEntry

logger = logging.getLogger(__name__)


class ServiceRegistry:
    """Project Nardole service registry."""

    def __init__(
        self,
        permission_file_path: Path | str = PERMISSIONS_FILE_PATH,
    ) -> None:
        """Initialize class."""
        if isinstance(permission_file_path, str):
            permission_file_path = Path(permission_file_path)
        self._services: list[ServiceEntry] = []
        self._permissions_registry = PermissionsRegistry(
            permissions_registry_file_path=permission_file_path,
        )

    def _get_service_record(self, service_domain: str, service_name: str) -> ServiceEntry | None:
        """Retrieve a service entry if it exists."""
        matches = [
            service
            for service in self._services
            if service.service_name == service_name and service.service_domain == service_domain
        ]
        if not matches:
            return None
        return matches[0]

    def register_service(
        self,
        service_entry: ServiceEntry,
    ) -> None:
        """Register a service."""
        existing_record = self._get_service_record(
            service_domain=service_entry.service_domain,
            service_name=service_entry.service_name,
        )
        if existing_record:
            msg = (
                f"Service for domain {service_entry.service_domain}"
                f" and service name {service_entry.service_name}"
                " is already registered!"
            )
            raise ServiceCallRegistryError(msg)
        self._services.append(service_entry)
        self._permissions_registry.register_service_permissions(service_entry=service_entry, strict=False)

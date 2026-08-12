"""Integrations registry."""

import logging
from typing import TYPE_CHECKING

from nardole.core.registry.util import load_module_from_path
from nardole.exceptions import IntegrationError
from nardole.integrations import get_integrations_for_registry
from nardole.models.integrations.config_entry import BaseIntegrationConfigModel

if TYPE_CHECKING:
    from nardole.models.nardole.registry import Integration

logger = logging.getLogger(__name__)


class IntegrationRegistry:
    """Registry for integrations."""

    def __init__(self) -> None:
        """Initialize class."""
        self.integrations: dict[str, Integration] = {}

    def register_integrations(self) -> None:
        """Register all integrations."""
        self.integrations = {
            integration.manifest.domain: integration for integration in get_integrations_for_registry()
        }

    def get_config_schema_for_integration(self, domain: str) -> type[BaseIntegrationConfigModel]:
        """Retrieve the config schema for an integration."""
        integration = self.integrations.get(domain)
        if not integration:
            msg = f"Failed to find integration for domain {domain}"
            logger.error(msg)
            raise IntegrationError(msg)
        try:
            module = load_module_from_path(integration.module_path)
        except Exception as e:
            msg = f"Could not load module for integration {domain}"
            logger.exception(msg)
            raise IntegrationError(msg) from e

        schema = getattr(module, "CONFIG_SCHEMA", None)
        if type(schema) != type(BaseIntegrationConfigModel):  # noqa: E721
            msg = (
                f"Received incorrect type for {domain} integration schema."
                f"Expected a config model but received type {type(schema)}."
            )
            raise IntegrationError(msg)
        return schema  # ty: ignore[invalid-return-type]

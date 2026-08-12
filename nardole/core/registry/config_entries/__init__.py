"""Integration registry."""

from .config_entry_registry import ConfigEntryRegistry
from .const import IntegrationType, SupportedFeatures
from .integration_registry import IntegrationRegistry

__all__ = (
    "ConfigEntryRegistry",
    "IntegrationRegistry",
    "IntegrationType",
    "SupportedFeatures",
)

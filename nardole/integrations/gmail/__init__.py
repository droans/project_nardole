"""GMail Integration."""

from typing import TYPE_CHECKING

from nardole.integrations.gmail.main import GmailIntegration
from nardole.integrations.gmail.models import GMailConfig

if TYPE_CHECKING:
    from nardole.core import Nardole
    from nardole.core.indices import EmailIndexer
    from nardole.models.nardole.registry import ConfigEntry

CONFIG_SCHEMA = GMailConfig


def setup_from_config_entry(
    nardole: "Nardole",
    config_entry: "ConfigEntry",
    email_indexer: "EmailIndexer",
) -> GmailIntegration:
    """Setup integration from config entry."""
    integration = GmailIntegration(
        nardole=nardole,
        config_entry=config_entry,
        email_indexer=email_indexer,
    )
    integration.register_services()
    return integration

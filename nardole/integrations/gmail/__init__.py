"""GMail Integration."""

from typing import TYPE_CHECKING

from nardole.integrations.gmail.main import GMailIntegration
from nardole.integrations.gmail.models import GMailConfig
from nardole.models.nardole.registry import ConfigEntry

CONFIG_SCHEMA = GMailConfig

if TYPE_CHECKING:
    from nardole.core.contacts import ContactsManager
    from nardole.core.nardole import Nardole


def setup_from_config_entry(
    nardole: "Nardole",
    config_entry: ConfigEntry,
    contacts_manager: "ContactsManager",
) -> GMailIntegration:
    """Setup integration from config entry."""
    return GMailIntegration(
        nardole=nardole,
        config_entry=config_entry,
        contacts_manager=contacts_manager,
    )

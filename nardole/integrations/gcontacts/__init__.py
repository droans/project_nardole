"""Google Contacts Integration."""

from typing import TYPE_CHECKING

from nardole.integrations.gcontacts.main import GContactsIntegration
from nardole.integrations.gcontacts.models import GoogleContactsConfigModel
from nardole.models.nardole.registry import ConfigEntry

if TYPE_CHECKING:
    from nardole.core.contacts import ContactsManager
    from nardole.core.nardole import Nardole

CONFIG_SCHEMA = GoogleContactsConfigModel


def setup_from_config_entry(
    nardole: "Nardole",
    config_entry: ConfigEntry,
    contacts_manager: "ContactsManager",
) -> GContactsIntegration:
    """Setup integration from config entry."""
    return GContactsIntegration(nardole=nardole, config_entry=config_entry, contacts_manager=contacts_manager)

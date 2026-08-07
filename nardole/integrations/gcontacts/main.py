"""Main integration class."""

from typing import TYPE_CHECKING

from pydantic import ValidationError

from nardole.exceptions import ConfigEntryLoadError
from nardole.integrations.gcontacts.const import DOMAIN, REFRESH_CONTACTS_SERVICE
from nardole.integrations.gcontacts.models import GoogleContactsConfigModel, RefreshContactsServiceSchema
from nardole.models.nardole.registry import ServiceEntry

if TYPE_CHECKING:
    from nardole.core.contacts import ContactsManager
    from nardole.core.nardole import Nardole
    from nardole.models.nardole.registry import ConfigEntry


class GContactsIntegration:
    """Google Contacts integration."""

    def __init__(
        self,
        nardole: "Nardole",
        config_entry: "ConfigEntry",
        contacts_manager: "ContactsManager",
    ) -> None:
        """Initialize class."""
        self.nardole = nardole
        self.config_entry = config_entry
        self.contacts_manager = contacts_manager
        try:
            self.config = GoogleContactsConfigModel.model_validate(self.config_entry.user_config)
        except ValidationError as e:
            msg = "Received validation error when attempting to load config for Google Contacts"
            raise ConfigEntryLoadError(msg) from e
        except Exception as e:
            msg = "Config load failed for Google Contacts"
            raise ConfigEntryLoadError(msg) from e

    def register_services(self) -> None:
        """Register services."""
        refresh_contacts_entry = ServiceEntry(
            service_domain=DOMAIN,
            service_name=REFRESH_CONTACTS_SERVICE,
            grant_opts=None,
            function=self.update_contacts,
            service_schema=RefreshContactsServiceSchema,
        )
        self.nardole.service_registry.register_service(refresh_contacts_entry)

    async def update_contacts(self, account_name: str) -> None:
        """Update contacts."""

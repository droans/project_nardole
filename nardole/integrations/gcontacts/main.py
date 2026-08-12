"""Main integration class."""

from typing import TYPE_CHECKING

from pydantic import ValidationError

from nardole.exceptions import ConfigEntryLoadError
from nardole.models.nardole.registry import ServiceEntry

from .client import GContactsAPIClient
from .const import DOMAIN, REFRESH_CONTACTS_SERVICE
from .models import GoogleContactsConfigModel, RefreshContactsServiceSchema

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
        self.gcontacts_client = GContactsAPIClient(account_configs=self.config.accounts)

    def register_services(self) -> None:
        """Register services."""
        refresh_contacts_entry = ServiceEntry(
            service_domain=DOMAIN,
            service_name=REFRESH_CONTACTS_SERVICE,
            grant_opts=None,
            function=self.update_contacts,
            service_schema=RefreshContactsServiceSchema,
            user_service=True,
            model_service=False,
        )
        self.nardole.service_registry.register_service(refresh_contacts_entry)

    async def update_contacts(self, account_name: str) -> None:
        """Update contacts."""
        contacts = self.gcontacts_client.get_all_contacts_for_account(account_name=account_name)

        contact_emails = self.gcontacts_client.get_all_contact_email_addresses_for_account(account_name=account_name)
        contact_names = self.gcontacts_client.get_all_contact_names_for_account(account_name=account_name)
        contact_nicknames = self.gcontacts_client.get_all_contact_nicknames_for_account(account_name=account_name)
        contact_phone_numbers = self.gcontacts_client.get_all_contact_phone_numbers_for_account(
            account_name=account_name,
        )
        contact_photos = self.gcontacts_client.get_all_contact_photos_for_account(account_name=account_name)
        contact_urls = self.gcontacts_client.get_all_contact_urls_for_account(account_name=account_name)

        self.contacts_manager.import_contacts(contacts=contacts)
        self.contacts_manager.import_contacts_email_addresses(contacts=contact_emails)
        self.contacts_manager.import_contacts_names(contacts=contact_names)
        self.contacts_manager.import_contacts_nicknames(contacts=contact_nicknames)
        self.contacts_manager.import_contacts_phone_numbers(contacts=contact_phone_numbers)
        self.contacts_manager.import_contacts_photos(contacts=contact_photos)
        self.contacts_manager.import_contacts_urls(contacts=contact_urls)

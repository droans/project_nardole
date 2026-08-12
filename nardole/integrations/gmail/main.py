"""Main GMail Integration."""

import logging
from typing import TYPE_CHECKING

from nardole.integrations.gcontacts.const import DOMAIN
from nardole.models.nardole.registry import ServiceEntry

from .client import GMailAPIClient
from .const import GET_EMAILS_SERVICE
from .indexer import GMailIndexer
from .models import EmailFilter, GetEmailsForAccountServiceSchema, GMailConfig
from .utils import (
    get_all_conversations,
    store_account_last_process_timestamp,
)

if TYPE_CHECKING:
    from nardole.core.contacts import ContactsManager
    from nardole.core.nardole import Nardole
    from nardole.models.nardole.registry import ConfigEntry

logger = logging.getLogger(__name__)


class GMailIntegration:
    """GMail Integration."""

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
        self.config = GMailConfig.model_validate(config_entry.user_config)
        self.data_directory = config_entry.data_directory
        self.api_client = GMailAPIClient(
            config=self.config,
            data_directory=self.data_directory,
        )
        self.indexer = GMailIndexer(
            config=self.config,
            nardole=nardole,
            contacts_manager=contacts_manager,
        )

    def register_services(self) -> None:
        """Register Services."""
        get_emails_service_schema = ServiceEntry(
            service_domain=DOMAIN,
            service_name=GET_EMAILS_SERVICE,
            grant_opts=None,
            user_service=True,
            model_service=True,
            function=self.get_emails_for_account,
            service_schema=GetEmailsForAccountServiceSchema,
        )
        self.nardole.service_registry.register_service(service_entry=get_emails_service_schema)

    def get_emails_for_account(
        self,
        account_names: list[str] | str | None = None,
        filters: list[EmailFilter] | None = None,
        reprocess: bool = False,
    ) -> None:
        """Import messages interface."""
        if not account_names:
            account_names = [account.account_name for account in self.config.accounts]
        if isinstance(account_names, str):
            account_names = [account_names]
        for account_name in account_names:
            msg = f"Retrieving messages for {account_name}"
            logger.info(msg)
            messages = self.api_client.retrieve_all_messages_for_account(
                account_name=account_name,
                reprocess=reprocess,
                _filters=filters,
            )
            msg = f"Found {len(messages)} messages."
            logger.info(msg)
            conversations = get_all_conversations(account_name=account_name, messages=messages)

            logger.debug("Importing all messages.")
            self.indexer.import_messages_to_meilisearch(account_name=account_name, messages=messages)
            logger.debug("Imported all messages.")

            logger.debug("Importing all conversations.")
            self.indexer.import_conversations_to_meilisearch(
                account_name=account_name,
                conversations=conversations,
            )
            logger.debug("Imported all conversations.")

            store_account_last_process_timestamp(
                data_directory=self.data_directory,
                account_name=account_name,
            )

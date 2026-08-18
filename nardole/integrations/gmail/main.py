"""Gmail Integration."""

import logging
from typing import TYPE_CHECKING

from pydantic import ValidationError

from nardole.exceptions import ConfigEntryLoadError
from nardole.integrations.gmail.client import GMailAPIClient
from nardole.integrations.gmail.const import DOMAIN, GET_EMAILS_SERVICE
from nardole.integrations.gmail.models import EmailFilter, GetEmailsForAccountServiceSchema, GMailConfig
from nardole.models.nardole.registry import ServiceEntry

if TYPE_CHECKING:
    from nardole.core import Nardole
    from nardole.core.indices import EmailIndexer
    from nardole.models.nardole.registry import ConfigEntry


logger = logging.getLogger(__name__)


class GmailIntegration:
    """Gmail Integration."""

    def __init__(
        self,
        nardole: "Nardole",
        config_entry: "ConfigEntry",
        email_indexer: "EmailIndexer",
    ) -> None:
        """Initialize class."""
        self.nardole = nardole
        self.config_entry = config_entry
        self.email_indexer = email_indexer

        try:
            self.config = GMailConfig.model_validate(self.config_entry.user_config)
        except ValidationError as e:
            msg = (
                "Received validation error when attempting to load config for GMail"
                f"\n\nConfig: \n{self.config_entry.user_config}"
                f"\n\nConfig Entry: \n{self.config_entry}"
            )
            raise ConfigEntryLoadError(msg) from e
        except Exception as e:
            msg = "Config load failed for GMail"
            raise ConfigEntryLoadError(msg) from e
        self.gmail_client = GMailAPIClient(
            nardole=nardole,
            config=self.config,
            data_directory=self.config_entry.data_directory,
        )

    def register_services(self) -> None:
        """Register services."""
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
        override_filters: list[EmailFilter] | None = None,
        reprocess: bool = False,
    ) -> None:
        """Import messages."""
        if not account_names:
            account_names = [account.account_name for account in self.config.accounts]
        if isinstance(account_names, str):
            account_names = [account_names]
        for account_name in account_names:
            msg = f"Retrieving messages for {account_name}"
            logger.info(msg)
            messages = self.gmail_client.get_all_messages_for_account(
                account_name=account_name,
                reprocess=reprocess,
                override_filters=override_filters,
                response_format="raw",
            )
            self.email_indexer.import_emails(
                emails=messages,
                import_conversations=True,
                add_or_update="update",
            )

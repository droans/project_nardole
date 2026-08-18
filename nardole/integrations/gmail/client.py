"""GMail API Client."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from nardole.integrations.gmail.const import GmailClientError, GmailIntegrationError
from nardole.integrations.gmail.filters import create_filter_string
from nardole.integrations.gmail.models import (
    EmailFilter,
    EmailFiltersRule,
    GMailAccountConfig,
    GMailConfig,
    GmailMessage,
    GMailMetadataMessage,
    GmailRawMessage,
    ListMessagesResponse,
    MessageIdentifier,
)
from nardole.integrations.gmail.process_email import process_gmail_email
from nardole.integrations.gmail.util import get_last_process_datetime_for_account_and_filters
from nardole.models.indices.email import EmailModel

if TYPE_CHECKING:
    from googleapiclient._apis.gmail.v1.resources import GmailResource

    from nardole.core import Nardole

logger = logging.getLogger(__name__)

GetEmailResponseFormats = Literal["raw", "full"]


class GMailAPIClient:
    """Client to interact with GMail API."""

    def __init__(
        self,
        nardole: "Nardole",
        config: GMailConfig,
        data_directory: Path,
    ) -> None:
        """Initialize class."""
        self.nardole = nardole
        self.config = config
        self.data_directory = data_directory

    def _create_client(self, account_name: str) -> "GmailResource | None":
        """Create client for account."""
        account = self.get_account_by_name(account_name)
        if not account:
            return None
        creds = Credentials.from_authorized_user_file(filename=account.credentials_path)
        if creds.expired:
            creds.refresh(Request())

        return build(
            serviceName="gmail",
            version="v1",
            credentials=creds,
        )

    def get_account_by_name(self, account_name: str) -> GMailAccountConfig | None:
        """Get an account by the account name."""
        assert isinstance(self.config, GMailConfig)
        accounts = self.config.accounts
        for account in accounts:
            if account.account_name == account_name:
                return account
        return None

    def get_message_data_page(
        self,
        client: "GmailResource",
        account_name: str,
        page_token: str | None = None,
        _filter: EmailFilter | None = None,
        reprocess: bool = False,
    ) -> ListMessagesResponse:
        """Retrieve a single page of message data.

        If `reprocess` is False, this function will use the filters and additionally ensure message
            data is only pulled for new emails since the last run.
        If `reprocess` is True, this function will only use the filters.
        """
        if not reprocess:
            if _filter is None:
                _filter = EmailFilter(unique_id="auto")
            if _filter.include is None:
                _filter.include = EmailFiltersRule()
            latest_ts = get_last_process_datetime_for_account_and_filters(
                data_directory=self.data_directory,
                account_name=account_name,
                filters=_filter,
            )
            msg = f"Not set to reprocess; using latest timestamp of {latest_ts}."
            logger.debug(msg)
            _filter.include.after = max(_filter.include.after, latest_ts) if _filter.include.after else latest_ts
        qry_filters = create_filter_string(_filter) if _filter else None
        if qry_filters:
            msg = f'Final query string: "{qry_filters}"'
            logger.debug(msg)
        response = (
            client.users()
            .messages()
            .list(
                userId="me",
                pageToken=page_token,
                q=qry_filters,
            )
            .execute()
        )
        return ListMessagesResponse.model_validate(response)

    def retrieve_message_data(
        self,
        client: "GmailResource",
        account_name: str,
        _filter: EmailFilter,
        reprocess: bool = False,
    ) -> list[MessageIdentifier]:
        """Retrieve email data which matches the filter.

        If `reprocess` is False, this function will use the filters and additionally ensure message
            data is only pulled for new emails since the last run.
        If `reprocess` is True, this function will only use the filters.
        """
        next_page_token = None
        result: list[MessageIdentifier] = []
        msg = f"Retrieving messages for {account_name} using filters [{_filter.model_dump()}] (Reprocess: {reprocess})"
        logger.debug(msg)
        while True:
            tmp = self.get_message_data_page(
                client=client,
                account_name=account_name,
                page_token=next_page_token,
                _filter=_filter,
                reprocess=reprocess,
            )
            result.extend(tmp.messages)
            next_page_token = tmp.nextPageToken
            if not next_page_token:
                logger.debug("Received no new page token, assuming we have all our messages.")
                break
        return result

    def retrieve_message_data_for_filters(
        self,
        client: "GmailResource",
        account_name: str,
        message_filters: list[EmailFilter],
        reprocess: bool = False,
    ) -> list[MessageIdentifier]:
        """Retrieve all messages from account.

        If `reprocess` is False, this function will use the filters and additionally ensure message
            data is only pulled for new emails since the last run.
        If `reprocess` is True, this function will only use the filters.
        """
        result: list[MessageIdentifier] = []
        for _filter in message_filters:
            message_data = self.retrieve_message_data(
                client=client,
                account_name=account_name,
                _filter=_filter,
                reprocess=reprocess,
            )
            [result.append(msg_data) for msg_data in message_data if msg_data not in result]

        return result

    def retrieve_message_metadata(
        self,
        client: "GmailResource",
        message_identifiers: MessageIdentifier,
    ) -> GMailMetadataMessage:
        """Retrieve the metadata for a single message."""
        message = client.users().messages().get(userId="me", id=message_identifiers.id, format="metadata")
        return GMailMetadataMessage.model_validate(message)

    def retrieve_message(
        self,
        client: "GmailResource",
        message_identifiers: MessageIdentifier,
    ) -> GmailMessage:
        """Retrieve a single message."""
        message = client.users().messages().get(userId="me", id=message_identifiers.id, format="full")
        return GmailMessage.model_validate(message)

    def retrieve_message_raw(
        self,
        client: "GmailResource",
        message_identifiers: MessageIdentifier,
    ) -> GmailRawMessage:
        """Retrieve a single message with the raw data."""
        message = client.users().messages().get(userId="me", id=message_identifiers.id, format="raw")
        return GmailRawMessage.model_validate(message)

    def retrieve_messages(
        self,
        client: "GmailResource",
        message_identifiers: list[MessageIdentifier],
        response_format: GetEmailResponseFormats = "raw",
    ) -> list[GmailRawMessage] | list[GmailMessage]:
        """Retrieve messages by identifier."""
        funcs = {
            "raw": self.retrieve_message_raw,
            "metadata": self.retrieve_message_metadata,
            "full": self.retrieve_message,
        }
        func = funcs.get(response_format)
        assert func
        result: list[GmailRawMessage] | list[GmailMessage] = []
        for identifier in message_identifiers:
            result.append(func(client=client, message_identifiers=identifier))  # ty: ignore[invalid-argument-type] (Seriously, ty?)
        return result

    def get_all_messages_for_account(
        self,
        account_name: str,
        reprocess: bool = False,
        override_filters: list[EmailFilter] | None = None,
        response_format: GetEmailResponseFormats = "raw",
    ) -> list[EmailModel]:
        """Retrieve all messages for an account."""
        client = self._create_client(account_name=account_name)
        if not client:
            msg = f"Cannot create client for account {account_name}. Is it defined in your config?"
            raise GmailClientError(msg)
        account_config = self.get_account_by_name(account_name=account_name)
        if not account_config:
            msg = f"Cannot find account configuration for account {account_name}. Ensure you defined it in your config."
            raise GmailIntegrationError(msg)
        msg = f"Retrieving all messages for {account_name} (Reprocessing: {reprocess})"
        logger.debug(msg)
        used_filters = override_filters or account_config.filters
        message_identifiers = self.retrieve_message_data_for_filters(
            client=client,
            account_name=account_name,
            message_filters=used_filters,
            reprocess=reprocess,
        )
        messages = self.retrieve_messages(
            client=client,
            message_identifiers=message_identifiers,
            response_format=response_format,
        )
        return [process_gmail_email(email=message, account_name=account_name) for message in messages]

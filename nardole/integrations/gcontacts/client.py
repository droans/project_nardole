"""Google Contacts API Client."""

import logging
from typing import TYPE_CHECKING

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from nardole.integrations.gcontacts.const import (
    FIELD_EMAIL_ADDRESSES,
    FIELD_NAMES,
    FIELD_NICKNAMES,
    FIELD_PHONE_NUMBERS,
    FIELD_PHOTOS,
    FIELD_URLS,
)
from nardole.integrations.gcontacts.models import (
    GContactsApiAnyConnectionsModel,
    GContactsApiAnyModel,
    GoogleContactsAccountConfig,
)
from nardole.models.indices.contacts import (
    ContactEmailAddressModel,
    ContactModel,
    ContactNameModel,
    ContactNicknameModel,
    ContactPhoneNumberModel,
    ContactPhotoModel,
    ContactURLModel,
)

if TYPE_CHECKING:
    from googleapiclient._apis.people.v1.resources import PeopleServiceResource

logger = logging.getLogger(__name__)


class GContactsAPIClient:
    """Google Contacts API Client."""

    def __init__(
        self,
        account_configs: list[GoogleContactsAccountConfig],
    ) -> None:
        """Initialize class."""
        self.account_configs = account_configs

    def _create_client(self, account_name: str) -> "PeopleServiceResource | None":
        """Create client for account."""
        msg = f"Getting credentials for {account_name}"
        logger.info(msg)
        account = self.get_account_by_name(account_name=account_name)
        if not account:
            return None
        creds = Credentials.from_authorized_user_file(filename=account.credentials_path)
        msg = f"Expired? {creds.expired}"
        logger.info(msg)
        if creds.expired:
            msg = f"Refreshing credentials for {account_name}."
            logger.info(msg)
            creds.refresh(Request())
            with open(account.credentials_path, "w") as f:
                f.write(creds.to_json())
        return build(
            serviceName="people",
            version="v1",
            credentials=creds,
        )

    def get_account_by_name(self, account_name: str) -> GoogleContactsAccountConfig | None:
        """Get an account by the account name."""
        for account in self.account_configs:
            if account.account_name == account_name:
                return account
        return None

    def get_contacts_page(
        self,
        client: "PeopleServiceResource",
        field: str,
        page_token: str | None = None,
    ) -> GContactsApiAnyModel:
        """Return a single page of data for a single field."""
        response = (
            client.people()
            .connections()
            .list(
                resourceName="people/me",
                personFields=field,
                pageToken=page_token,
            )
            .execute()
        )
        return GContactsApiAnyModel.model_validate(response)

    def get_all_contacts_for_field(
        self,
        client: "PeopleServiceResource",
        field: str,
    ) -> list[GContactsApiAnyConnectionsModel]:
        """Get all contacts for a single field."""
        next_page_token = None
        result: list[GContactsApiAnyConnectionsModel] = []
        while True:
            tmp = self.get_contacts_page(
                client=client,
                field=field,
                page_token=next_page_token,
            )
            result.extend(tmp.connections)
            next_page_token = tmp.nextPageToken
            if not next_page_token:
                break
        return result

    def get_all_contacts_for_account(self, account_name: str) -> list[ContactModel]:
        """Return the base contacts model for all contacts with an account."""
        client = self._create_client(account_name)
        assert client
        all_fields = [
            FIELD_EMAIL_ADDRESSES,
            FIELD_NAMES,
            FIELD_NICKNAMES,
            FIELD_PHONE_NUMBERS,
            FIELD_PHOTOS,
            FIELD_URLS,
        ]
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=",".join(all_fields),
        )
        return [
            ContactModel(
                contact_id=contact.resourceName,
                email_address_keys=[addr.metadata.source.id for addr in contact.emailAddresses],
                name_keys=[addr.metadata.source.id for addr in contact.names],
                nickname_keys=[addr.metadata.source.id for addr in contact.nicknames],
                phone_number_keys=[addr.metadata.source.id for addr in contact.phoneNumbers],
                photo_keys=[addr.metadata.source.id for addr in contact.photos],
                url_keys=[addr.metadata.source.id for addr in contact.urls],
            )
            for contact in all_contacts
        ]

    def get_all_contact_email_addresses_for_account(self, account_name: str) -> list[ContactEmailAddressModel]:
        """Get all contact email addresses for an account."""
        client = self._create_client(account_name=account_name)
        assert client
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=FIELD_EMAIL_ADDRESSES,
        )
        result = []
        for contact in all_contacts:
            resource_name = contact.resourceName
            addrs = contact.emailAddresses
            for addr in addrs:
                source_id = addr.metadata.source.id
                address = addr.value
                addr_type = addr.type
                result.append(
                    ContactEmailAddressModel(
                        contact_id=resource_name,
                        unique_id=source_id,
                        email_address=address,
                        type=addr_type,
                    ),
                )
        return result

    def get_all_contact_phone_numbers_for_account(self, account_name: str) -> list[ContactPhoneNumberModel]:
        """Get all contact phone numbers for an account."""
        client = self._create_client(account_name=account_name)
        assert client
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=FIELD_PHONE_NUMBERS,
        )
        result = []
        for contact in all_contacts:
            resource_name = contact.resourceName
            phone_numbers = contact.phoneNumbers
            for phone_number in phone_numbers:
                number = phone_number.value
                canonical = phone_number.canonicalForm
                num_type = phone_number.type
                unique_id = phone_number.metadata.source.id
                result.append(
                    ContactPhoneNumberModel(
                        contact_id=resource_name,
                        unique_id=unique_id,
                        display_number=number,
                        canonical_number=canonical,
                        type=num_type,
                    ),
                )
        return result

    def get_all_contact_names_for_account(self, account_name: str) -> list[ContactNameModel]:
        """Get all contact names for an account."""
        client = self._create_client(account_name=account_name)
        assert client
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=FIELD_NAMES,
        )
        result = []
        for contact in all_contacts:
            resource_name = contact.resourceName
            names = contact.names
            for name in names:
                unique_id = name.metadata.source.id
                result.append(
                    ContactNameModel(
                        contact_id=resource_name,
                        unique_id=unique_id,
                        display_name=name.displayName,
                        family_name=name.familyName,
                        given_name=name.givenName,
                        last_first_name=name.displayNameLastFirst,
                        unstructured_name=name.unstructuredName,
                    ),
                )
        return result

    def get_all_contact_nicknames_for_account(self, account_name: str) -> list[ContactNicknameModel]:
        """Get all contact nicknames for an account."""
        client = self._create_client(account_name=account_name)
        assert client
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=FIELD_NICKNAMES,
        )
        result = []
        for contact in all_contacts:
            resource_name = contact.resourceName
            for nickname in contact.nicknames:
                unique_id = nickname.metadata.source.id
                result.append(
                    ContactNicknameModel(
                        contact_id=resource_name,
                        unique_id=unique_id,
                        nickname=nickname.value,
                    ),
                )
        return result

    def get_all_contact_photos_for_account(self, account_name: str) -> list[ContactPhotoModel]:
        """Get all contact photos for an account."""
        client = self._create_client(account_name=account_name)
        assert client
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=FIELD_PHOTOS,
        )
        result = []
        for contact in all_contacts:
            resource_name = contact.resourceName
            for photo in contact.photos:
                unique_id = photo.metadata.source.id
                result.append(
                    ContactPhotoModel(
                        contact_id=resource_name,
                        unique_id=unique_id,
                        photo_url=photo.url,
                    ),
                )
        return result

    def get_all_contact_urls_for_account(self, account_name: str) -> list[ContactURLModel]:
        """Get all contact URLs for an account."""
        client = self._create_client(account_name=account_name)
        assert client
        all_contacts = self.get_all_contacts_for_field(
            client=client,
            field=FIELD_URLS,
        )
        result = []
        for contact in all_contacts:
            resource_name = contact.resourceName
            for url in contact.urls:
                unique_id = url.metadata.source.id
                result.append(
                    ContactURLModel(
                        contact_id=resource_name,
                        unique_id=unique_id,
                        url=url.value,
                        type=url.type,
                    ),
                )
        return result

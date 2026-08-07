"""Contacts Index Manager."""

from typing import TYPE_CHECKING

from nardole.const import INDEX_CONTACTS
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
    from meilisearch import Client


class ContactsManager:
    """Contacts manager."""

    def __init__(
        self,
        meilisearch_client: "Client",
    ) -> None:
        """Initialize class."""
        self._client = meilisearch_client
        self._index = self._client.index(INDEX_CONTACTS)

    def import_contacts(self, contacts: list[ContactModel]) -> None:
        """Import contacts to Meilisearch."""

    def import_contacts_email_addresses(self, contacts: list[ContactEmailAddressModel]) -> None:
        """Import contacts email addresses to Meilisearch."""

    def import_contacts_names(self, contacts: list[ContactNameModel]) -> None:
        """Import contacts names to Meilisearch."""

    def import_contacts_nicknames(self, contacts: list[ContactNicknameModel]) -> None:
        """Import contacts nicknames to Meilisearch."""

    def import_contacts_phone_numbers(self, contacts: list[ContactPhoneNumberModel]) -> None:
        """Import contacts phone numbers to Meilisearch."""

    def import_contacts_photos(self, contacts: list[ContactPhotoModel]) -> None:
        """Import contacts photos to Meilisearch."""

    def import_contacts_urls(self, contacts: list[ContactURLModel]) -> None:
        """Import contacts urls to Meilisearch."""

    def search_contacts_by(
        self,
        email_addresses: list[str] | None = None,
        names: list[str] | None = None,
        nicknames: list[str] | None = None,
        phone_numbers: list[str] | None = None,
        photos: list[str] | None = None,
        urls: list[str] | None = None,
    ) -> list[ContactModel]:
        """Retrieve one or more contacts by a single field."""
        filters = []

        if email_addresses:
            filters.append(
                [f"_foreign(email_address_keys, email_address = {email_address})" for email_address in email_addresses],
            )

        if names:
            filters.append(
                [f"_foreign(name_keys, display_name = {name})" for name in names],
            )
        if nicknames:
            filters.append(
                [f"_foreign(nickname_keys, nickname = {nickname})" for nickname in nicknames],
            )
        if phone_numbers:
            filters.append(
                [f"_foreign(phone_number_keys, display_number = {phone_number})" for phone_number in phone_numbers],
            )
        if photos:
            filters.append(
                [f"_foreign(photos_keys, photo_url = {photo})" for photo in photos],
            )
        if urls:
            filters.append(
                [f"_foreign(url_keys, url = {url})" for url in urls],
            )

        results = self._index.search("", filters)
        return [ContactModel.model_validate(hit) for hit in results["hits"]]

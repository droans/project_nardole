"""Contacts Index Manager."""

from typing import TYPE_CHECKING, Literal

from nardole.const.contacts import (
    INDEX_CONTACTS,
    INDEX_CONTACTS_EMAIL_ADDRESSES,
    INDEX_CONTACTS_NAMES,
    INDEX_CONTACTS_NICKNAMES,
    INDEX_CONTACTS_PHONE_NUMBERS,
    INDEX_CONTACTS_PHOTOS,
    INDEX_CONTACTS_URLS,
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
    from meilisearch import Client


class ContactsIndexer:
    """Contacts manager."""

    def __init__(
        self,
        meilisearch_client: "Client",
    ) -> None:
        """Initialize class."""
        self._client = meilisearch_client
        self._contacts_index = self._client.index(INDEX_CONTACTS)
        self._email_index = self._client.index(INDEX_CONTACTS_EMAIL_ADDRESSES)
        self._name_index = self._client.index(INDEX_CONTACTS_NAMES)
        self._nickname_index = self._client.index(INDEX_CONTACTS_NICKNAMES)
        self._phone_number_index = self._client.index(INDEX_CONTACTS_PHONE_NUMBERS)
        self._photo_index = self._client.index(INDEX_CONTACTS_PHOTOS)
        self._url_index = self._client.index(INDEX_CONTACTS_URLS)

    def import_contacts(
        self,
        contacts: list[ContactModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts to Meilisearch."""
        func = self._contacts_index.add_documents if add_or_update == "add" else self._contacts_index.update_documents
        func(
            [contact.model_dump() for contact in contacts],
        )

    def import_contacts_email_addresses(
        self,
        contacts: list[ContactEmailAddressModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts email addresses to Meilisearch."""
        func = self._email_index.add_documents if add_or_update == "add" else self._email_index.update_documents
        func(
            [contact.model_dump() for contact in contacts],
        )

    def import_contacts_names(
        self,
        contacts: list[ContactNameModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts names to Meilisearch."""
        func = self._name_index.add_documents if add_or_update == "add" else self._name_index.update_documents
        func(
            [contact.model_dump() for contact in contacts],
        )

    def import_contacts_nicknames(
        self,
        contacts: list[ContactNicknameModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts nicknames to Meilisearch."""
        func = self._nickname_index.add_documents if add_or_update == "add" else self._nickname_index.update_documents
        func(
            [contact.model_dump() for contact in contacts],
        )

    def import_contacts_phone_numbers(
        self,
        contacts: list[ContactPhoneNumberModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts phone numbers to Meilisearch."""
        func = (
            self._phone_number_index.add_documents
            if add_or_update == "add"
            else self._phone_number_index.update_documents
        )
        func(
            [contact.model_dump() for contact in contacts],
        )

    def import_contacts_photos(
        self,
        contacts: list[ContactPhotoModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts photos to Meilisearch."""
        func = self._photo_index.add_documents if add_or_update == "add" else self._photo_index.update_documents
        func(
            [contact.model_dump() for contact in contacts],
        )

    def import_contacts_urls(
        self,
        contacts: list[ContactURLModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import contacts urls to Meilisearch."""
        func = self._url_index.add_documents if add_or_update == "add" else self._url_index.update_documents
        func(
            [contact.model_dump() for contact in contacts],
        )

    def filter_contacts_by(
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

        results = self._contacts_index.search("", filters)
        return [ContactModel.model_validate(hit) for hit in results["hits"]]

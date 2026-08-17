"""Configure Contacts Index settings."""

from nardole.const.indices import (
    INDEX_CONTACTS,
    INDEX_CONTACTS_EMAIL_ADDRESSES,
    INDEX_CONTACTS_NAMES,
    INDEX_CONTACTS_NICKNAMES,
    INDEX_CONTACTS_PHONE_NUMBERS,
    INDEX_CONTACTS_PHOTOS,
    INDEX_CONTACTS_URLS,
    ContactEmailIndexFields,
    ContactNamesIndexFields,
    ContactNicknameIndexFields,
    ContactPhoneNumberIndexFields,
    ContactPhotoIndexFields,
    ContactsIndexFields,
    ContactURLIndexFields,
)
from nardole.models.indices.settings import IndexAttributesConfig, IndexAttributesForeignKeyConfig, IndexConfig

CONTACTS_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    searchable_attributes=[
        ContactsIndexFields.EMAIL_ADDRESS_KEYS,
        ContactsIndexFields.NAME_KEYS,
        ContactsIndexFields.NICKNAME_KEYS,
        ContactsIndexFields.PHONE_NUMBER_KEYS,
    ],
    filterable_attributes=[ContactsIndexFields.CONTACT_ID],
)

EMAIL_ADDRESS_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[ContactEmailIndexFields.TYPE],
    displayed_attributes=[ContactEmailIndexFields.EMAIL, ContactEmailIndexFields.TYPE],
    searchable_attributes=[ContactEmailIndexFields.EMAIL],
)

NAME_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[ContactNamesIndexFields.FAMILY_NAME],
    displayed_attributes=[ContactNamesIndexFields.DISPLAY_NAME],
    searchable_attributes=[ContactNamesIndexFields.UNSTRUCTURED_NAME],
)

NICKNAME_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[ContactNicknameIndexFields.NICKNAME],
    displayed_attributes=[ContactNicknameIndexFields.NICKNAME],
    searchable_attributes=[ContactNicknameIndexFields.NICKNAME],
)


PHONE_NUMBER_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[ContactPhoneNumberIndexFields.TYPE],
    displayed_attributes=[
        ContactPhoneNumberIndexFields.CANONICAL_NUMER,
        ContactPhoneNumberIndexFields.PHONE_NUMBER,
        ContactPhoneNumberIndexFields.TYPE,
    ],
    searchable_attributes=[ContactPhoneNumberIndexFields.PHONE_NUMBER, ContactPhoneNumberIndexFields.CANONICAL_NUMER],
)


PHOTO_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    displayed_attributes=[ContactPhotoIndexFields.PHOTO_URL],
)

URL_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[ContactURLIndexFields.TYPE],
    displayed_attributes=[ContactURLIndexFields.URL, ContactURLIndexFields.TYPE],
    searchable_attributes=[ContactURLIndexFields.URL],
)


CONTACTS_INDEX_FOREIGN_KEY_CONFIG: list[IndexAttributesForeignKeyConfig] = [
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        field_name=ContactsIndexFields.EMAIL_ADDRESS_KEYS,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_NAMES,
        field_name=ContactsIndexFields.NAME_KEYS,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_NICKNAMES,
        field_name=ContactsIndexFields.NICKNAME_KEYS,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_PHONE_NUMBERS,
        field_name=ContactsIndexFields.PHONE_NUMBER_KEYS,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_PHOTOS,
        field_name=ContactsIndexFields.PHOTOS_KEYS,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_URLS,
        field_name=ContactsIndexFields.URL_KEYS,
    ),
]


def create_contacts_index_config() -> IndexConfig:
    """Create the contacts index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS,
        primary_key=ContactsIndexFields.CONTACT_ID,
        foreign_keys=CONTACTS_INDEX_FOREIGN_KEY_CONFIG,
        attributes=CONTACTS_INDEX_ATTRIBUTES_CONFIG,
    )


def create_email_address_index_config() -> IndexConfig:
    """Create the contacts email address index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        primary_key=ContactEmailIndexFields.UNIQUE_ID,
        attributes=EMAIL_ADDRESS_ATTRIBUTES_CONFIG,
    )


def create_name_index_config() -> IndexConfig:
    """Create the contacts name index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS_NAMES,
        primary_key=ContactNamesIndexFields.UNIQUE_ID,
        attributes=NAME_ATTRIBUTES_CONFIG,
    )


def create_nickname_index_config() -> IndexConfig:
    """Create the contacts nickname index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS_NICKNAMES,
        primary_key=ContactNicknameIndexFields.UNIQUE_ID,
        attributes=NICKNAME_ATTRIBUTES_CONFIG,
    )


def create_phone_number_index_config() -> IndexConfig:
    """Create the contacts phone number index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS_PHONE_NUMBERS,
        primary_key=ContactPhoneNumberIndexFields.UNIQUE_ID,
        attributes=PHONE_NUMBER_ATTRIBUTES_CONFIG,
    )


def create_photo_index_config() -> IndexConfig:
    """Create the contacts photo index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS_PHOTOS,
        primary_key=ContactPhotoIndexFields.UNIQUE_ID,
        attributes=PHOTO_ATTRIBUTES_CONFIG,
    )


def create_url_index_config() -> IndexConfig:
    """Create the contacts URL index config."""
    return IndexConfig(
        index_uid=INDEX_CONTACTS_URLS,
        primary_key=ContactURLIndexFields.UNIQUE_ID,
        attributes=URL_ATTRIBUTES_CONFIG,
    )

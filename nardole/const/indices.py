"""Project Nardole index consts."""

from enum import StrEnum

# Contacts
INDEX_CONTACTS = "contacts_ids"
INDEX_CONTACTS_EMAIL_ADDRESSES = "contacts_email_addresses"
INDEX_CONTACTS_NAMES = "contacts_names"
INDEX_CONTACTS_NICKNAMES = "contacts_nicknames"
INDEX_CONTACTS_PHONE_NUMBERS = "contacts_phone_numbers"
INDEX_CONTACTS_PHOTOS = "contacts_photos"
INDEX_CONTACTS_URLS = "contacts_urls"


class ContactsIndexFields(StrEnum):
    """`contacts_ids` Index fields."""

    CONTACT_ID = "contact_id"
    EMAIL_ADDRESS_KEYS = "email_address_keys"
    NAME_KEYS = "name_keys"
    NICKNAME_KEYS = "nickname_keys"
    PHONE_NUMBER_KEYS = "phone_number_keys"
    PHOTOS_KEYS = "photos_keys"
    URL_KEYS = "url_keys"


class ContactEmailIndexFields(StrEnum):
    """`contacts_email_addresses` Index fields."""

    CONTACT_ID = "contact_id"
    UNIQUE_ID = "unique_id"
    EMAIL = "email"
    TYPE = "type"


class ContactNamesIndexFields(StrEnum):
    """`contacts_names` Index fields."""

    CONTACT_ID = "contact_id"
    UNIQUE_ID = "unique_id"
    DISPLAY_NAME = "display_name"
    FAMILY_NAME = "family_name"
    GIVEN_NAME = "given_name"
    UNSTRUCTURED_NAME = "unstructured_name"


class ContactNicknameIndexFields(StrEnum):
    """`contacts_nicknames` Index fields."""

    CONTACT_ID = "contact_id"
    UNIQUE_ID = "unique_id"
    NICKNAME = "nickname"


class ContactPhoneNumberIndexFields(StrEnum):
    """`contacts_phone_numbers` Index fields."""

    CONTACT_ID = "contact_id"
    UNIQUE_ID = "unique_id"
    CANONICAL_NUMER = "canonical"
    PHONE_NUMBER = "phone_numer"
    TYPE = "type"


class ContactPhotoIndexFields(StrEnum):
    """`contacts_photos` Index fields."""

    CONTACT_ID = "contact_id"
    UNIQUE_ID = "unique_id"
    PHOTO_URL = "photo_url"


class ContactURLIndexFields(StrEnum):
    """`contact_urls` Index fields."""

    CONTACT_ID = "contact_id"
    UNIQUE_ID = "unique_id"
    URL = "url"
    TYPE = "type"


# Emails

INDEX_EMAILS = "emails"
INDEX_EMAIL_CONVERSATIONS = "email_conversations"


class EmailIndexFields(StrEnum):
    """`email` Index fields."""

    EMAIL_ID = "email_id"
    CONVERSATION_ID = "conversation_id"
    SENDER = "sender"
    TO = "to"
    CC = "cc"
    BCC = "bcc"
    SUBJECT = "subject"
    SUMMARIES = "summaries"
    ATTACHMENTS = "attachments"
    DOMAIN = "domain"
    ACCOUNT = "account"
    TIMESTAMP = "timestamp"


class EmailConversationIndexFields(StrEnum):
    """`email_conversations` Index fields."""

    CONVERSATION_ID = "conversation_id"
    ACCOUNT = "account"
    DOMAIN = "domain"
    PARTICIPANTS = "participants"

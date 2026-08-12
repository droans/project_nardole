"""Indexer configurations."""

from nardole.core.const import INDEX_CONTACTS
from nardole.integrations.gmail.const import (
    DOCUMENT_TEMPLATE,
    INDEX_CONVERSATIONS,
    INDEX_EMAILS,
    PRIMARY_KEY_CONVERSATIONS,
    PRIMARY_KEY_EMAILS,
)
from nardole.models.indexing import EmbedderSettings
from nardole.models.indices.settings import (
    IndexAttributesConfig,
    IndexAttributesForeignKeyConfig,
    IndexChatConfig,
    IndexConfig,
)

EMAIL_INDEX_CHAT_CONFIG = IndexChatConfig(
    default_document_template=DOCUMENT_TEMPLATE,
    description="Emails retrieved from the user's GMail account",
)
EMAIL_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[
        "thread_id",
        "label_ids",
        "mime_type",
        "sender",
        "to",
        "cc",
        "bcc",
        "subject",
        "body",
        "account_name",
    ],
)

EMAIL_INDEX_FOREIGN_KEY_CONFIG = [
    IndexAttributesForeignKeyConfig(foreign_key_uid=INDEX_CONVERSATIONS, field_name="thread_id"),
    IndexAttributesForeignKeyConfig(foreign_key_uid=INDEX_CONTACTS, field_name="sender"),
    IndexAttributesForeignKeyConfig(foreign_key_uid=INDEX_CONTACTS, field_name="to"),
    IndexAttributesForeignKeyConfig(foreign_key_uid=INDEX_CONTACTS, field_name="cc"),
    IndexAttributesForeignKeyConfig(foreign_key_uid=INDEX_CONTACTS, field_name="bcc"),
]

CONVERSATIONS_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[
        "thread_id",
        "participants",
        "account_name",
    ],
)

CONVERSATIONS_INDEX_FOREIGN_KEY_CONFIG = [
    IndexAttributesForeignKeyConfig(foreign_key_uid=INDEX_CONTACTS, field_name="participants"),
]


def create_email_index_config(embedder_settings: EmbedderSettings) -> IndexConfig:
    """Create the config for the email index."""
    return IndexConfig(
        index_uid=INDEX_EMAILS,
        primary_key=PRIMARY_KEY_EMAILS,
        chat=EMAIL_INDEX_CHAT_CONFIG,
        embedder=embedder_settings,
        foreign_keys=EMAIL_INDEX_FOREIGN_KEY_CONFIG,
        attributes=EMAIL_INDEX_ATTRIBUTES_CONFIG,
    )


def create_conversations_index_config() -> IndexConfig:
    """Create the config for the conversations index."""
    return IndexConfig(
        index_uid=INDEX_CONVERSATIONS,
        primary_key=PRIMARY_KEY_CONVERSATIONS,
        foreign_keys=CONVERSATIONS_INDEX_FOREIGN_KEY_CONFIG,
        attributes=CONVERSATIONS_INDEX_ATTRIBUTES_CONFIG,
    )

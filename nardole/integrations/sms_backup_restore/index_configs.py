"""Index configurations."""

from nardole.core.const import INDEX_CONTACTS
from nardole.models.indexing import EmbedderSettings
from nardole.models.indices.settings import (
    IndexAttributesConfig,
    IndexAttributesForeignKeyConfig,
    IndexChatConfig,
    IndexConfig,
)

from .const import (
    DOCUMENT_TEMPLATE,
    INDEX_SMS_CONVERSATIONS,
    INDEX_SMS_MESSAGES,
    PRIMARY_KEY_SMS_CONVERSATIONS,
    PRIMARY_KEY_SMS_MESSAGES,
)

SMS_MESSAGE_INDEX_CHAT_CONFIG = IndexChatConfig(
    description="An index of text messages.",
    default_document_template=DOCUMENT_TEMPLATE,
)

SMS_MESSAGE_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[
        "type",
        "sender",
        "participants",
        "conversation_id",
        "timestamp",
        "direction",
    ],
    searchable_attributes=[
        "message",
        "type",
        "sender",
        "participants",
        "conversation_id",
        "direction",
        "attachments",
    ],
    sortable_attributes=[
        "participants",
        "direction",
        "sender",
        "type",
        "timestamp",
    ],
)

SMS_MESSAGE_INDEX_FOREIGN_KEY_CONFIG = [
    IndexAttributesForeignKeyConfig(foreign_key_uid="sms_conversation", field_name="conversation_id"),
]


SMS_CONVERSATIONS_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[
        "participants",
        "conversation_id",
    ],
    searchable_attributes=["participants"],
    sortable_attributes=["participants"],
)

SMS_CONVERSATIONS_INDEX_FOREIGN_KEY_CONFIG = [
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS,
        field_name="participants",
    ),
]


def create_sms_message_index_config(embedder_settings: EmbedderSettings) -> IndexConfig:
    """Create the config for the SMS message index."""
    return IndexConfig(
        index_uid=INDEX_SMS_MESSAGES,
        primary_key=PRIMARY_KEY_SMS_MESSAGES,
        embedder=embedder_settings,
        chat=SMS_MESSAGE_INDEX_CHAT_CONFIG,
        foreign_keys=SMS_MESSAGE_INDEX_FOREIGN_KEY_CONFIG,
        attributes=SMS_MESSAGE_INDEX_ATTRIBUTES_CONFIG,
    )


def create_sms_conversations_index_config() -> IndexConfig:
    """Create the config for the SMS message index."""
    return IndexConfig(
        index_uid=INDEX_SMS_CONVERSATIONS,
        primary_key=PRIMARY_KEY_SMS_CONVERSATIONS,
        foreign_keys=SMS_CONVERSATIONS_INDEX_FOREIGN_KEY_CONFIG,
        attributes=SMS_CONVERSATIONS_INDEX_ATTRIBUTES_CONFIG,
    )

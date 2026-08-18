"""Configure Contacts Index settings."""

from typing import TYPE_CHECKING

from nardole.const.contacts import INDEX_CONTACTS_EMAIL_ADDRESSES
from nardole.const.email import (
    INDEX_EMAIL_CONVERSATIONS,
    INDEX_EMAILS,
    EmailConversationIndexFields,
    EmailIndexFields,
)
from nardole.models.indices.settings import IndexAttributesConfig, IndexAttributesForeignKeyConfig, IndexConfig

if TYPE_CHECKING:
    from nardole.models.indexing import EmbedderSettings

EMAILS_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[
        EmailIndexFields.ACCOUNT,
        EmailIndexFields.CONVERSATION_ID,
        EmailIndexFields.DOMAIN,
        EmailIndexFields.SENDER,
        EmailIndexFields.TO,
        EmailIndexFields.CC,
        EmailIndexFields.BCC,
    ],
    searchable_attributes=[
        EmailIndexFields.ATTACHMENTS,
        EmailIndexFields.SUBJECT,
        EmailIndexFields.SUMMARIES,
    ],
    sortable_attributes=[
        EmailIndexFields.TIMESTAMP,
    ],
    displayed_attributes=[
        EmailIndexFields.SENDER,
        EmailIndexFields.TO,
        EmailIndexFields.CC,
        EmailIndexFields.BCC,
        EmailIndexFields.SUBJECT,
        EmailIndexFields.SUMMARIES,
        EmailIndexFields.TIMESTAMP,
        EmailIndexFields.ATTACHMENTS,
    ],
)

EMAIL_CONVERSATION_INDEX_ATTRIBUTES_CONFIG = IndexAttributesConfig(
    filterable_attributes=[
        EmailConversationIndexFields.PARTICIPANTS,
        EmailConversationIndexFields.DOMAIN,
        EmailConversationIndexFields.ACCOUNT,
    ],
    searchable_attributes=[EmailConversationIndexFields.CONVERSATION_ID],
)

EMAILS_INDEX_FOREIGN_KEY_CONFIG: list[IndexAttributesForeignKeyConfig] = [
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_EMAIL_CONVERSATIONS,
        field_name=EmailIndexFields.CONVERSATION_ID,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        field_name=EmailIndexFields.SENDER,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        field_name=EmailIndexFields.TO,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        field_name=EmailIndexFields.CC,
    ),
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        field_name=EmailIndexFields.BCC,
    ),
]

EMAIL_CONVERSATION_INDEX_FOREIGN_KEY_CONFIG: list[IndexAttributesForeignKeyConfig] = [
    IndexAttributesForeignKeyConfig(
        foreign_key_uid=INDEX_CONTACTS_EMAIL_ADDRESSES,
        field_name=EmailConversationIndexFields.PARTICIPANTS,
    ),
]


def create_email_index_config(embedder_settings: "EmbedderSettings") -> IndexConfig:
    """Create the email index config."""
    return IndexConfig(
        index_uid=INDEX_EMAILS,
        primary_key=EmailIndexFields.EMAIL_ID,
        embedder=embedder_settings,
        foreign_keys=EMAILS_INDEX_FOREIGN_KEY_CONFIG,
        attributes=EMAILS_INDEX_ATTRIBUTES_CONFIG,
    )


def create_email_conversations_index_config() -> IndexConfig:
    """Create the email conversations index config."""
    return IndexConfig(
        index_uid=INDEX_EMAIL_CONVERSATIONS,
        primary_key=EmailIndexFields.CONVERSATION_ID,
        foreign_keys=EMAIL_CONVERSATION_INDEX_FOREIGN_KEY_CONFIG,
        attributes=EMAIL_CONVERSATION_INDEX_ATTRIBUTES_CONFIG,
    )

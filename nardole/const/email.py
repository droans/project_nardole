"""Email indexer consts."""

from enum import StrEnum

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

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
    ATTACHMENTS_FILENAME = "attachments.filename"
    ATTACHMENTS_MIME_TYPE = "attachments.mime_type"
    ATTACHMENTS_ATTACHMENT_ID = "attachments.attachment_id"
    ATTACHMENTS_SIZE = "attachments.size"
    ATTACHMENTS_CONTENT_ID = "attachments.content_id"
    LABELS = "labels"
    DOMAIN = "domain"
    ACCOUNT = "account"
    TIMESTAMP = "timestamp"


class EmailConversationIndexFields(StrEnum):
    """`email_conversations` Index fields."""

    CONVERSATION_ID = "conversation_id"
    ACCOUNT = "account"
    DOMAIN = "domain"
    PARTICIPANTS = "participants"


REPLACEMENT_IMG_HTML_TAG = "nardole-img"

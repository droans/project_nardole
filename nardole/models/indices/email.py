"""Email index models."""

from pydantic import BaseModel


class EmailAttachmentConfig(BaseModel):
    """Model for an email attachment."""

    filename: str
    mime_type: str
    attachment_id: str
    size: int
    content_id: str | None = None


class EmailModel(BaseModel):
    """Config for a single email."""

    timestamp: int
    email_id: str
    conversation_id: str
    sender: str
    to: list[str]
    cc: list[str]
    bcc: list[str]
    subject: str
    summaries: list[str]
    attachments: list[EmailAttachmentConfig]
    account: str
    domain: str

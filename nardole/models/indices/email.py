"""Email index models."""

from typing import Literal

from pydantic import BaseModel

from nardole.models.indexing import BaseSearchRequest


class EmailAttachmentConfig(BaseModel):
    """Model for an email attachment."""

    filename: str
    content_type: str
    attachment_id: str
    size: int = 0
    content_id: str | None = None


class EmailModel(BaseModel):
    """Config for a single email."""

    timestamp: int
    email_id: str
    conversation_id: str
    labels: list[str] = []
    sender: str
    to: list[str]
    cc: list[str]
    bcc: list[str]
    subject: str
    summaries: list[str]
    attachments: list[EmailAttachmentConfig]
    account: str
    domain: str


class EmailConversationModel(BaseModel):
    """Model for an email conversation."""

    conversation_id: str
    participants: list[str]
    domain: str
    account: str


class EmailSearchOptions(BaseModel):
    """Model for the options for searching emails."""

    attachments_filename: str | None = None
    subject: str | None = None
    summaries: str | None = None


class EmailSortOptions(BaseModel):
    """Model for the options for sorting email search results."""

    timestamp: Literal["asc", "desc"] | None = None


class EmailFilterOptions(BaseModel):
    """Model for filtering search emails."""

    account: str | list[str] | None = None
    conversation_id: str | list[str] | None = None
    domain: str | list[str] | None = None
    sender: str | list[str] | None = None
    to: str | list[str] | None = None
    cc: str | list[str] | None = None
    bcc: str | list[str] | None = None
    attachments_mime_type: str | list[str] | None = None
    labels: str | list[str] | None = None


class EmailSearchRequest(BaseSearchRequest):
    """Model for an email search request."""

    search: str | EmailSearchOptions = ""
    sort: EmailSortOptions | None = None
    filter: EmailFilterOptions | None = None

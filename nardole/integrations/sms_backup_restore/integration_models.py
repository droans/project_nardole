"""Integration models."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from nardole.models.indexing import E164NumberType, IndexFileModel
from nardole.models.integrations.config_entry import BaseIntegrationConfigModel

from .const import (
    DEFAULT_PROCESS_CONTENT_TYPE_PREFIXES,
    DEFAULT_PROCESS_CONTENT_TYPES,
)


class SMSBackupAndRestoreConfigModel(BaseIntegrationConfigModel):
    """User config schema."""

    type: Literal["sms_br"]
    user_phone_number: str
    region: str
    save_attachment_types: list[str] = DEFAULT_PROCESS_CONTENT_TYPES
    save_attachment_type_prefixes: list[str] = DEFAULT_PROCESS_CONTENT_TYPE_PREFIXES


class ImportSMSMessagesServiceSchema(BaseModel):
    """Service schema for import_sms_messages."""

    xml_path: str | Path


class MessageModel(BaseModel):
    """Base Model for a single message."""

    type: Literal["sms", "mms", "rcs"]
    sender: E164NumberType
    participants: list[E164NumberType]
    conversation_id: str
    timestamp: int
    message: str | None = None
    readable_date: str | None = None
    direction: Literal["sent", "received"]
    message_id: str
    attachments: list[IndexFileModel] = []


class ConversationModel(BaseModel):
    """Model for a conversation."""

    conversation_id: str
    participants: list[E164NumberType]


class UnsavedAttachment(BaseModel):
    """Model for an unsaved attachment."""

    file_name: str
    content_type: str
    encoded_data: bytes


class UnprocessedMessageModel(MessageModel):
    """Model for a single message with unsaved attachments."""

    attachments: list[UnsavedAttachment] = []

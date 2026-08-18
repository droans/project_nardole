"""GMail Integration models."""

import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, FilePath

from nardole.models.integrations.config_entry import BaseIntegrationConfigModel


def _str_to_list(val: str | list[str]) -> list[str]:
    if isinstance(val, list):
        return val
    return [val]


StringOrListString = Annotated[
    str | list[str],
    BeforeValidator(_str_to_list),
]


class EmailFiltersRule(BaseModel):
    """Rule for filtering emails selected."""

    before: datetime.datetime | None = None
    after: datetime.datetime | None = None
    sender: StringOrListString | None = None
    participants: StringOrListString | None = None
    to: StringOrListString | None = None
    cc: StringOrListString | None = None
    bcc: StringOrListString | None = None
    label_ids: list[str] | None = None
    has_attachment: bool | None = None


class EmailFilter(BaseModel):
    """Include/Exclude rules for managing emails."""

    unique_id: str
    include: EmailFiltersRule | None = None
    exclude: EmailFiltersRule | None = None


class GetEmailsForAccountServiceSchema(BaseModel):
    """Service schema for GetEmailsForAccount."""

    account_names: list[str] | str | None
    override_filters: list[EmailFilter] | None = None
    reprocess: bool = False


class GMailAccountConfig(
    BaseModel,
    arbitrary_types_allowed=True,
):
    """Model for the configuration for a single gmail account."""

    credentials_path: FilePath
    account_name: str
    filters: list[EmailFilter] = []


class GMailConfig(BaseIntegrationConfigModel):
    """Model for gmail configuration."""

    domain: Literal["gmail"]
    accounts: list[GMailAccountConfig]


class GmailClassificationLabelFieldValues(BaseModel):
    """Model for ClassificationLabelFieldValue.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#classificationlabelfieldvalue
    """

    fieldId: str
    selection: str


class GmailClassificationLabelValues(BaseModel):
    """Model for ClassificationLabelValues.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message.ClassificationLabelValue
    """

    labelId: str
    fields: list[GmailClassificationLabelFieldValues]


class GmailMessageHeader(BaseModel):
    """Model for a message header.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message.Header
    """

    name: str
    value: str


class GmailMessagePartBody(BaseModel):
    """Model for MessagePartBody.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages.attachments#MessagePartBody
    """

    attachmentId: str | None = None
    size: int
    data: bytes | None = None


class GmailMessagePart(BaseModel):
    """Model for a message part.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message.MessagePart
    """

    partId: str
    mimeType: str
    filename: str
    headers: list[GmailMessageHeader]
    body: GmailMessagePartBody
    parts: "list[GmailMessagePart] | None" = None


class GMailMetadataMessagePart(BaseModel):
    """Model for a message part, only containing metadata.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message.MessagePart
    """

    mimeType: str
    headers: list[GmailMessageHeader]


class BaseGmailMessage(BaseModel):
    """Base model for an email message.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message
    """

    id: str
    threadId: str
    labelIds: list[str]
    snippet: str
    historyId: str
    internalDate: str
    sizeEstimate: int
    classificationLabelValues: GmailClassificationLabelValues | None = None
    raw: bytes | None = None
    payload: GmailMessagePart | GMailMetadataMessagePart | None = None


class GmailRawMessage(BaseGmailMessage):
    """Model for a raw email message.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message
    """

    raw: str


class GmailMessage(BaseGmailMessage):
    """Model for an email message.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message
    """

    payload: GmailMessagePart


class GMailMetadataMessage(BaseGmailMessage):
    """Model for a metadata-only email message.

    https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages#Message
    """

    payload: GMailMetadataMessagePart


class MessageIdentifier(BaseModel):
    """Message identifier stub from calling messages.list."""

    id: str
    threadId: str


class ListMessagesResponse(BaseModel):
    """Model representing the response from calling messages.list."""

    messages: list[MessageIdentifier]
    nextPageToken: str | None = None
    resultSizeEstimate: int


class FailedItemModel(BaseModel, arbitrary_types_allowed=True):
    """Model for a failed email item."""

    reason: str | None = None
    exception: Exception
    item: Any

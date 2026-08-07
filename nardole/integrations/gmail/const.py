"""Constants."""

from dataclasses import dataclass
from pathlib import Path

DOMAIN = "gmail"
GET_EMAILS_SERVICE = "get_emails"


@dataclass(frozen=True)
class DataPaths:
    """Paths for data files."""

    PROCESSING_PATH: Path = Path("processing")
    METADATA_PATH: Path = Path("meta")
    FAILED_EMAIL_PROCESSING: Path = Path(PROCESSING_PATH, "emails_failed_processing.json")
    LAST_PROCESS_TS: Path = Path(METADATA_PATH, "last_download.json")


DATA_DIRECTORIES = (
    DataPaths.PROCESSING_PATH,
    DataPaths.METADATA_PATH,
)

DOCUMENT_TEMPLATE = (
    "{% assign participants = doc.to | concat: doc.cc.size | concat: doc.bcc %}"
    "{% if participants.size > 1 %}A group email{%else%}An email{% endif %}"
    "from"
    "{{ doc.sender.name}} ({{ doc.sender.email_address }}),"
    "'{% if doc.subject %}Subject: {{ doc.subject }}, {% endif %}'"
    "{% if doc.attachments.size %}"
    "Attachments:"
    "{% for attachment in doc.attachments %}"
    "\n- {{ attachment.filename }} (MIME: {{ attachment.mime_type}})"
    "{% endfor %}"
    "{%endif%}"
)

INDEX_EMAILS = "gmail_emails"
INDEX_CONVERSATIONS = "gmail_conversations"

PRIMARY_KEY_EMAILS = "id"
PRIMARY_KEY_CONVERSATIONS = "thread_id"

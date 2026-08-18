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


class GmailClientError(Exception):
    """Exception occuring due to GMail API client."""


class GmailIntegrationError(Exception):
    """Exception occuring due to GMail integration."""

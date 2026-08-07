"""Constants."""

from enum import StrEnum
from pathlib import Path


class SupportedFeatures(StrEnum):
    """Supported features for integrations."""

    CREATE_INDEX = "create_index"  # Create indices
    MANAGE_INDEX = "manage_index"  # Manage integration-owned indices
    CONNECTED_INTEGRATION = "connected_integration"  # Can connect with indices owned by other integrations
    ADD_DOCUMENTS_TO_SELF = "add_documents_to_self"  # Add documents to owned indices
    ADD_CONTACTS = "add_contacts"  # Add contacts
    API = "api"  # API Endpoints
    USER_SERVICES = "user_services"  # Users can run services
    AI_TASKS = "ai_tasks"  # Includes features for AI tasks.
    PROACTIVE_REQUESTS = "proactive_requests"  # Includes features that allows the AI to initiate
    # requests to the user if permitted.

    PROACTIVE_ACTIONS = "proactive_actions"  # Includes features that allows the AI to perform
    # tasks without user input if permitted

    MANUAL_ACTIONS = "manual_actions"  # Includes features that allow the AI to perform
    # tasks with user approval


class ServicePermission(StrEnum):
    """Service permissions."""

    ALWAYS_ASK = "always_ask"
    ALWAYS_ALLOW = "always_allow"
    ALWAYS_DENY = "always_deny"
    UNSET = "unset"


class PermissionGrant(StrEnum):
    """Permission granted by user."""

    ALLOW = "allow"
    DENY = "deny"
    ALWAYS_ALLOW = "always_allow"
    ALWAYS_DENY = "always_deny"
    ALWAYS_DENY_ALL_MODELS = "always_deny_all_models"


class CallServiceStatus(StrEnum):
    """Service call status."""

    SUCCESS = "success"  # Service successfully called
    REQUIRES_APPROVAL = "requires_approval"  # Service call requires user approval
    FORBIDDEN = "forbidden"  # User set permissions to always deny
    DENIED = "denied"  # User denied service call
    REJECTED = "rejected"  # Service call rejected for any other reason
    FAILURE = "failure"  # Service call failed
    NOT_REGISTERED = "not_registered"  # Service not yet registered


DATA_DIR = Path("/", "app", "data")
STORE_PATH = DATA_DIR.joinpath(".store")
CONFIG_ENTRY_PATH = STORE_PATH.joinpath("config_entries.json")
INTEGRATION_DATA_DIR = DATA_DIR.joinpath("integrations")
CONFIG_PATH = Path("/", "config")
CONFIG_FILE = CONFIG_PATH.joinpath("config.yaml")
PERMISSIONS_FILE_PATH = STORE_PATH.joinpath("permissions.json")

INDEX_CONTACTS = "contact"
INDEX_EMAIL_ADDRESSES = "email_addresses"
INDEX_NAMES = "names"
INDEX_NICKNAMES = "nicknames"
INDEX_PHONE_NUMBERS = "phone_numbers"
INDEX_PHOTOS = "photos"
INDEX_URLS = "urls"

DEFAULT_STOP_WORDS = [
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "if",
    "in",
    "into",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "such",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "was",
    "will",
    "with",
]

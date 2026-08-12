"""Constants."""

from pathlib import Path

DATA_DIR = Path("/", "app", "data")
STORE_PATH = DATA_DIR.joinpath(".store")
CONFIG_ENTRY_PATH = STORE_PATH.joinpath("config_entries.json")
INTEGRATION_DATA_DIR = DATA_DIR.joinpath("integrations")
CONFIG_PATH = Path("/", "config")
CONFIG_FILE = CONFIG_PATH.joinpath("config.yaml")
PERMISSIONS_FILE_PATH = STORE_PATH.joinpath("permissions.json")
SAVE_FILE_PATH = DATA_DIR.joinpath("files")

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

ATTACHMENT_ENDPOINT = "/files"

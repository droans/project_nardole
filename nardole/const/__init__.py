"""Constants."""

from pathlib import Path

# Directory paths
DATA_DIR = Path("/", "app", "data")
STORE_PATH = DATA_DIR.joinpath(".store")
INTEGRATION_DATA_DIR = DATA_DIR.joinpath("integrations")
CONFIG_PATH = Path("/", "config")
SAVE_FILE_PATH = DATA_DIR.joinpath("files")

# File paths
CONFIG_FILE = CONFIG_PATH.joinpath("config.yaml")
CONFIG_ENTRY_PATH = STORE_PATH.joinpath("config_entries.json")
PERMISSIONS_FILE_PATH = STORE_PATH.joinpath("permissions.json")
FILE_MANAGER_DATA_PATH = STORE_PATH.joinpath("files.json")

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

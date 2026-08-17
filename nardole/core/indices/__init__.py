"""Project Nardole built-in indices."""

from .contacts import ContactsIndexer
from .email import EmailIndexer

__all__ = (
    "ContactsIndexer",
    "EmailIndexer",
)

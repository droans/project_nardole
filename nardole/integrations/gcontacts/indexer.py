"""Google Contacts integration."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from meilisearch import Client


class GContactsIndexer:
    """Class to manage Meilisearch indexing."""

    def __init__(
        self,
        meilisearch_client: "Client",
    ) -> None:
        """Initialize class."""
        self.meilisearch_client = meilisearch_client

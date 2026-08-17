"""Email index."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from meilisearch import Client


class EmailIndexer:
    """Project Nardole built-in email index."""

    def __init__(
        self,
        meilisearch_client: "Client",
    ) -> None:
        """Initialize class."""
        self._client = meilisearch_client

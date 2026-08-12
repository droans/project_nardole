"""GMail indexer."""

from typing import TYPE_CHECKING

from nardole.core.meilisearch.util import create_index

from .const import (
    DOCUMENT_TEMPLATE,
    INDEX_CONVERSATIONS,
    INDEX_EMAILS,
)
from .index_configs import create_conversations_index_config, create_email_index_config
from .models import ConversationModel, EmailModel, GMailConfig

if TYPE_CHECKING:
    from nardole.core.contacts import ContactsManager
    from nardole.core.nardole import Nardole


class GMailIndexer:
    """Class to manage indexing."""

    def __init__(
        self,
        config: GMailConfig,
        nardole: "Nardole",
        contacts_manager: "ContactsManager",
    ) -> None:
        """Initialize class."""
        self.config = config
        self.nardole = nardole
        self.meilisearch_client = nardole.meilisearch_client
        self.contacts_manager = contacts_manager

    def setup_indices(self) -> None:
        """Setup indices if not already set up."""
        all_indices = [idx.uid for idx in self.meilisearch_client.get_indexes()["results"]]

        if INDEX_EMAILS not in all_indices:
            email_embed_settings = self.nardole.create_embedder_settings(DOCUMENT_TEMPLATE)
            email_index_config = create_email_index_config(embedder_settings=email_embed_settings)
            create_index(
                client=self.nardole.meilisearch_client,
                index_config=email_index_config,
            )
            self.setup_embedder()

        if INDEX_CONVERSATIONS not in all_indices:
            conversations_index_config = create_conversations_index_config()
            create_index(
                client=self.nardole.meilisearch_client,
                index_config=conversations_index_config,
            )

    def setup_embedder(self) -> None:
        """Setup embedder if not already set."""
        model = self.nardole.create_embedder_settings(DOCUMENT_TEMPLATE)
        config = {
            model.model_name: {
                "source": "rest",
                "url": model.url,
                "apiKey": model.api_key,
                "dimensions": model.dimensions,
                "request": model.request,
                "response": model.response,
                "documentTemplate": model.document_template,
            },
        }
        self.meilisearch_client.index(INDEX_EMAILS).update_embedders(config)

    def import_messages_to_meilisearch(self, account_name: str, messages: list[EmailModel]) -> None:
        """Import messages into Meilisearch."""
        for message in messages:
            message.account_name = account_name
        self.meilisearch_client.index(INDEX_EMAILS).add_documents(
            [message.model_dump() for message in messages],
        )

    def import_conversations_to_meilisearch(
        self,
        account_name: str,
        conversations: list[ConversationModel],
    ) -> None:
        """Import conversations into Meilisearch."""
        for conversation in conversations:
            conversation.account_name = account_name
        self.meilisearch_client.index(INDEX_CONVERSATIONS).add_documents(
            [conversation.model_dump() for conversation in conversations],
        )

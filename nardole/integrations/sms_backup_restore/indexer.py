"""SMS Backup & Restore integration."""

from typing import TYPE_CHECKING

from nardole.core.meilisearch.util import create_index, embedder_exists, index_exists
from nardole.integrations.sms_backup_restore.integration_models import ConversationModel, MessageModel

from .const import DOCUMENT_TEMPLATE, INDEX_SMS_CONVERSATIONS, INDEX_SMS_MESSAGES
from .index_configs import (
    create_sms_conversations_index_config,
    create_sms_message_index_config,
)

if TYPE_CHECKING:
    from nardole.core import Nardole

    from .integration_models import SMSBackupAndRestoreConfigModel


class SMSBackupAndRestoreIndexer:
    """Class for managing Meilisearch indices."""

    def __init__(
        self,
        config: "SMSBackupAndRestoreConfigModel",
        nardole: "Nardole",
    ) -> None:
        """Initialize class."""
        self.config = config
        self.nardole = nardole
        self.meilisearch_client = nardole.meilisearch_client

    def setup_indices(self) -> None:
        """Setup indices if not already ready."""
        if not index_exists(self.meilisearch_client, INDEX_SMS_MESSAGES):
            embedder_settings = self.nardole.create_embedder_settings(DOCUMENT_TEMPLATE)
            config = create_sms_message_index_config(embedder_settings=embedder_settings)
            create_index(client=self.meilisearch_client, index_config=config)
        if not index_exists(self.meilisearch_client, INDEX_SMS_CONVERSATIONS):
            config = create_sms_conversations_index_config()
            create_index(client=self.meilisearch_client, index_config=config)
        self.setup_embedder()

    def setup_embedder(self) -> None:
        """Setup embedder for SMS messages index."""
        model = self.nardole.create_embedder_settings(DOCUMENT_TEMPLATE)
        api_key = model.api_key
        if api_key:
            api_key = api_key.get_secret_value()
        if embedder_exists(self.meilisearch_client, INDEX_SMS_MESSAGES, model):
            return
        config = {
            model.model_name: {
                "source": "rest",
                "url": model.url.encoded_string(),
                "apiKey": api_key,
                "dimensions": model.dimensions,
                "request": model.request,
                "response": model.response,
                "documentTemplate": model.document_template,
            },
        }
        self.meilisearch_client.index(INDEX_SMS_MESSAGES).update_embedders(config)

    def import_sms_messages(self, sms_messages: list[MessageModel]) -> None:
        """Import SMS messages into Meilisearch."""
        self.meilisearch_client.index(INDEX_SMS_MESSAGES).add_documents(
            documents=[msg.model_dump() for msg in sms_messages],
        )

    def import_sms_conversations(self, conversations: list[ConversationModel]) -> None:
        """Import SMS conversation records into Meilisearch."""
        self.meilisearch_client.index(INDEX_SMS_CONVERSATIONS).add_documents(
            documents=[conversation.model_dump() for conversation in conversations],
        )

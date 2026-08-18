"""Email index."""

from typing import TYPE_CHECKING, Literal

from nardole.const.email import INDEX_EMAIL_CONVERSATIONS, INDEX_EMAILS
from nardole.core.indices.email.configure import create_email_conversations_index_config, create_email_index_config
from nardole.core.indices.email.utils import generate_email_search_dict_from_model
from nardole.core.meilisearch.util import create_index, embedder_exists, index_exists, update_index_embedder_config
from nardole.models.indices.email import EmailConversationModel, EmailModel, EmailSearchRequest

if TYPE_CHECKING:
    from meilisearch import Client

    from nardole.models.indexing import EmbedderSettings


class EmailIndexer:
    """Project Nardole built-in email index."""

    def __init__(
        self,
        meilisearch_client: "Client",
        embedder_settings: "EmbedderSettings",
    ) -> None:
        """Initialize class."""
        self.client = meilisearch_client
        self.embedder_config = embedder_settings

    def initialize(self) -> None:
        """Initialize indexer."""
        self._email_index = self.client.index(INDEX_EMAILS)
        self._conversation_index = self.client.index(INDEX_EMAIL_CONVERSATIONS)

        if not index_exists(self.client, INDEX_EMAILS):
            email_index_configuration = create_email_index_config(embedder_settings=self.embedder_config)
            create_index(self.client, email_index_configuration)

        if not index_exists(self.client, INDEX_EMAIL_CONVERSATIONS):
            email_conversations_configuration = create_email_conversations_index_config()
            create_index(self.client, email_conversations_configuration)

        if not embedder_exists(self.client, INDEX_EMAILS, self.embedder_config):
            update_index_embedder_config(self._email_index, self.embedder_config)

    def import_emails(
        self,
        emails: list[EmailModel],
        import_conversations: bool = True,
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import emails into Meilisearch."""
        if not emails:
            return
        func = self._email_index.add_documents if add_or_update == "add" else self._email_index.update_documents
        func(
            [eml.model_dump() for eml in emails],
        )
        if not import_conversations:
            return
        self._import_conversations_from_emails(emails)

    def _import_conversations_from_emails(self, emails: list[EmailModel]) -> None:
        """Import/update conversations from emails."""
        conv_ids = list({eml.conversation_id for eml in emails})
        existing_convs = {conv.conversation_id: conv for conv in self.find_existing_conversations(conv_ids)}
        email_convs: dict[str, EmailConversationModel] = {}

        for eml in emails:
            conv_id = eml.conversation_id
            participants = eml.to + eml.cc + eml.bcc + [eml.sender]

            if conv_id not in email_convs:
                email_convs[conv_id] = EmailConversationModel(
                    conversation_id=conv_id,
                    participants=participants,
                    domain=eml.domain,
                    account=eml.account,
                )
                continue
            conversation = email_convs[conv_id]

            # Add email participants which aren't included in the conversation participants
            for participant in set(participants) - set(conversation.participants):
                conversation.participants.append(participant)

        import_conversationss: list[EmailConversationModel] = []
        for conv_id, conversation in email_convs.items():
            if conv_id not in existing_convs:
                import_conversationss.append(conversation)
                continue

            existing_conversation = existing_convs[conv_id]
            existing_participants = existing_conversation.participants
            conversation_participants = conversation.participants
            if existing_participants == conversation_participants:
                continue
            conversation.participants = list(set(existing_participants + conversation_participants))
            import_conversationss.append(conversation)

        self.import_conversations(import_conversationss)

    def find_existing_conversations(self, conversation_ids: list[str]) -> list[EmailConversationModel]:
        """Find all existing conversations."""
        conv_id_filter = ",".join(f"'{conv_id}'" for conv_id in conversation_ids)
        results = self._conversation_index.search(
            "",
            {"filter": f"conversation_id IN [{conv_id_filter}]"},
        )
        hits = results.get("hits", [])
        result = set()
        for hit in hits:
            conversation = EmailConversationModel.model_validate(hit)
            if conversation.conversation_id in conversation_ids:
                result.add(conversation)
        return list(result)

    def import_conversations(
        self,
        conversations: list[EmailConversationModel],
        add_or_update: Literal["add", "update"] = "add",
    ) -> None:
        """Import conversations into Meilisearch."""
        if not conversations:
            return
        func = (
            self._conversation_index.add_documents
            if add_or_update == "add"
            else self._conversation_index.update_documents
        )
        func([conversation.model_dump() for conversation in conversations])
        return

    def search_emails(
        self,
        search_config: EmailSearchRequest,
    ) -> list[EmailModel]:
        """Search for emails in Meilisearch."""
        search_opts = generate_email_search_dict_from_model(search_config)
        results = self._email_index.search(search_config.query, search_opts)
        hits = results.get("hits", [])
        return [EmailModel.model_validate(hit) for hit in hits]

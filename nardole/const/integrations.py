"""Integration constants."""

from enum import StrEnum


class SupportedFeatures(StrEnum):
    """Supported features for integrations."""

    # Create and manage indices
    INDEX = "index"

    # Integration has API endpoints.
    API = "api"

    """
        External indices.

        Support working with indices from other integrations.
    """
    # Query indices from other integrations
    QUERY_EXTERNAL_INDEX = "query_external_index"

    # Add documents to indices from other integrations
    ADD_DOCUMENTS_EXTERNAL_INDEX = "add_documents_external_index"

    # Manage the settings for an external index
    MANAGE_EXTERNAL_INDEX = "manage_external_index"

    """
        Built-in indices.

        Support working with indices from other integrations.
    """
    # Manage contacts
    #
    # Declaring support for MANAGE_CONTACTS is required for the ContactsIndexer
    # to be passed to the integration during setup.
    MANAGE_CONTACTS = "manage_contacts"

    # Manage Emails
    #
    # Declaring support for MANAGE_EMAILS is required for the EmailIndexer
    # to be passed to the integration during setup.
    MANAGE_EMAILS = "manage_emails"

    # Manage SMS Messages
    #
    # Declaring support for MANAGE_SMS is required for the SMSIndexer
    # to be passed to the integration during setup.
    MANAGE_SMS = "manage_sms"

    """
        Services

        Declare supported service types.
    """
    # Declare support for user-initiated services
    USER_SERVICES = "user_services"

    # Declare support for automated (non-AI) services
    AUTOMATED_SERVICES = "automated_services"

    # Declare support for AI-run services
    AI_SERVICES = "ai_services"

    """
        Proactivity

        Support features that don't require user input prior to running.
    """
    # Declare support for proactive notifications
    PROACTIVE_NOTIFICATIONS = "proactive_notifications"

    # Declare support for initiating conversations with the user
    INITIATE_CONVERSATION = "initiate_conversation"

    # Declare support for AI-run proactive actions
    #
    # While AI_SERVICES allows for AI models to run actions,
    # PROACTIVE_ACTIONS allows for AI to perform an action without any discussion with the user
    # IE - an email integration may allow for the AI to receive certain emails and reply to them without input.
    #
    # Requires AI_SERVICES support.
    PROACTIVE_ACTIONS = "proactive_actions"


class IntegrationType(StrEnum):
    """Integration types."""

    CONVERSATION_EMAIL = "conversation.email"
    CONVERSATION_TEXT_MESSAGES = "conversation.text_messages"
    CONVERSATION_CHATS = "conversation.chat"
    CONTACTS = "contacts"
    CALENDAR = "calendar"

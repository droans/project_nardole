"""Integration constants."""

from enum import StrEnum


class SupportedFeatures(StrEnum):
    """Supported features for integrations."""

    # Create indices
    CREATE_INDEX = "create_index"

    # Manage integration-owned indices
    MANAGE_INDEX = "manage_index"

    # Can connect with indices owned by other integrations
    CONNECTED_INTEGRATION = "connected_integration"
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


class IntegrationType(StrEnum):
    """Integration types."""

    CONVERSATION_EMAIL = "conversation.email"
    CONVERSATION_TEXT_MESSAGES = "conversation.text_messages"
    CONVERSATION_CHATS = "conversation.chat"
    CONTACTS = "contacts"
    CALENDAR = "calendar"

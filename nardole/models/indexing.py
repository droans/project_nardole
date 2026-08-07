"""Models related to indexing."""

from nardole.models.config import EmbedderConfig


class EmbedderSettings(EmbedderConfig):
    """Model for setup embedder config."""

    document_template: str

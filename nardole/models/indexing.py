"""Models related to indexing."""

from .config import EmbedderConfig


class EmbedderSettings(EmbedderConfig):
    """Model for setup embedder config."""

    document_template: str

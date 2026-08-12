"""Models related to indexing."""

from pydantic import BaseModel

from .config import EmbedderConfig


class EmbedderSettings(EmbedderConfig):
    """Model for setup embedder config."""

    document_template: str


class IndexFileModel(BaseModel):
    """Model representing a single index file."""

    file_name: str
    content_type: str
    src: str

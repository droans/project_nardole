"""Models related to indexing."""

from typing import Annotated, Any

import phonenumbers
from pydantic import BaseModel, Field
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

from .config import EmbedderConfig


class EmbedderSettings(EmbedderConfig):
    """Model for setup embedder config."""

    document_template: str


class IndexFileModel(BaseModel):
    """Model representing a single index file."""

    domain: str
    file_name: str
    content_type: str
    uid: str


E164NumberType = Annotated[str | phonenumbers.PhoneNumber, PhoneNumberValidator(number_format="E164")]


class BaseSearchRequest(BaseModel):
    """Base model for a search request."""

    query: str = ""
    offset: int = 0
    limit: int = 20
    page: int | None = None
    hits_per_page: int | None = None
    semantic_ratio: float = Field(default=0.5, le=1, ge=0)
    attributes_to_retrieve: list[str] | None = None
    attributes_to_crop: list[str] | None = None
    crop_length: int | None = None
    crop_marker: str | None = None
    attributes_to_highlight: list[str] | None = None
    highlight_pre_tag: str | None = None
    highlight_post_tag: str | None = None
    kwargs: dict[str, Any] = {}

"""Index setup chat config model."""

from typing import Literal

from pydantic import BaseModel, Field

from nardole.const import DEFAULT_STOP_WORDS
from nardole.models.indexing import EmbedderSettings


class IndexChatSearchParametersConfig(BaseModel):
    """Model for search parameters."""

    semantic_ratio: float | None = None
    limit: int | None = None
    sort: list[str]
    distinct: list[str]
    matching_strategy: Literal["last", "all", "frequency"] | None = None
    search_attributes: list[str] | None
    ranking_score_threshold: float | None = Field(default=None, ge=0, le=1)


class IndexChatConfig(BaseModel):
    """Model for the chat config for an index."""

    description: str
    default_document_template: str | None = None
    search_parameters: IndexChatSearchParametersConfig | None = None


class FilterableAttributesConfig(BaseModel):
    """Advanced configuration for filterable attributes."""

    attribute_patterns: list[str]
    enable_facet_search: bool | None = None
    enable_equality_filter: bool | None = None
    enable_comparison_filter: bool | None = None
    max_values_per_facet: int | None = None
    sort_facet_values_by: dict[str, Literal["alpha", "count"]] | None = None


class IndexAttributesConfig(BaseModel):
    """Config for index attributes."""

    # Attributes that can be filtered.
    filterable_attributes: list[str | FilterableAttributesConfig] | None = None

    # Attributes that can be checked.
    searchable_attributes: list[str] | None = None

    # Attributes that can be sorted.
    sortable_attributes: list[str] | None = None

    # Attributes that can be returned.
    displayed_attributes: list[str] | None = None

    # When set, if multiple items share the same distinct attribute,
    #  only one of them will be returned.
    distinct_attribute: str | None = None


class IndexAttributesForeignKeyConfig(BaseModel):
    """Config for foreign key settings for an index."""

    foreign_key_uid: str
    field_name: str


class IndexConfig(BaseModel):
    """Model for an index."""

    index_uid: str
    primary_key: str
    embedder: EmbedderSettings | None = None
    chat: IndexChatConfig | None = None
    foreign_keys: list[IndexAttributesForeignKeyConfig] | None = None
    attributes: IndexAttributesConfig
    stop_words: list[str] = DEFAULT_STOP_WORDS


class IndexFileModel(BaseModel):
    """Model representing a single index file."""

    file_name: str
    content_type: str
    src: str

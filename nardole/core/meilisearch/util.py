"""Utility functions for Meilisearch."""

import time
from typing import TYPE_CHECKING, Literal

from meilisearch.index import Index
from meilisearch.models.embedders import RestEmbedder

from nardole.models.indexing import EmbedderSettings
from nardole.models.indices.settings import (
    FilterableAttributesConfig,
    IndexAttributesForeignKeyConfig,
    IndexChatConfig,
    IndexConfig,
)

if TYPE_CHECKING:
    from meilisearch import Client


def index_exists(client: "Client", index_uid: str) -> bool:
    """Test if an index exists."""
    request = client.get_indexes()
    indices = request["results"]
    return any(index.uid == index_uid for index in indices)


def update_index_primary_key(idx: Index, primary_key: str) -> None:
    """Update the primary key for an index."""
    idx.update(primary_key=primary_key)


def update_index_embedder_config(idx: Index, embedder_config: EmbedderSettings) -> None:
    """Update the embedder config for an index."""
    embed_config = {
        embedder_config.model_name: {
            "source": "rest",
            "url": embedder_config.url,
            "apiKey": embedder_config.api_key,
            "dimensions": embedder_config.dimensions,
            "request": embedder_config.request,
            "response": embedder_config.response,
            "documentTemplate": embedder_config.document_template,
        },
    }
    idx.update_embedders(embed_config)


def update_index_chat_config(idx: Index, chat_config: IndexChatConfig) -> None:
    """Update the chat config for an index."""
    conf = {
        "description": chat_config.description,
        "documentTemplate": chat_config.default_document_template,
    }
    if chat_config.search_parameters is not None:
        params = chat_config.search_parameters
        search_params = {}
        if params.semantic_ratio is not None:
            search_params["hybrid"] = {
                "embedder": "default",
                "semanticRatio": params.semantic_ratio,
            }
        if params.limit is not None:
            search_params["limit"] = params.limit
        if params.sort is not None:
            search_params["sort"] = params.sort
        if params.distinct is not None:
            search_params["distinct"] = params.distinct
        if params.matching_strategy is not None:
            search_params["matching_strategy"] = params.matching_strategy
        if params.search_attributes is not None:
            search_params["attributesToSearchOn"] = params.search_attributes
        if params.ranking_score_threshold is not None:
            search_params["rankingScoreThreshold"] = params.ranking_score_threshold
        conf["searchParameters"] = search_params

    idx.update_settings({"chat": conf})


def update_index_foreign_keys(
    idx: Index,
    foreign_keys: list[IndexAttributesForeignKeyConfig],
    replace_or_append: Literal["replace", "append"] = "replace",
) -> None:
    """Update the foreign keys for an index."""
    keys = [
        {
            "foreignIndexUid": fk.foreign_key_uid,
            "fieldName": fk.field_name,
        }
        for fk in foreign_keys
    ]
    if replace_or_append == "append":
        keys.extend(idx.get_foreign_keys())
    idx.reset_foreign_keys()
    idx.update_foreign_keys(keys)


def update_index_stop_words(idx: Index, stop_words: list[str]) -> None:
    """Update the chat config for an index."""
    idx.update_stop_words(stop_words)


def _create_filterable_attributes_config(attributes: FilterableAttributesConfig | str) -> dict | str:
    """Create the config for Filterable Attributes from the model."""
    if isinstance(attributes, str):
        return attributes
    return {
        "attributePatterns": attributes.attribute_patterns,
        "features": {
            "facetSearch": attributes.enable_facet_search,
            "filter": {
                "equality": attributes.enable_equality_filter,
                "comparison": attributes.enable_comparison_filter,
            },
        },
    }


def update_index_filterable_attributes(idx: Index, attributes: list[str | FilterableAttributesConfig] | None) -> None:
    """Update the filterable attributes for an index. Pass None to reset."""
    if not attributes:
        idx.reset_filterable_attributes()
        return
    attrs = [_create_filterable_attributes_config(attribute) for attribute in attributes]
    idx.update_filterable_attributes(attrs)  # ty: ignore[invalid-argument-type]


def update_index_searchable_attributes(idx: Index, attributes: list[str] | None) -> None:
    """Update the searchable attributes for an index. Pass None to reset."""
    if attributes:
        idx.update_searchable_attributes(attributes)
    else:
        idx.reset_searchable_attributes()


def update_index_sortable_attributes(idx: Index, attributes: list[str] | None) -> None:
    """Update the sortable attributes for an index. Pass None to reset."""
    if attributes:
        idx.update_filterable_attributes(attributes)
    else:
        idx.reset_sortable_attributes()


def update_index_displayed_attributes(idx: Index, attributes: list[str] | None) -> None:
    """Update the displayed attributes for an index. Pass None to reset."""
    if attributes:
        idx.update_displayed_attributes(attributes)
    else:
        idx.reset_displayed_attributes()


def update_index_distinct_attributes(idx: Index, attributes: str | None) -> None:
    """Update the distinct attribute for an index. Pass None to reset."""
    if attributes:
        idx.update_distinct_attribute(attributes)
    else:
        idx.reset_distinct_attribute()


def create_index(client: "Client", index_config: IndexConfig) -> None:
    """Create an index from the passed configuration. Does NOT set embedder settings."""
    if index_exists(client=client, index_uid=index_config.index_uid):
        return
    primary_key = index_config.primary_key

    client.create_index(index_config.index_uid, options={"primaryKey": primary_key})

    # Force a sleep to give time for the task to complete.
    time.sleep(0.2)
    idx = client.index(index_config.index_uid)
    if index_config.chat:
        update_index_chat_config(idx, index_config.chat)

    if index_config.foreign_keys:
        update_index_foreign_keys(idx, index_config.foreign_keys)
    if index_config.stop_words:
        update_index_stop_words(idx, index_config.stop_words)

    attrs = index_config.attributes

    if attrs.filterable_attributes:
        update_index_filterable_attributes(idx, attrs.filterable_attributes)
    if attrs.sortable_attributes:
        update_index_sortable_attributes(idx, attrs.sortable_attributes)
    if attrs.searchable_attributes:
        update_index_searchable_attributes(idx, attrs.searchable_attributes)
    if attrs.displayed_attributes:
        update_index_displayed_attributes(idx, attrs.displayed_attributes)
    if attrs.distinct_attribute:
        update_index_distinct_attributes(idx, attrs.distinct_attribute)


def embedder_exists(
    meilisearch_client: "Client",
    index_uid: str,
    embedder_config: EmbedderSettings,
) -> bool:
    """Test if an embedder is already setup."""
    if not index_exists(client=meilisearch_client, index_uid=index_uid):
        return False
    index = meilisearch_client.index(index_uid)
    embedders = index.get_embedders()
    if not embedders:
        return False
    current_embedder = embedders.embedders.get(embedder_config.model_name)
    if not current_embedder or not isinstance(current_embedder, RestEmbedder):
        return False
    cur_template = current_embedder.document_template
    if cur_template:
        cur_template = cur_template.strip().replace("\n", "").replace("\r", "")
    new_template = embedder_config.document_template.strip().replace("\n", "").replace("\r", "")
    return all(
        [
            cur_template == new_template,
            current_embedder.url == embedder_config.url,
            current_embedder.dimensions == embedder_config.dimensions,
            current_embedder.request == embedder_config.request,
            current_embedder.response == embedder_config.response,
        ],
    )

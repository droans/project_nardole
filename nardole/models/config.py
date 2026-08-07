"""Project Nardole config."""

from pydantic import BaseModel, HttpUrl, SecretStr

from nardole.models.integrations.config_entry import BaseIntegrationConfigModel


class EmbedderConfig(BaseModel):
    """Model for the embedder config."""

    model_name: str
    url: HttpUrl
    api_key: str | None = None
    dimensions: int

    # See https://www.meilisearch.com/docs/capabilities/hybrid_search/how_to/configure_rest_embedder
    request: dict
    response: dict


class APIConfig(BaseModel):
    """API Configuration."""

    host: str = "127.0.0.1"
    port: int = 8000
    allowed_origins: list[str] = ["*"]


class MeilisearchConfig(BaseModel):
    """Model for Meilisearch config."""

    url: HttpUrl
    api_key: SecretStr | None = None
    embedder: EmbedderConfig


class ConfigModel(BaseModel):
    """Model for the user config."""

    api: APIConfig
    meilisearch: MeilisearchConfig
    integrations: list[BaseIntegrationConfigModel]

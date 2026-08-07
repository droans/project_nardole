"""Project Nardole config."""

from pydantic import BaseModel, HttpUrl, SecretStr

from nardole.models.integrations.config_entry import BaseIntegrationConfigModel


class APIConfig(BaseModel):
    """API Configuration."""

    host: str = "127.0.0.1"
    port: int = 8000
    allowed_origins: list[str] = ["*"]


class MeilisearchConfig(BaseModel):
    """Model for Meilisearch config."""

    url: HttpUrl
    api_key: SecretStr | None = None


class ConfigModel(BaseModel):
    """Model for the user config."""

    api: APIConfig
    meilisearch: MeilisearchConfig
    integrations: list[BaseIntegrationConfigModel]

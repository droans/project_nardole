"""User config entry for an integration."""

from pydantic import BaseModel, ConfigDict


class BaseIntegrationConfigModel(BaseModel):
    """Base Model for integration configuration."""

    model_config = ConfigDict(extra="allow")
    domain: str

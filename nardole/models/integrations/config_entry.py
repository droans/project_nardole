"""User config entry for an integration."""

from pydantic import BaseModel


class BaseIntegrationConfigModel(BaseModel):
    """Base Model for integration configuration."""

    domain: str

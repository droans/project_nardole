"""Models for an integration manifest."""

from pydantic import BaseModel

from nardole.const.integrations import IntegrationType, SupportedFeatures


class IntegrationManifestIndexConfig(BaseModel):
    """Model for an index config for an integration manifest."""


class IntegrationManifest(BaseModel):
    """Integration manifest model."""

    # Name of integration
    name: str
    # Description of integration
    description: str

    # Unique domain for integration, used in user configs
    domain: str
    supported_features: list[SupportedFeatures]
    integration_types: list[IntegrationType]

    requirements: list[str] = []
    connected_indices: list[str] = []

"""Project Nardole core module."""

import asyncio
from pathlib import Path

import yaml
from meilisearch import Client

from nardole.const import (
    CONFIG_ENTRY_PATH,
    CONFIG_FILE,
    FILE_MANAGER_DATA_PATH,
    INTEGRATION_DATA_DIR,
    PERMISSIONS_FILE_PATH,
    SAVE_FILE_PATH,
)
from nardole.core.file_manager import FileManager
from nardole.models.config import ConfigModel
from nardole.models.indexing import EmbedderSettings

from .registry.config_entries import ConfigEntryRegistry, IntegrationRegistry
from .registry.services import ServiceRegistry


class Nardole:
    """Root object for Project Nardole."""

    config_entry_registry: ConfigEntryRegistry
    service_registry: ServiceRegistry
    integration_registry: IntegrationRegistry

    def __init__(
        self,
        config_file: Path | str = CONFIG_FILE,
    ) -> None:
        """Initialize class."""
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()

        if isinstance(config_file, str):
            config_file = Path(config_file)

        self.config = load_config_from_path(config_file=config_file)

    def initialize(
        self,
        config_entry_json_path: Path | str = CONFIG_ENTRY_PATH,
        permissions_json_path: Path | str = PERMISSIONS_FILE_PATH,
        file_manager_json_path: Path | str = FILE_MANAGER_DATA_PATH,
        integration_data_path: Path | str = INTEGRATION_DATA_DIR,
        saved_file_path: Path | str = SAVE_FILE_PATH,
    ) -> None:
        """Initialize Nardole."""
        meilisearch_conf = self.config.meilisearch
        api_key = meilisearch_conf.api_key.get_secret_value() if meilisearch_conf.api_key is not None else None
        self.meilisearch_client = Client(url=meilisearch_conf.url.unicode_string(), api_key=api_key)

        if isinstance(config_entry_json_path, str):
            config_entry_json_path = Path(config_entry_json_path)
        if isinstance(integration_data_path, str):
            integration_data_path = Path(integration_data_path)
        if isinstance(saved_file_path, str):
            saved_file_path = Path(saved_file_path)
        if isinstance(file_manager_json_path, str):
            file_manager_json_path = Path(file_manager_json_path)

        self.integration_registry = IntegrationRegistry()
        self.integration_registry.register_integrations()
        self.config_entry_registry = ConfigEntryRegistry(
            entries_json_path=config_entry_json_path,
            integration_data_path=integration_data_path,
            nardole=self,
        )
        self.service_registry = ServiceRegistry(
            permission_file_path=permissions_json_path,
        )
        self.file_manager = FileManager(nardole=self, file_directory=saved_file_path, data_path=file_manager_json_path)
        self.config_entry_registry.load_from_entries()
        self.config_entry_registry.load_from_config(self.config.integrations)

    def create_embedder_settings(self, document_template: str) -> EmbedderSettings:
        """Create the embedder settings for an index."""
        return EmbedderSettings(
            **self.config.meilisearch.embedder.model_dump(),
            document_template=document_template,
        )


def load_config_from_path(config_file: Path | str) -> ConfigModel:
    """Retrieve the Project Nardole config."""
    with open(config_file) as f:
        raw_config = yaml.safe_load(f)
    return ConfigModel.model_validate(raw_config)

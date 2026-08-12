"""Project Nardole core module."""

import asyncio
from pathlib import Path

import magic
import yaml
from meilisearch import Client

from nardole.const import ATTACHMENT_ENDPOINT, CONFIG_ENTRY_PATH, PERMISSIONS_FILE_PATH, SAVE_FILE_PATH
from nardole.models.config import ConfigModel
from nardole.models.indexing import EmbedderSettings, IndexFileModel

from .registry.config_entries import ConfigEntryRegistry, IntegrationRegistry
from .registry.services import ServiceRegistry


class Nardole:
    """Root object for Project Nardole."""

    config_entry_registry: ConfigEntryRegistry
    service_registry: ServiceRegistry
    integration_registry: IntegrationRegistry

    def __init__(
        self,
        config_file: Path | str = CONFIG_ENTRY_PATH,
        config_entry_json: Path | str = CONFIG_ENTRY_PATH,
    ) -> None:
        """Initialize class."""
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()

        if isinstance(config_entry_json, str):
            config_entry_json = Path(config_entry_json)

        if isinstance(config_file, str):
            config_file = Path(config_file)

        self.config = load_config_from_path(config_file=config_file)

    def initialize(
        self,
        config_entry_json_path: Path | str = CONFIG_ENTRY_PATH,
        permissions_json_path: Path | str = PERMISSIONS_FILE_PATH,
    ) -> None:
        """Initialize Nardole."""
        meilisearch_conf = self.config.meilisearch
        api_key = meilisearch_conf.api_key.get_secret_value() if meilisearch_conf.api_key is not None else None
        self.meilisearch_client = Client(url=meilisearch_conf.url.unicode_string(), api_key=api_key)

        if isinstance(config_entry_json_path, str):
            config_entry_json_path = Path(config_entry_json_path)

        self.integration_registry = IntegrationRegistry()
        self.integration_registry.register_integrations()
        self.config_entry_registry = ConfigEntryRegistry(
            entries_json_path=config_entry_json_path,
            nardole=self,
        )
        self.service_registry = ServiceRegistry(
            permission_file_path=permissions_json_path,
        )
        self.config_entry_registry.load_from_entries()

    def create_embedder_settings(self, document_template: str) -> EmbedderSettings:
        """Create the embedder settings for an index."""
        return EmbedderSettings.model_validate(
            {"document_template": document_template},
            **self.config.meilisearch.embedder.model_dump(),
        )


def load_config_from_path(config_file: Path | str) -> ConfigModel:
    """Retrieve the Project Nardole config."""
    with open(config_file) as f:
        raw_config = yaml.safe_load(f)
    return ConfigModel.model_validate(raw_config)


def save_attachment(unique_id: str, data: str | bytes) -> IndexFileModel:
    """Save down a single attachment."""
    content_type = magic.from_buffer(data)
    mime = magic.from_buffer(data, mime=True)
    suffix = mime.split("/")[-1]
    fname = f"{unique_id}.{suffix}"
    if not SAVE_FILE_PATH.exists():
        SAVE_FILE_PATH.mkdir()
    file_path = SAVE_FILE_PATH.joinpath(fname)
    if not file_path.exists():
        open_mode = "wb" if isinstance(data, bytes) else "w"
        with open(fname, open_mode) as f:
            f.write(data)
    return IndexFileModel(
        file_name=fname,
        content_type=content_type,
        src=f"{ATTACHMENT_ENDPOINT}/{fname}",
    )

"""Config entry registry."""

import hashlib
import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

from nardole.const.integrations import SupportedFeatures
from nardole.core.indices.contacts import ContactsIndexer
from nardole.core.registry.util import install_manifest_packages, load_module_from_path
from nardole.exceptions import ConfigEntryLoadError
from nardole.models.integrations.config_entry import BaseIntegrationConfigModel
from nardole.models.nardole.registry import (
    ConfigEntry,
    LoadedIntegration,
    RegisteredIntegration,
    UnregisteredConfigEntry,
)

if TYPE_CHECKING:
    from nardole.core.nardole import Nardole

logger = logging.getLogger(__name__)


class ConfigEntryRegistry:
    """Config Entry Registry."""

    def __init__(
        self,
        entries_json_path: Path,
        integration_data_path: Path,
        nardole: "Nardole",
    ) -> None:
        """Initialize class."""
        self.config_entries: dict[str, LoadedIntegration] = {}
        self.nardole = nardole
        self._entries_path = entries_json_path
        self._integration_data_path = integration_data_path
        self._contacts_manager = ContactsIndexer(meilisearch_client=self.nardole.meilisearch_client)

    def load_config_entry(self, config_entry: UnregisteredConfigEntry) -> LoadedIntegration:
        """Load a config entry."""
        integration = config_entry.integration
        manifest = integration.manifest
        msg = f"Loading integration {manifest.domain}..."
        logger.debug(msg)
        if manifest.requirements:
            install_manifest_packages(manifest)

        module_path = integration.module_path
        data_dir = self._integration_data_path.joinpath(manifest.domain)
        entry = ConfigEntry(
            integration=config_entry.integration,
            user_config=config_entry.user_config,
            data_directory=data_dir,
        )
        try:
            module = load_module_from_path(module_path=module_path)
        except Exception as e:
            msg = f"Failed to load integration {manifest.domain} at path {module_path}"
            logger.exception(msg)
            raise ConfigEntryLoadError(msg) from e

        setup_fn = getattr(module, "setup_from_config_entry", None)
        if setup_fn is None:
            msg = f"Failed to get setup function for integration {manifest.name}"
            logger.error(msg)
            raise ConfigEntryLoadError(msg)
        if not isinstance(setup_fn, Callable):
            msg = (
                "Expected setup_from_config_entry to be a function"
                f" for integration {manifest.domain}, got type {type(setup_fn)} instead."
            )
            logger.error(msg)
            raise ConfigEntryLoadError(msg)

        setup_kwargs = {
            "nardole": self.nardole,
            "config_entry": entry,
        }

        if SupportedFeatures.ADD_CONTACTS in manifest.supported_features:
            setup_kwargs["contacts_manager"] = self._contacts_manager
        try:
            setup_result = setup_fn(**setup_kwargs)
        except Exception as e:
            msg = (
                "Received exception loading config entry ID"
                f" {integration.entry_id} for integration {manifest.domain}: {e}"
            )
            logger.exception(msg)
            raise ConfigEntryLoadError(msg) from e

        entry = LoadedIntegration(
            integration=config_entry.integration,
            user_config=config_entry.user_config,
            instance=setup_result,
        )
        self.config_entries[integration.entry_id] = entry
        return entry

    def load_from_config(self, config_entries: list[BaseIntegrationConfigModel]) -> None:
        """Load config entries from the config file."""
        integration_registry = self.nardole.integration_registry
        loaded_new_entries = False
        for entry in config_entries:
            entry_id = hashlib.sha224(entry.model_dump_json().encode()).hexdigest()
            if entry_id not in self.config_entries:
                loaded_new_entries = True
                integration = integration_registry.integrations.get(entry.domain)
                if not integration:
                    msg = f"Cannot find integration for domain {entry.domain}"
                    raise ConfigEntryLoadError(msg)
                registered_integration = RegisteredIntegration(
                    manifest=integration.manifest,
                    module_path=integration.module_path,
                    entry_id=entry_id,
                )
                config_entry = UnregisteredConfigEntry(
                    integration=registered_integration,
                    user_config=entry.model_dump(),
                )
                self.load_config_entry(config_entry=config_entry)
        if loaded_new_entries:
            processed = []
            for entry in self.config_entries.values():
                dumped = entry.model_dump_json(exclude={"instance"})
                processed.append(dumped)
            json_data = ", \n    ".join(processed)
            with open(self._entries_path, "w") as f:
                f.write(f"[\n    {json_data}\n]")

    def load_from_entries(self) -> None:
        """Load config from entries."""
        if not self._entries_path.exists():
            _create_config_entries_file(config_entry_path=self._entries_path, overwrite=True)
        with open(self._entries_path) as f:
            raw_entries = json.loads(f.read())
        all_entries = [UnregisteredConfigEntry.model_validate(entry) for entry in raw_entries]
        [self.load_config_entry(entry) for entry in all_entries]

    def get_config_entry(self, config_entry_id: str) -> LoadedIntegration:
        """Retrieve a config entry."""
        config_entry = self.config_entries.get(config_entry_id)
        if config_entry is None:
            msg = f"No config entry found with ID {config_entry_id}"
            raise ConfigEntryLoadError(msg)
        return config_entry


def _create_config_entries_file(config_entry_path: Path, overwrite: bool = False) -> None:
    """Create the config entries file."""
    if not (parent := config_entry_path.parent).exists():
        parent.mkdir(parents=True)
    config_entry_path.touch(mode=432, exist_ok=overwrite)
    with open(config_entry_path, "w") as f:
        f.write("[]")

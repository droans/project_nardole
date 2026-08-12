"""Config entry registry."""

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING

from nardole.const import DATA_DIR
from nardole.const.integrations import SupportedFeatures
from nardole.core.contacts import ContactsManager
from nardole.core.registry.util import install_manifest_packages, load_module_from_path
from nardole.exceptions import ConfigEntryLoadError
from nardole.models.nardole.registry import ConfigEntry, LoadedIntegration, UnregisteredConfigEntry

if TYPE_CHECKING:
    from nardole.core.nardole import Nardole

logger = logging.getLogger(__name__)


class ConfigEntryRegistry:
    """Config Entry Registry."""

    def __init__(
        self,
        entries_json_path: Path,
        nardole: "Nardole",
    ) -> None:
        """Initialize class."""
        self.config_entries: dict[str, LoadedIntegration] = {}
        self.nardole = nardole
        self._entries_path = entries_json_path
        self._contacts_manager = ContactsManager(meilisearch_client=self.nardole.meilisearch_client)

    def load_config_entry(self, config_entry: UnregisteredConfigEntry) -> LoadedIntegration:
        """Load a config entry."""
        integration = config_entry.integration
        manifest = integration.manifest
        msg = f"Loading integration {manifest.domain}..."
        logger.debug(msg)
        if manifest.requirements:
            install_manifest_packages(manifest)

        module_path = integration.module_path
        data_dir = DATA_DIR.joinpath(manifest.domain)
        config_entry = ConfigEntry.model_validate(
            {"data_directory": data_dir},
        )
        try:
            module = load_module_from_path(module_path=module_path)
        except Exception as e:
            msg = f"Failed to load integration {manifest.domain} at path {module_path}"
            logger.exception(msg)
            raise ConfigEntryLoadError(msg) from e

        setup_fn = getattr(module, "setup_from_config_entry", None)
        if setup_fn is None:
            msg = f"Failed to get setup function for integration {manifest.description}"
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
            "config_entry": config_entry,
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

        entry = LoadedIntegration(
            **config_entry.integration.model_dump(),
            instance=setup_result,
        )
        self.config_entries[integration.entry_id] = entry
        return entry

    def load_from_entries(self) -> None:
        """Load config from entries."""
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

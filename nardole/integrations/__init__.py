"""Integrations."""

import logging
import os
from pathlib import Path

import yaml

from nardole.exceptions import IntegrationRegistrationError
from nardole.models.integrations.manifest import IntegrationManifest
from nardole.models.nardole.registry import Integration

logger = logging.getLogger(__name__)


def get_integrations_for_registry() -> list[Integration]:
    """Return all the integrations."""
    manifests = []
    manifest_files = get_manifest_paths()
    for manifest_file in manifest_files:
        try:
            manifests.append(
                Integration(
                    manifest=load_manifest(manifest_file),
                    module_path=manifest_file,
                ),
            )
        except Exception as e:
            msg = f"Received exception loading manifest file {manifest_file}"
            logger.exception(msg)
            raise IntegrationRegistrationError(msg) from e
    return manifests


def load_manifest(manifest_path: Path) -> IntegrationManifest:
    """Retrieve the manifest for an integration."""
    with open(manifest_path) as f:
        raw_manifest = yaml.safe_load(f)
    return IntegrationManifest.model_validate(raw_manifest)


def get_manifest_paths() -> list[Path]:
    """Retrieve the paths of all the integrations."""
    return [
        Path(integration_dir, "manifest.yaml")
        for integration_dir, _subdirs, integration_files in os.walk(__path__[0])
        if "manifest.yaml" in integration_files
    ]

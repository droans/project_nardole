"""Registry utility functions."""

import importlib.util
import logging
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from subprocess import PIPE, Popen
from types import ModuleType
from urllib.parse import urlparse

from packaging.requirements import InvalidRequirement, Requirement

from nardole.models.integrations.manifest import IntegrationManifest

logger = logging.getLogger(__name__)


def load_module_from_path(module_path: Path) -> ModuleType:
    """Load a single module from path."""
    spec = importlib.util.spec_from_file_location("instance", module_path)
    assert spec
    return importlib.util.module_from_spec(spec)


def _install(args: list[str]) -> str | None:
    """Run the passed install command."""
    with Popen(  # noqa: S603
        args,
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=False,
    ) as process:
        _, stderr = process.communicate()
        if process.returncode != 0:
            return stderr.decode("utf-8").lstrip().strip()
    return None


def parse_requirement(requirement_str: str) -> Requirement | None:
    """Parse a requirement string as a Requirement object."""
    try:
        return Requirement(requirement_string=requirement_str)
    except InvalidRequirement:
        if "#" not in requirement_str:
            msg = f"Invalid requirement '{requirement_str}'"
            logger.error(msg)  # noqa: TRY400
            return None
        try:
            return Requirement(urlparse(requirement_str).fragment)
        except InvalidRequirement:
            msg = f"Invalid requirement '{requirement_str}'"
            logger.error(msg)  # noqa: TRY400
            return None


def install_package(requirement: Requirement) -> None:
    """Install a dependency integration from the manifest package string."""
    msg = f"Installing requirement: `{requirement.name}`"
    logger.info(msg)
    args = [
        sys.executable,
        "-m",
        "uv",
        "pip",
        "install",
        "--quiet",
        str(requirement),
    ]
    msg = f"Using argument: `{' '.join(args)}`"
    _install(args)


def package_is_installed(requirement: Requirement) -> bool:
    """Check if a package is already installed."""
    if not requirement:
        return False
    try:
        if (installed_version := version(requirement.name)) is None:
            return False
        if requirement.url:
            # Can't validate URL requirement versions, force reprocess
            return False
        return requirement.specifier.contains(installed_version, prereleases=True)
    except PackageNotFoundError:
        return False


def install_manifest_packages(manifest: IntegrationManifest) -> None:
    """Install all the packages from an integration manifest."""
    msg = f"Installing dependencies for domain {manifest.domain}"
    for requirement_str in manifest.requirements:
        msg = f"Attempting installation of {requirement_str}."
        logger.debug(msg)
        requirement = parse_requirement(requirement_str=requirement_str)
        if not requirement:
            msg = (
                f"Could not parse requirement for {manifest.domain}: "
                f"`{requirement_str}` is not a valid requirement string."
            )
            logger.error(msg)
            continue
        if package_is_installed(requirement=requirement):
            msg = f"Package {requirement.name} is already installed."
            logger.debug(msg)
            continue
        install_package(requirement=requirement)

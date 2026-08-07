"""Registry utility functions."""

import importlib.util
from pathlib import Path
from types import ModuleType


def load_module_from_path(module_path: Path) -> ModuleType:
    """Load a single module from path."""
    spec = importlib.util.spec_from_file_location("instance", module_path)
    assert spec
    return importlib.util.module_from_spec(spec)

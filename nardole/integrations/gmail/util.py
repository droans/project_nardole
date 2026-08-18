"""Utility functions."""

import datetime
import json
from pathlib import Path

from nardole.integrations.gmail.const import DataPaths
from nardole.integrations.gmail.models import EmailFilter


def get_last_process_datetime_for_account_and_filters(
    data_directory: Path,
    account_name: str,
    filters: EmailFilter | None,
) -> datetime.datetime:
    """Retrieve the latest processing time for the given account and filters."""
    filter_id = filters.unique_id if filters else None
    path = Path(data_directory, DataPaths.LAST_PROCESS_TS)
    if not path.exists():
        path.touch()
        with open(path, "w") as f:
            f.write("{}")

    with open(path) as f:
        data: dict[str, dict[str, int]] = json.loads(f.read())

    account_data = data.get(account_name, {})
    filter_ts = account_data.get(filter_id, 0)
    return datetime.datetime.fromtimestamp(filter_ts)

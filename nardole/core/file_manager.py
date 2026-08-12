"""File Manager."""

import json
import logging
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from prompt_toolkit.validation import ValidationError

from nardole.const import FILE_MANAGER_DATA_PATH, SAVE_FILE_PATH
from nardole.exceptions import FileManagerError
from nardole.models.indexing import IndexFileModel
from nardole.models.nardole.registry import FileManagerFileRecord

if TYPE_CHECKING:
    from nardole.core.nardole import Nardole

logger = logging.getLogger(__name__)


class FileManager:
    """Class to manage file uploads."""

    def __init__(
        self,
        nardole: "Nardole",
        file_directory: Path = SAVE_FILE_PATH,
        data_path: Path = FILE_MANAGER_DATA_PATH,
    ) -> None:
        """Initialize class."""
        self.nardole = nardole
        self.file_directory = file_directory
        self.data_path = data_path
        self.file_records = load_file_manager_data_file(data_path)

        self._files = {record.file_uid: record for record in self.file_records}

    def store_file(
        self,
        domain: str,
        file_name: str,
        content_type: str,
        bytes_or_text: str | bytes,
    ) -> IndexFileModel:
        """Save down the file provided and return the file model."""
        # Use different UID than file ID so the UID can't be traced back to a single file.
        uid = uuid.uuid4().hex
        file_id = uuid.uuid4().hex

        ext = file_name.rsplit(".", maxsplit=1)[-1] if "." in file_name else ""
        ext = f".{ext}" if ext else ""

        new_file_name = f"{file_id}{ext}"
        new_file_path = self.file_directory.joinpath(new_file_name)

        file_record = FileManagerFileRecord(file_uid=uid, file_path=new_file_path, domain=domain)

        open_mode = "w" if isinstance(bytes_or_text, str) else "wb"
        with open(new_file_path, mode=open_mode) as f:
            f.write(bytes_or_text)

        self.insert_file_record(file_record)
        return IndexFileModel(
            file_name=file_name,
            content_type=content_type,
            uid=uid,
            domain=domain,
        )

    def get_file_path(self, domain: str, file_uid: str) -> Path:
        """Return the path for a single file."""
        record = self._files.get(file_uid)
        if not record:
            msg = f"No record found for file UID {file_uid}"
            raise FileManagerError(msg)
        if record.domain != domain:
            msg = f"Cannot get file UID {file_uid}: Domain {domain} doesn't match file domain {record.domain}!"
            raise FileManagerError(msg)
        return record.file_path

    def insert_file_record(self, record: FileManagerFileRecord) -> None:
        """Add a file record."""
        self._files[record.file_uid] = record
        self.file_records.append(record)
        self._save_updated_records()

    def remove_file(self, file_uid: str) -> None:
        """Remove a file."""
        file_record = self._files.get(file_uid)
        if not file_record:
            msg = f"Can't remove file ID {file_uid}: No record of file found!"
            raise FileManagerError(msg)
        file_record.file_path.unlink(missing_ok=True)
        self.remove_file_record(file_uid=file_uid)

    def remove_file_record(self, file_uid: str) -> None:
        """Remove a file record."""
        new_records = [record for record in self.file_records if record.file_uid != file_uid]
        if len(new_records) - len(self.file_records) > 1:
            msg = f"Multiple files found for ID {file_uid}!"
            raise FileManagerError(msg)
        self.file_records = new_records
        self._files.pop(file_uid)
        self._save_updated_records()

    def _save_updated_records(self) -> None:
        """Save the records to disk."""
        with open(self.data_path, "w") as f:
            f.write(json.dumps(self.file_records))


def load_file_manager_data_file(data_path: Path) -> list[FileManagerFileRecord]:
    """Load the file manager data file."""
    if not data_path.exists():
        _create_file_manager_data_file(data_path=data_path)
        return []
    with open(data_path) as f:
        raw_data = f.read()
    try:
        js = json.loads(raw_data)
        assert isinstance(js, list)
        return [FileManagerFileRecord.model_validate(row) for row in js]
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            msg = "Failed to parse JSON from file manager data file."
        elif isinstance(e, AssertionError):
            msg = f"failed to parse data in file manager data file. Expected a list of file record, got {type(js)}"
        elif isinstance(e, ValidationError):
            msg = "Failed to parse the records in the file manager data file as file records."
        else:
            msg = f"Unknown error parsing file manager data file: {e}"
        msg += f"\nExisting file will be backed up as {data_path.as_posix()}.bak and replaced with a blank file."
        logger.exception(msg)
        backup_path = f"{data_path.as_posix()}.bak"
        data_path.rename(backup_path)
        _create_file_manager_data_file(data_path=data_path, overwrite=True)
    return []


def _create_file_manager_data_file(data_path: Path, overwrite: bool = False) -> None:
    """Create the file manager data file."""
    data_path.touch(mode=600, exist_ok=overwrite)
    with open(data_path, "w") as f:
        f.write("[]")

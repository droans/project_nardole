"""SMS Backup & Restore Integration."""

from typing import TYPE_CHECKING

from nardole.integrations.sms_backup_restore.integration_models import SMSBackupAndRestoreConfigModel
from nardole.integrations.sms_backup_restore.main import SMSBackupAndRestoreIntegration
from nardole.models.nardole.registry import ConfigEntry

CONFIG_SCHEMA = SMSBackupAndRestoreConfigModel


if TYPE_CHECKING:
    from nardole.core.nardole import Nardole


def setup_from_config_entry(
    nardole: "Nardole",
    config_entry: ConfigEntry,
) -> SMSBackupAndRestoreIntegration:
    """Setup integration."""
    integration = SMSBackupAndRestoreIntegration(
        nardole=nardole,
        config_entry=config_entry,
    )
    integration.indexer.setup_indices()
    integration.indexer.setup_embedder()
    integration.register_services()
    return integration

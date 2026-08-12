"""SMS Backup & Restore Integration."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import ValidationError

from nardole.exceptions import ConfigEntryLoadError
from nardole.integrations.sms_backup_restore.const import DOMAIN, IMPORT_SMS_MESSAGES_SERVICE
from nardole.integrations.sms_backup_restore.indexer import SMSBackupAndRestoreIndexer
from nardole.models.indexing import IndexFileModel
from nardole.models.nardole.registry import ServiceEntry

from .integration_models import (
    ImportSMSMessagesServiceSchema,
    MessageModel,
    SMSBackupAndRestoreConfigModel,
    UnsavedAttachment,
)
from .parse_xml import get_conversations, parse_sms_xml_data, process_message_xml_model

if TYPE_CHECKING:
    from nardole.core.contacts import ContactsManager
    from nardole.core.nardole import Nardole
    from nardole.models.nardole.registry import ConfigEntry

logger = logging.getLogger(__name__)


class SMSBackupAndRestoreIntegration:
    """Class for SMS B&R integration."""

    def __init__(
        self,
        nardole: "Nardole",
        config_entry: "ConfigEntry",
        contacts_manager: "ContactsManager",
    ) -> None:
        """Initialize class."""
        logger.debug("Initializing SMS Backup & Restore integration.")
        self.nardole = nardole
        self.config_entry = config_entry
        self.contacts_manager = contacts_manager
        try:
            self.config = SMSBackupAndRestoreConfigModel.model_validate(self.config_entry.user_config)
        except ValidationError as e:
            msg = "Received validation error attempting to load config for SMS Backup & Restore"
            raise ConfigEntryLoadError(msg) from e
        except Exception as e:
            msg = "Config load failed for Google Contacts"
            raise ConfigEntryLoadError(msg) from e
        self.indexer = SMSBackupAndRestoreIndexer(config=self.config, nardole=nardole)
        logger.debug("Initialized SMS Backup & Restore integration.")

    def register_services(self) -> None:
        """Register SMS B&R services."""
        import_messags_service_schema = ServiceEntry(
            service_domain=DOMAIN,
            service_name=IMPORT_SMS_MESSAGES_SERVICE,
            function=self.process_sms_xml,
            service_schema=ImportSMSMessagesServiceSchema,
            response="never",
        )
        self.nardole.service_registry.register_service(service_entry=import_messags_service_schema)

    def process_sms_xml(
        self,
        xml_path: str | Path,
    ) -> None:
        """Process an SMS Backup & Restore XML file."""
        msg = f"Requested to process and import messages from file {xml_path}"
        logger.debug(msg)
        if isinstance(xml_path, str):
            xml_path = Path(xml_path)
        if not xml_path.exists():
            msg = f"Could not find file at path {xml_path.as_posix()}!"
            raise FileNotFoundError(msg)
        logger.debug("Parsing XML file..")
        parsed_xml_models = parse_sms_xml_data(xml_path=xml_path)
        logger.debug("Parsed XML file")
        region_code = self.config.region
        personal_numer = self.config.user_phone_number
        allowed_cts = self.config.save_attachment_types
        allowed_ct_prefixes = self.config.save_attachment_type_prefixes
        messages = []
        logger.debug("Processing XML models...")
        for xml_model in parsed_xml_models:
            unprocessed = process_message_xml_model(
                message_model=xml_model,
                region_code=region_code,
                personal_phone_number=personal_numer,
                allowed_content_types=allowed_cts,
                allowed_content_type_prefixes=allowed_ct_prefixes,
            )
            model = xml_model.model_dump()
            if unprocessed is None:
                continue
            if unprocessed.attachments:
                attachments = self.process_and_save_attachments(unprocessed.attachments)
                model["attachments"] = attachments
            messages.append(MessageModel.model_validate(model))
        logger.debug("Processed XML models.")
        logger.debug("Getting conversations...")
        conversations = get_conversations(messages)
        logger.debug("Conversations retrieved.")
        logger.debug("Importing SMS messages...")
        self.indexer.import_sms_messages(sms_messages=messages)
        logger.debug("Imported SMS messages.")
        logger.debug("Importing conversations...")
        self.indexer.import_sms_conversations(conversations=conversations)
        logger.debug("Imported conversations.")

    def process_and_save_attachments(self, attachments: list[UnsavedAttachment]) -> list[IndexFileModel]:
        """Save the attachments provided and return a list of their index file models."""
        return [
            self.nardole.file_manager.store_file(
                domain=self.config.domain,
                file_name=attachment.file_name,
                content_type=attachment.content_type,
                bytes_or_text=attachment.encoded_data,
            )
            for attachment in attachments
        ]

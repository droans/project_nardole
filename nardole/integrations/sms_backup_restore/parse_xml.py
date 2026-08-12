"""Parse SMS Backup & Restore XML files."""

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import defusedxml.ElementTree
import phonenumbers

from .const import (
    DEFAULT_PROCESS_CONTENT_TYPE_PREFIXES,
    DEFAULT_PROCESS_CONTENT_TYPES,
    AddressType,
    MessageStatus,
)
from .integration_models import (
    ConversationModel,
    MessageModel,
    UnprocessedMessageModel,
    UnsavedAttachment,
)
from .xml_models import (
    XMLAddrModel,
    XMLAnyModel,
    XMLMMSModel,
    XMLPartModel,
    XMLRCSMMSModelStaging,
    XMLRCSModel,
    XMLSMSModel,
)

if TYPE_CHECKING:
    import xml.etree.ElementTree as ET


def parse_sms_xml_data(xml_path: Path) -> list[XMLAnyModel]:
    """Parse the data from an SMS Backup & Restore XML file into a list of XML models."""
    result = []

    context = defusedxml.ElementTree.iterparse(xml_path, events=("end",))

    for _event, elem in context:
        elem = cast("ET.Element", elem)
        tag = elem.tag
        if tag == "sms":
            data = dict(elem.items())
            result.append(XMLSMSModel.model_validate(data))
            continue
        data: dict[str, Any] = dict(elem.items())
        data["parts"] = get_xml_elem_parts(elem)
        data["addrs"] = get_xml_elem_addrs(elem)
        staged = XMLRCSMMSModelStaging.model_validate(data)
        result.append(staged.data)
    return result


def get_xml_elem_parts(elem: "ET.Element") -> list[XMLPartModel]:
    """Collect and return the parts elems from an element."""
    parts_elem = elem.find("parts")
    if not parts_elem:
        return []
    parts = parts_elem.findall("part")
    return [XMLPartModel.model_validate(dict(part.items())) for part in parts]


def get_xml_elem_addrs(elem: "ET.Element") -> list[XMLAddrModel]:
    """Collect and return the addr elems from an element."""
    addrs_elem = elem.find("addrs")
    if not addrs_elem:
        return []
    addrs = addrs_elem.findall("addr")
    return [XMLAddrModel.model_validate(dict(addr.items())) for addr in addrs]


def parse_addrs(
    region_code: str,
    addrs: list[XMLAddrModel],
) -> tuple[phonenumbers.PhoneNumber | None, list[phonenumbers.PhoneNumber]]:
    """Parse a list of XMLAddrModels into a tuple of the sender and participants."""
    sender = None
    recipients = []

    for addr in addrs:
        address = phonenumbers.parse(addr.address, region=region_code)
        if addr.type == AddressType.From:
            sender = address
        recipients.append(address)
    return (sender, recipients)


def parse_parts(
    parts: list[XMLPartModel],
    allowed_content_types: list[str],
    allowed_content_type_prefixes: list[str],
) -> list[str | UnsavedAttachment]:
    """Parse the parts of XMLPartModels into a list of either the message or attachments."""
    attachments = []
    for part in parts:
        if part.text:
            attachments.append(part.text)
        if not part.data:
            continue
        raw_data = part.data.encode()
        content_type = part.ct
        if content_type not in allowed_content_types and not content_type.startswith(
            tuple(allowed_content_type_prefixes),
        ):
            continue
        file_name = part.name or part.cl
        if not file_name or not content_type:
            continue
        attachments.append(UnsavedAttachment(file_name=file_name, content_type=content_type, encoded_data=raw_data))
    return attachments


def _determine_conversation_id(participants: list[phonenumbers.PhoneNumber]) -> str:
    """Create a conversation ID from the participants."""
    participant_numbers = [f"{participant.national_number}" for participant in participants]
    participant_numbers.sort()
    joined_numbers = "_".join(participant_numbers)
    return hashlib.sha224(joined_numbers.encode()).hexdigest()


def _determine_message_id(message: XMLAnyModel) -> str:
    """Create a message ID.

    To ensure the hash remains consistent, the function dumps the contents of the model,
    sorts the items by key, converts the value to a string, and then hashes the string.
    """
    dump = message.model_dump()
    assert isinstance(dump, dict)
    sorted_dump = sorted(dump.items())
    sorted_dump_string = f"{sorted_dump}"
    return hashlib.sha224(sorted_dump_string.encode()).hexdigest()


def process_rcs_mms_message(
    message: XMLRCSModel | XMLMMSModel,
    allowed_content_types: list[str],
    allowed_content_type_prefixes: list[str],
    region_code: str,
) -> UnprocessedMessageModel | None:
    """Parse a MMS/RCS message from the XML model."""
    parts = parse_parts(
        parts=message.parts,
        allowed_content_types=allowed_content_types,
        allowed_content_type_prefixes=allowed_content_type_prefixes,
    )
    sender, participants = parse_addrs(
        region_code=region_code,
        addrs=message.addrs,
    )
    if not sender or not participants:
        return None
    conv_id = _determine_conversation_id(participants=participants)
    timestamp = message.date
    message_contents = [part for part in parts if isinstance(part, str)]
    message_content = message_contents[0] if message_contents else ""
    readable_date = message.readable_date
    direction = "received" if message.msg_box == MessageStatus.Received else "sent"
    message_id = _determine_message_id(message=message)
    attachments = [part for part in parts if not isinstance(part, str)]

    model_type = "rcs" if isinstance(message, XMLRCSModel) else "mms"

    return UnprocessedMessageModel(
        sender=sender,
        conversation_id=conv_id,
        timestamp=timestamp,
        message=message_content,
        readable_date=readable_date,
        direction=direction,
        message_id=message_id,
        attachments=attachments,
        type=model_type,
        participants=participants,
    )


def process_sms_message(
    message: XMLSMSModel,
    region_code: str,
    personal_phone_number: phonenumbers.PhoneNumber,
) -> UnprocessedMessageModel:
    """Process a single SMS message from the XML model."""
    message_status = message.type
    other_party = phonenumbers.parse(message.address, region=region_code)
    participants = [personal_phone_number, other_party]
    conv_id = _determine_conversation_id(participants)
    if message_status == MessageStatus.Received:
        sender = other_party
        direction = "received"
    else:
        sender = personal_phone_number
        direction = "sent"
    message_id = _determine_message_id(message)
    timestamp = message.date
    message_content = message.body
    readable_date = message.readable_date
    return UnprocessedMessageModel(
        type="sms",
        sender=sender,
        conversation_id=conv_id,
        timestamp=timestamp,
        message=message_content,
        readable_date=readable_date,
        direction=direction,
        message_id=message_id,
        participants=participants,
    )


def process_message_xml_model(
    message_model: XMLAnyModel,
    region_code: str,
    personal_phone_number: str,
    allowed_content_types: list[str] = DEFAULT_PROCESS_CONTENT_TYPES,
    allowed_content_type_prefixes: list[str] = DEFAULT_PROCESS_CONTENT_TYPE_PREFIXES,
) -> UnprocessedMessageModel | None:
    """Process messages from their XML models."""
    phone_number = phonenumbers.parse(personal_phone_number, region=region_code)
    if isinstance(message_model, XMLSMSModel):
        return process_sms_message(message=message_model, region_code=region_code, personal_phone_number=phone_number)
    return process_rcs_mms_message(
        message=message_model,
        allowed_content_types=allowed_content_types,
        allowed_content_type_prefixes=allowed_content_type_prefixes,
        region_code=region_code,
    )


def get_conversations(models: list[MessageModel]) -> list[ConversationModel]:
    """Generate a list of conversations from a list of messages."""
    conversation_ids = set()
    conversations = []
    for model in models:
        conv_id = model.conversation_id
        if conv_id not in conversation_ids:
            conversation_ids.add(conv_id)
            conversations.append(ConversationModel(conversation_id=conv_id, participants=model.participants))
    return conversations

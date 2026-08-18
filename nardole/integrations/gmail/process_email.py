"""Process individual emails."""

import base64
import html
import quopri
from email import policy
from email.message import EmailMessage
from email.parser import Parser
from email.utils import getaddresses
from typing import cast

from nardole.core.indices.email.utils import sanitize_email_html
from nardole.integrations.gmail.const import DOMAIN
from nardole.integrations.gmail.models import GmailMessage, GmailRawMessage
from nardole.models.indices.email import EmailAttachmentConfig, EmailModel


def process_attachments(eml: EmailMessage) -> list[EmailAttachmentConfig]:
    """Process attachments for an email."""
    attachments = []
    for attachment in eml.iter_attachments():
        filename = attachment.get_filename()
        if not filename:
            continue
        ct = attachment.get_content_type()
        attachment_id: str | None = attachment.get("content-id")
        if not isinstance(attachment_id, str):
            continue
        attachment_id = attachment_id.removeprefix("<").removesuffix(">")
        attachments.append(
            EmailAttachmentConfig(
                filename=filename,
                content_type=ct,
                attachment_id=attachment_id,
                content_id=attachment_id,
            ),
        )
    return attachments


def parse_addresses(addrs: str) -> list[str]:
    """Parse the addresses from the passed address header."""
    parsed = getaddresses([addrs])
    return [addr[1] for addr in parsed]


"""
        filename: str
        content_type: str
    attachment_id: str
    size: int = 0
    content_id: str | None = None


        timestamp: int
        email_id: str
        conversation_id: str
        labels: list[str] = []
        sender: str
        to: list[str]
        cc: list[str]
        bcc: list[str]
        subject: str
        summaries: list[str]
    attachments: list[EmailAttachmentConfig]
    account: str
    domain: str
"""


def process_gmail_email_raw(email_msg: GmailRawMessage, account_name: str) -> EmailModel:
    """Create an EmailModel from email metadata."""
    raw_email = base64.urlsafe_b64decode(email_msg.raw).decode()
    eml = Parser(policy=policy.default).parsestr(raw_email)

    raw_sender = eml.get("from")
    sender = parse_addresses(raw_sender)[0] if isinstance(raw_sender, str) else "N/A"

    raw_to = eml.get("to")
    _to = parse_addresses(raw_to) if isinstance(raw_to, str) else "N/A"

    raw_cc = eml.get("cc")
    _cc = parse_addresses(raw_cc) if isinstance(raw_cc, str) else "N/A"

    raw_bcc = eml.get("bcc")
    _bcc = parse_addresses(raw_bcc) if isinstance(raw_bcc, str) else "N/A"

    subject = eml.get("subject", "N/A")
    timestamp = int(email_msg.internalDate)
    email_id = email_msg.id
    conversation_id = email_msg.threadId
    labels = email_msg.labelIds

    summaries = []
    summaries.append(email_msg.snippet)
    html_body = eml.get_body(["html"])
    if html_body:
        body = cast("str", html_body.get_content())
        body = html.unescape(body)
        body = quopri.decodestring(body).decode()
        summaries.append(sanitize_email_html(html=body, return_type="text_only"))
    text_body = eml.get_body(["plain"])
    if text_body:
        summaries.append(cast("str", text_body.get_content()))
    attachments = process_attachments(eml)
    return EmailModel(
        timestamp=timestamp,
        email_id=email_id,
        conversation_id=conversation_id,
        labels=labels,
        sender=sender,
        to=_to,
        cc=_cc,
        bcc=_bcc,
        subject=subject,
        summaries=summaries,
        attachments=attachments,
        account=account_name,
        domain=DOMAIN,
    )


def process_gmail_email_full(email: GmailMessage) -> EmailModel:
    """Create an EmailModel from a full email."""
    raise NotImplementedError


def process_gmail_email(email: GmailRawMessage | GmailMessage, account_name: str) -> EmailModel:
    """Process a single email from GMail."""
    if isinstance(email, GmailRawMessage):
        return process_gmail_email_raw(email, account_name=account_name)
    return process_gmail_email_full(email)

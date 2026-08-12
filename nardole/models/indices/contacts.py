"""Model for the contacts indices."""

import datetime

from pydantic import BaseModel

from nardole.models.indexing import E164NumberType


class ContactModel(BaseModel):
    """Model for the contacts index."""

    contact_id: str
    email_address_keys: list[str]
    name_keys: list[str]
    nickname_keys: list[str]
    phone_number_keys: list[str]
    photo_keys: list[str]
    url_keys: list[str]


class BaseContactFieldIndexModel(BaseModel):
    """Base model for a contact field."""

    contact_id: str
    unique_id: str


class ContactEmailAddressModel(BaseContactFieldIndexModel):
    """Model for the email address field for a contact."""

    email_address: str
    type: str | None = None
    notes: list[str] | None = None


class ContactNameModel(BaseContactFieldIndexModel):
    """Model for the name field for a contact."""

    display_name: str
    family_name: str | None = None
    given_name: str | None = None
    last_first_name: str | None = None
    unstructured_name: str | None = None


class ContactNicknameModel(BaseContactFieldIndexModel):
    """Model for the Nickname field for a contact."""

    nickname: str
    notes: list[str] | None = None


class ContactPhoneNumberModel(BaseContactFieldIndexModel):
    """Model for the phone number field for a contact."""

    display_number: str | None = None
    canonical_number: E164NumberType
    notes: list[str] | None = None
    type: str


class ContactPhotoModel(BaseContactFieldIndexModel):
    """Model for the photo field for a contact."""

    photo_url: str
    photo_description: str | None = None
    photo_date: datetime.datetime | None = None
    notes: list[str] | None = None


class ContactURLModel(BaseContactFieldIndexModel):
    """Model for the URL field for a contact."""

    url: str
    type: str
    notes: list[str] | None = None

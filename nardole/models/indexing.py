"""Models related to indexing."""

from typing import Annotated

import phonenumbers
from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumberValidator

from .config import EmbedderConfig


class EmbedderSettings(EmbedderConfig):
    """Model for setup embedder config."""

    document_template: str


class IndexFileModel(BaseModel):
    """Model representing a single index file."""

    domain: str
    file_name: str
    content_type: str
    uid: str


E164NumberType = Annotated[str | phonenumbers.PhoneNumber, PhoneNumberValidator(number_format="E164")]

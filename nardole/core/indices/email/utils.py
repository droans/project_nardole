"""Email indexer utility functions."""

from typing import Literal

import bs4
from bs4 import Comment

from nardole.const.email import EmailIndexFields
from nardole.core.meilisearch.util import generate_base_search_config_from_model, generate_single_filter_string
from nardole.models.indices.email import EmailFilterOptions, EmailSearchRequest, EmailSortOptions

StripEmailReturnTypes = Literal[
    "text_only",
    "all_html",
    "html_text_only",
]


def sanitize_email_html(
    html: str,
    return_type: StripEmailReturnTypes = "html_text_only",
    strip_imgs: bool = True,
    strip_styles: bool = True,
    strip_attributes: bool = True,
    strip_a_href: bool = True,
    strip_comments: bool = True,
) -> str:
    """Sanitize the HTML from an email body. Always removes scripts.

    Params:
        return_type:
            text_only: Returns only the text in the HTML.
            html_text_only: Returns the entire HTML structure for any text-containing element
                Note: If any of the `strip_` parameters are set to False, will return those elements, too.
            all_html: Returns the entire HTML structure
        strip_imgs: Remove all `img` elements.
        strip_styles: Remove all `style` elements
        strip_a_href: Remove all `a href` elements
        strip_attributes: Remove the attributes from all (except img) elements
            Note: `img`, `a`, and `style` elements will retain their attributes if they are not stripped

    Returns: String
    """
    soup = bs4.BeautifulSoup(html)

    # Scripts are always removed
    remove_elems = ["script"]
    if strip_imgs:
        remove_elems.append("img")
    if strip_styles:
        remove_elems.append("style")
    if strip_a_href:
        remove_elems.append("a")

    for script in soup(remove_elems):
        script.decompose()

    # If text only, no need to continue.
    if return_type == "text_only":
        return "\n".join([line for line in soup.text.split("\n") if line.strip()])

    for tag in soup.find_all():
        tag_name = tag.name

        # Don't strip attributes for img, style, a elements.
        if tag_name in ["img", "style", "a"]:
            continue

        # If element has children, strip attributes and continue.
        if tag.find_all():
            if strip_attributes:
                tag.attrs = {}
            continue

        if return_type in ("html_text_only") and not tag.text.strip():
            tag.decompose()
            continue
        if strip_attributes:
            tag.attrs = {}
    if strip_comments:
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()

    return "\n".join([line for line in str(soup).split("\n") if line.strip()])


def generate_email_filter_string_from_model(model: EmailFilterOptions) -> str:
    """Generates the email filter string from the provided model."""
    filter_ls: list[str] = []
    if model.account:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.ACCOUNT, model.account))
    if model.conversation_id:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.CONVERSATION_ID, model.conversation_id))
    if model.domain:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.DOMAIN, model.domain))
    if model.sender:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.SENDER, model.sender))
    if model.to:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.TO, model.to))
    if model.cc:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.CC, model.cc))
    if model.bcc:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.BCC, model.bcc))
    if model.attachments_mime_type:
        filter_ls.append(
            generate_single_filter_string(EmailIndexFields.ATTACHMENTS_MIME_TYPE, model.attachments_mime_type),
        )
    if model.labels:
        filter_ls.append(generate_single_filter_string(EmailIndexFields.LABELS, model.labels))
    return " AND ".join(filter_ls)


def generate_email_sort_list_from_model(model: EmailSortOptions) -> list[str]:
    """Generates the email sort string from the provided model."""
    result = []

    if model.timestamp:
        result.append(f"{EmailIndexFields.TIMESTAMP}:{model.timestamp}")
    return result


"""
        sort: EmailSortOptions | None = None
        filter: EmailFilterOptions | None = None
        offset: int = 0
        limit: int = 20
        page: int | None = None
        hits_per_page: int | None = None
    semantic_ratio: float = Field(default=0.5, le=1, ge=0)
    attributes_to_retrieve: list[str] | None = None
    kwargs: dict = {}
"""


def generate_email_search_dict_from_model(model: EmailSearchRequest) -> dict:
    """Generate the search options dictionary from the search request model."""
    result = generate_base_search_config_from_model(model)
    if model.filter:
        result["filter"] = generate_email_filter_string_from_model(model.filter)
    if model.sort:
        result["sort"] = generate_email_sort_list_from_model(model.sort)
    return result

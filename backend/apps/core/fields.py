"""Model fields shared across apps."""

import nh3
from django.db import models

# What the editor (Trix) can produce, and nothing else. Links are forced to
# rel="noopener noreferrer" so pasted content cannot reach window.opener.
ALLOWED_TAGS = {
    "p", "br", "strong", "b", "em", "i", "u", "s", "a", "ul", "ol", "li",
    "h2", "h3", "h4", "blockquote", "pre", "code", "figure", "figcaption", "hr", "div",
}
ALLOWED_ATTRIBUTES = {"a": {"href", "title"}}


def sanitize_html(value: str) -> str:
    if not value:
        return ""
    return nh3.clean(
        value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes={"http", "https", "mailto", "tel"},
        link_rel="noopener noreferrer",
    )


class RichTextField(models.TextField):
    """HTML from the admin editor, sanitised every time it is saved."""

    def pre_save(self, model_instance, add):
        value = sanitize_html(getattr(model_instance, self.attname))
        setattr(model_instance, self.attname, value)
        return value

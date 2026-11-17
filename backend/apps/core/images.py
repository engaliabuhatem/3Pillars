"""
Everything about public images, in one place.

* Validation: allowed types, an 8 MB ceiling and minimum dimensions, applied to
  new uploads only, so an old file never blocks an unrelated edit.
* Renditions: every saved image gets a WebP and an AVIF sibling next to it
  (`photo.jpg` -> `photo.jpg.webp`, `photo.jpg.avif`). The names are derived,
  so no extra columns are needed and a rendition can always be rebuilt.
* Payload: `image_payload()` builds the object the API returns.

Only `file.url` and the storage API are used, never a disk path, so the
storage backend can change without touching models or serializers.
"""

import logging
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible
from PIL import Image, ImageOps

#: SVG is excluded from photo fields because it can carry script. Logos accept
#: it separately through LOGO_VALIDATORS, which sniffs for script.
log = logging.getLogger(__name__)

PHOTO_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "avif"]
MAX_IMAGE_MB = 8
MAX_IMAGE_BYTES = MAX_IMAGE_MB * 1024 * 1024
RENDITION_MAX_EDGE = 2560
RENDITION_FORMATS = {"webp": {"quality": 82}, "avif": {"quality": 60}}

PHOTO_HELP = (
    f"JPG, PNG, WebP or AVIF, up to {MAX_IMAGE_MB} MB. WebP and AVIF copies are "
    "made automatically for fast loading."
)


def is_new_upload(file) -> bool:
    return not getattr(file, "_committed", False)


@deconstructible
class NewUploadExtensionValidator(FileExtensionValidator):
    def __call__(self, value):
        if is_new_upload(value):
            super().__call__(value)


@deconstructible
class MaxFileSizeValidator:
    def __init__(self, max_bytes: int):
        self.max_bytes = max_bytes

    def __call__(self, file):
        if is_new_upload(file) and file.size > self.max_bytes:
            raise ValidationError(
                "This file is %(size).1f MB. The largest you can upload here is "
                "%(limit)d MB, so please compress it and try again.",
                code="file_too_large",
                params={"size": file.size / 1048576, "limit": self.max_bytes // 1048576},
            )

    def __eq__(self, other):
        return isinstance(other, MaxFileSizeValidator) and self.max_bytes == other.max_bytes


@deconstructible
class MinDimensionsValidator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __call__(self, file):
        if not is_new_upload(file):
            return
        try:
            file.seek(0)
            with Image.open(file) as img:
                width, height = img.size
            file.seek(0)
        except Exception as exc:
            raise ValidationError("This file could not be read as an image.") from exc
        if width < self.width or height < self.height:
            raise ValidationError(
                "This image is %(w)d×%(h)d pixels. Please use one at least "
                "%(min_w)d×%(min_h)d so it stays sharp on large screens.",
                code="image_too_small",
                params={"w": width, "h": height, "min_w": self.width, "min_h": self.height},
            )

    def __eq__(self, other):
        return (
            isinstance(other, MinDimensionsValidator)
            and (self.width, self.height) == (other.width, other.height)
        )


@deconstructible
class SafeSvgValidator:
    """Rejects SVGs carrying script, event handlers or external references."""

    BANNED = (b"<script", b"javascript:", b"onload", b"onerror", b"onclick",
              b"<foreignobject", b"xlink:href=\"http", b"href=\"http", b"<iframe")

    def __call__(self, file):
        if not is_new_upload(file) or not file.name.lower().endswith(".svg"):
            return
        file.seek(0)
        body = file.read().lower()
        file.seek(0)
        if any(token in body for token in self.BANNED):
            raise ValidationError(
                "This SVG contains scripts or external links and cannot be used. "
                "Export a plain SVG or upload a PNG instead."
            )

    def __eq__(self, other):
        return isinstance(other, SafeSvgValidator)


def _extension_validator(extensions):
    return NewUploadExtensionValidator(
        allowed_extensions=extensions,
        message="“%(extension)s” files can’t be uploaded here. Allowed: %(allowed_extensions)s.",
    )


def photo_validators(min_width: int = 1200, min_height: int = 600) -> list:
    return [
        _extension_validator(PHOTO_EXTENSIONS),
        MaxFileSizeValidator(MAX_IMAGE_BYTES),
        MinDimensionsValidator(min_width, min_height),
    ]


LOGO_VALIDATORS = [
    _extension_validator(["svg", "png", "webp"]),
    MaxFileSizeValidator(2 * 1024 * 1024),
    SafeSvgValidator(),
]


# ── Renditions ───────────────────────────────────────────────────────────


def rendition_name(name: str, fmt: str) -> str:
    return f"{name}.{fmt}"


def build_renditions(fieldfile) -> None:
    """Write WebP + AVIF siblings for a stored raster image. Idempotent."""
    if not fieldfile or fieldfile.name.lower().endswith(".svg"):
        return
    storage = fieldfile.storage
    missing = [f for f in RENDITION_FORMATS if not storage.exists(rendition_name(fieldfile.name, f))]
    if not missing or not storage.exists(fieldfile.name):
        return
    try:
        _write_renditions(fieldfile, missing)
    except Exception as exc:  # The original still serves; a rendition is an optimisation.
        log.warning("could not build renditions for %s: %s", fieldfile.name, exc)


def _write_renditions(fieldfile, missing: list[str]) -> None:
    storage = fieldfile.storage
    with storage.open(fieldfile.name, "rb") as handle, Image.open(handle) as img:
        img = ImageOps.exif_transpose(img)
        img.thumbnail((RENDITION_MAX_EDGE, RENDITION_MAX_EDGE))
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
        for fmt in missing:
            buffer = BytesIO()
            img.save(buffer, format=fmt.upper(), **RENDITION_FORMATS[fmt])
            storage.save(rendition_name(fieldfile.name, fmt), ContentFile(buffer.getvalue()))


def delete_with_renditions(name: str, storage=default_storage) -> None:
    for path in (name, *(rendition_name(name, f) for f in RENDITION_FORMATS)):
        if path and storage.exists(path):
            storage.delete(path)


def image_dimensions(fieldfile) -> tuple[int | None, int | None]:
    try:
        return fieldfile.width, fieldfile.height
    except Exception:
        return None, None


# ── API payload ──────────────────────────────────────────────────────────


def _absolute(url: str, request) -> str:
    return request.build_absolute_uri(url) if request else url


def image_payload(instance, field: str = "image", *, request=None, locale: str = "en"):
    """
    `{src, alt, width, height, sources}` for the image in `field`, or None.

    `alt` follows the locale with English as the fallback, so a missing Arabic
    alt text never ships an empty one.
    """
    fieldfile = getattr(instance, field, None)
    if not fieldfile:
        return None
    alt_en = getattr(instance, f"{field}_alt", "") or ""
    alt_ar = getattr(instance, f"{field}_alt_ar", "") or ""
    width, height = image_dimensions(fieldfile)
    storage = fieldfile.storage
    sources = {
        fmt: _absolute(storage.url(rendition_name(fieldfile.name, fmt)), request)
        for fmt in RENDITION_FORMATS
        if storage.exists(rendition_name(fieldfile.name, fmt))
    }
    return {
        "src": _absolute(fieldfile.url, request),
        "alt": (alt_ar or alt_en) if locale == "ar" else alt_en,
        "width": width,
        "height": height,
        "sources": sources,
    }


def file_payload(instance, field: str, *, request=None):
    fieldfile = getattr(instance, field, None)
    if not fieldfile:
        return None
    return {"src": _absolute(fieldfile.url, request), "size": fieldfile.size}

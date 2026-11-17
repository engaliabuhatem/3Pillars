"""
Private uploads: CVs and proposal attachments.

They are stored under PRIVATE_MEDIA_ROOT with random names and have no public
URL; staff fetch them through an authenticated admin view. The declared file
type is never trusted — the first bytes are sniffed against the formats each
field accepts.
"""

import secrets
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.utils.deconstruct import deconstructible
from django.utils.functional import LazyObject

from .images import MaxFileSizeValidator, is_new_upload

#: Magic numbers. DOCX/XLSX/PPTX are zip containers; the extension narrows it.
SIGNATURES = {
    "pdf": [b"%PDF-"],
    "docx": [b"PK\x03\x04"],
    "xlsx": [b"PK\x03\x04"],
    "png": [b"\x89PNG\r\n\x1a\n"],
    "jpg": [b"\xff\xd8\xff"],
    "jpeg": [b"\xff\xd8\xff"],
    "zip": [b"PK\x03\x04"],
    "mp4": [],
    "webm": [b"\x1a\x45\xdf\xa3"],
}


class PrivateFileSystemStorage(FileSystemStorage):
    def url(self, name):
        raise ValueError("Private files have no public URL; staff download them through the admin.")


class _PrivateStorage(LazyObject):
    def _setup(self):
        self._wrapped = PrivateFileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)


_private = _PrivateStorage()


def private_storage():
    """Passed as a callable so migrations never bake in a filesystem path."""
    return _private


@deconstructible
class RandomName:
    """upload_to that discards the uploaded filename (it can leak names and PII)."""

    def __init__(self, folder: str):
        self.folder = folder

    def __call__(self, instance, filename):
        ext = Path(filename).suffix.lower()[:10]
        return f"{self.folder}/{secrets.token_hex(16)}{ext}"

    def __eq__(self, other):
        return isinstance(other, RandomName) and other.folder == self.folder


@deconstructible
class SniffedTypeValidator:
    """Checks extension and the file's own signature agree with `allowed`."""

    def __init__(self, allowed: tuple[str, ...]):
        self.allowed = tuple(allowed)

    def __call__(self, file):
        if not is_new_upload(file):
            return
        ext = Path(file.name).suffix.lower().lstrip(".")
        if ext not in self.allowed:
            raise ValidationError(
                "“%(ext)s” files are not accepted. Allowed: %(allowed)s.",
                params={"ext": ext or "?", "allowed": ", ".join(self.allowed).upper()},
            )
        signatures = SIGNATURES.get(ext, [])
        file.seek(0)
        head = file.read(16)
        file.seek(0)
        if ext == "mp4":
            valid = head[4:8] == b"ftyp"
        else:
            valid = not signatures or any(head.startswith(sig) for sig in signatures)
        if not valid:
            raise ValidationError("This file’s contents don’t match its type. Please re-export it and try again.")

    def __eq__(self, other):
        return isinstance(other, SniffedTypeValidator) and self.allowed == other.allowed


def document_validators(allowed=("pdf", "docx"), max_mb: int = 5) -> list:
    return [SniffedTypeValidator(allowed), MaxFileSizeValidator(max_mb * 1024 * 1024)]


def video_validators(max_mb: int, allowed=("mp4",)) -> list:
    return [SniffedTypeValidator(allowed), MaxFileSizeValidator(max_mb * 1024 * 1024)]

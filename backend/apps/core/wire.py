"""
camelCase on the wire, snake_case in Python.

Kept apart from api.py on purpose: DRF imports these classes while building
its own settings, so this module must not import anything that reads them.
"""

import re

from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import DataAndFiles, JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer

_CAMEL = re.compile(r"_([a-z0-9])")
_SNAKE = re.compile(r"(?<!^)(?=[A-Z])")


def camel(key: str) -> str:
    return _CAMEL.sub(lambda m: m.group(1).upper(), key)


def snake(key: str) -> str:
    return _SNAKE.sub("_", key).lower()


def transform_keys(data, fn):
    if isinstance(data, dict):
        return {fn(k) if isinstance(k, str) else k: transform_keys(v, fn) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [transform_keys(v, fn) for v in data]
    return data


class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render(transform_keys(data, camel), accepted_media_type, renderer_context)


class CamelCaseJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        return transform_keys(super().parse(stream, media_type, parser_context), snake)


class CamelCaseMultiPartParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type, parser_context)
        data = QueryDict(mutable=True)
        for key in result.data:
            data.setlist(snake(key), result.data.getlist(key))
        files = MultiValueDict()
        for key in result.files:
            files.setlist(snake(key), result.files.getlist(key))
        return DataAndFiles(data, files)


class Pagination(PageNumberPagination):
    page_size_query_param = "pageSize"
    max_page_size = 100

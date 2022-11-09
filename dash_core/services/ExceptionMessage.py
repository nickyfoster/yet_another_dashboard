from enum import Enum


class ExceptionMessage(Enum):
    DASHCORE_URL_INVALID = 'dashcore.url.invalid'
    DASHCORE_URL_NOT_FOUND = 'dashcore.url.not_found'
    DASHCORE_URL_UNABLE_TO_PARSE_HTML = 'dashcore.url.unable_to_parse_html_table'
    DASHCORE_URL_UNABLE_TO_PARSE_WEEK = 'dashcore.url.unable_to_parse_week_columns'

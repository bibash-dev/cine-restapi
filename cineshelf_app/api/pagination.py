from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)


class MediaStreamPagination(PageNumberPagination):
    page_size = 5
    page_query_param = "record"
    page_size_query_param = "limit"
    max_page_size = 10
    last_page_strings = "end"


class MediaStreamLOPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10
    limit_query_param = "limit"
    offset_query_param = "offset"


class MediaStreamCursorPagination(CursorPagination):
    page_size = 5
    ordering = "created_at"
    cursor_query_param = "record"

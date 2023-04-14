from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class PaginateMixin:
    def paginated_list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        paginator = LimitOffsetPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

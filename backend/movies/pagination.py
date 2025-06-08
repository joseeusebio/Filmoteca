from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

class CustomCursorPagination(CursorPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    ordering = 'id'

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "data": data,
            "meta": {
                "itemsPerPage": len(data),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            }
        })

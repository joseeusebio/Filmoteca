from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "status": "success",
            "data": data,
            "meta": {
                "count": self.page.paginator.count,
                "totalPages": self.page.paginator.num_pages,
                "currentPage": self.page.number,
                "itemsPerPage": self.get_page_size(self.request),
                "hasNext": self.page.has_next(),
                "hasPrevious": self.page.has_previous(),
            }
        })

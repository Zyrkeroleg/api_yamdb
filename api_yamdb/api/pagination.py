from rest_framework import pagination
from rest_framework.response import Response


class CustomReviewPagination(pagination.PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )


class CustomCommentPagination(pagination.PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        print(data)
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )

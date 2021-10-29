from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class AuthorPagination(PageNumberPagination):
    page_size = 10 # default size if no size parameter passed
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'authors': data
        })

class PostPagination(PageNumberPagination):
    page_size = 10 # default size if no size parameter passed
    page_size_query_param = 'size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'posts': data
        })
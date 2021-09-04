from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustomLimitPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100



    """
    
    
    page = self.paginate_queryset(booking_list_qs)
    serializer = self.get_serializer(page, many=True)
    paginated_data = self.get_paginated_response(serializer.data)

    """
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
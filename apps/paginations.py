from rest_framework.pagination import PageNumberPagination as _PageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(_PageNumberPagination):
    page_query_param = 'page'  # 前端传入第几页
    page_size_query_param = 'perPage'  # 前端传入每页显示条数

    page_size = 10  # 每页显示记录数，前端没有传入page_num，则默认显示此参数
    max_page_size = 100  # 后端控制每页显示最大记录数

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page_num': self.page.number,
            'page_size': self.get_page_size(self.request),
            'items': data
        })

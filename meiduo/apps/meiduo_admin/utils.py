from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNum(PageNumberPagination):
    # 1.开启分页、设置默认每页多少条记录
    page_size = 5
    # 2.开启每页多少条记录 可已通过传递的参数传递
    # pagesize=xxx 每页多少条记录的 key
    page_size_query_param = 'pagesize'

    # 最大一页多少条记录
    max_page_size = 3

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'pagesize': self.page.paginator.per_page,
            'lists': data
        })

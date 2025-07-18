from rest_framework.generics import ListCreateAPIView

from apps.users.models import User
from apps.meiduo_admin.serializer.user import UserModelSerializer
from apps.meiduo_admin.utils import PageNum

"""
用户管理

    用户展示    --  获取用户信息,实现分页和搜索功能
        1. 先实现用户查询
            1.1 查询所有用户
            1.2 将对象列表转换为 满足需求的字典列表 (序列化器)
            1.3 返回响应
        2. 再实现搜索功能
        3. 最后实现分页

    新增用户    --  增加一个测试用户

"""


class UserApiView(ListCreateAPIView):
    # queryset = User.objects.all()

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return User.objects.filter(username__contains=keyword)

        return User.objects.all()

    serializer_class = UserModelSerializer

    # 分页
    pagination_class = PageNum

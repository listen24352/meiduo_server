"""
viewsets：用于创建视图集，视图集是一种将视图逻辑组织在一起的方式。
status：包含 HTTP 状态码的常量，方便在响应中使用。
permissions：用于设置视图的访问权限。
mixins：提供了一些通用的视图行为，如创建、读取、更新和删除等。
"""
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action  # 导入 action 装饰器，用于在视图集中定义自定义的动作。
from rest_framework.response import Response  # 导入 Response 类，用于构建 RESTful 响应。
from django.contrib.auth import login  # 导入 login 函数，用于在用户注册成功后自动登录用户。
from drf_spectacular.utils import extend_schema
from apps.users.serializers.register_serializers import RegisterSerializer
from apps.users.models import User


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户管理视图集
    包含：用户名检查、用户注册
    CreateModelMixin：提供了创建对象的功能
    GenericViewSet：是一个通用的视图集基类
    """
    # 指定视图集要处理的查询集，这里表示获取所有的 User 对象。
    queryset = User.objects.all()
    # 指定视图集使用的序列化器
    serializer_class = RegisterSerializer
    # 允许任何用户访问该视图集的接口
    permission_classes = [permissions.AllowAny]
    @extend_schema(responses=RegisterSerializer)
    @action(detail=False, methods=['GET'], url_path='check_username/(?P<username>[^/.]+)', url_name='check-username')
    def check_username(self, request, username=None):
        """
        detail=False：表示该动作不针对单个对象，而是针对整个视图集。
        methods=['GET']：表示该动作只接受 GET 请求。
        url_path  定义该动作的 URL 路径，其中 (?P<username>[^/.]+) 是一个正则表达式，用于捕获用户名参数。
        url_name='check-username'：为该动作的 URL 定义一个名称，方便在代码中引用。

        检查用户名是否存在
        """
        if not username:
            return Response({'code': 400, 'errmsg': '用户名不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        count = User.objects.filter(username=username).count()
        return Response({'code': 0, 'count': count, 'errmsg': 'ok'})

    # 重写 CreateModelMixin 中的 create 方法，用于处理用户注册请求。
    def create(self, request, *args, **kwargs):
        """用户注册"""

        # 使用视图集的序列化器类创建一个序列化器实例，并将请求数据传递给它。
        serializer = self.get_serializer(data=request.data)
        # 验证请求数据的有效性，如果数据无效则抛出异常。
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 注册成功后自动登录
        login(request, user)
        # 获取成功响应的头部信息。
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'code': 0, 'errmsg': '注册成功'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

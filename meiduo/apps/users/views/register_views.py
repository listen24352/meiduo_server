from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.users.serializers.register_serializers import RegisterSerializer
from apps.users.models import User
from django.contrib.auth import login


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    用户管理视图集
    包含：用户名检查、用户注册
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['GET'], url_path='check_username/(?P<username>[^/.]+)', url_name='check-username')
    def check_username(self, request, username=None):
        """检查用户名是否存在"""
        if not username:
            return Response({'code': 400, 'errmsg': '用户名不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        count = User.objects.filter(username=username).count()
        return Response({'code': 0, 'count': count, 'errmsg': 'ok'})

    def create(self, request, *args, **kwargs):
        """用户注册"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 注册成功后自动登录
        login(request, user)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {'code': 0, 'errmsg': '注册成功'},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

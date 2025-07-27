from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.contrib.auth import login

from apps.users.serializers.login_serializers import LoginSerializer
from apps.carts.utils import merge_cookie_to_redis
from django.views.decorators.csrf import csrf_exempt


class LoginView(APIView):
    """用户登录API"""
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    @csrf_exempt
    def post(self, request):
        # 实例化序列化器并验证数据
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'code': 400, 'errmsg': '参数错误', 'errors': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        # 获取验证后的数据
        validated_data = serializer.validated_data
        user = validated_data['user']
        print(user.is_active)
        remembered = validated_data.get('remembered', False)

        # 登录用户
        login(request, user)

        # 设置session过期时间
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        # 准备响应数据
        data = {'code': 0, 'errmsg': 'ok'}
        response = Response(data)

        # 设置cookie
        response.set_cookie('username', user.username)

        # 合并购物车数据
        response = merge_cookie_to_redis(request, response)

        return response

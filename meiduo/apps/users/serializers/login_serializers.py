import re

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# 登录序列化器
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    remembered = serializers.BooleanField(required=False, default=False)

    def validate(self, data):
        # 检查用户名格式
        username = data.get('username')
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 验证用户
        user = authenticate(
            username=username,
            password=data.get('password')
        )

        if not user:
            raise serializers.ValidationError('账号或密码错误')

        # 将用户对象添加到验证数据中
        data['user'] = user
        return data

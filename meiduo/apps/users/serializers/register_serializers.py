# serializers.py
from rest_framework import serializers
from apps.users.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import re


class RegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',)
        extra_kwargs = {
            'password': {'write_only': True},
            # 'mobile': {'required': False, 'allow_blank': True}  # 允许不提供mobile
        }
        # 'email': {'required': True}  # 确保邮箱是必填项

    def validate_username(self, value):
        """验证用户名格式"""
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', value):
            raise serializers.ValidationError(
                "用户名必须由5-20位字母、数字、下划线或连字符组成"
            )
        # 检查用户名是否已存在
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    # def validate_email(self, value):
    #     """验证邮箱格式"""
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("邮箱已被注册")
    #     return value

    # def validate_mobile(self, value):
    #     """处理空手机号"""
    #     if value == '':
    #         return None  # 将空字符串转换为None
    #     return value

    def validate(self, attrs):
        """验证两次输入的密码是否一致"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password2": "两次输入的密码不一致"}
            )

        # 使用Django内置密码验证器
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        """创建用户"""
        # 移除不需要的password2字段
        validated_data.pop('password2')
        # print(validated_data)
        # 使用create_user方法创建用户（自动加密密码）
        user = User.objects.create_user(**validated_data)
        return user

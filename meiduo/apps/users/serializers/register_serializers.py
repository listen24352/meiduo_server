import re

from rest_framework import serializers  # 创建序列化类
# Django 内置的密码验证器，用于验证用户输入的密码是否符合密码策略。
from django.contrib.auth.password_validation import validate_password
# Django 的 ValidationError 异常类，用于在验证失败时抛出异常。
from django.core.exceptions import ValidationError

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    ModelSerializer  快速创建与模型相关的序列化器。

    反序列化（网页 → 数据库）反序列化是把客户端发送的 JSON 数据转化为模型实例，然后保存到数据库中。
    序列化（数据库 → 网页）序列化的过程是将数据库中的模型实例转化为 JSON 等格式，以便在 API 中返回。
    """

    # write_only=True 表示该字段只用于写入操作（如创建或更新），不会在序列化输出中显示；
    # required=True 表示该字段是必需的。
    password2 = serializers.CharField(write_only=True, required=True)

    # 这是一个内部类，用于配置序列化器的元数据
    class Meta:
        model = User  # 指定该序列化器对应的模型为 User 模型
        fields = ('username', 'password', 'password2')  # 指定序列化器包含的字段
        # extra_kwargs 用于为特定字段提供额外的配置选项
        extra_kwargs = {
            'password': {'write_only': True},  # 设置为只写字段
            # 'mobile': {'required': False, 'allow_blank': True}  # 允许不提供mobile
        }
        # 'email': {'required': True}  # 确保邮箱是必填项

    def validate_username(self, value):
        """
        验证用户名格式
        value 参数：value 代表当前正在验证的字段的值
        """
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

    # 全局验证方法，用于验证序列化器中的所有字段。
    def validate(self, attrs):
        """
        验证两次输入的密码是否一致
        attrs 参数：在序列化器的全局验证方法（如 validate）中，attrs 是一个字典，包含了所有经过字段级验证后的字段及其值。
        也就是说，attrs 是一个包含了所有有效字段数据的字典。

        """
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

    # 创建用户
    def create(self, validated_data):
        """
        创建用户
        validated_data 在序列化器的创建方法（如 create）或更新方法（如 update）中，validated_data 是一个字典，包含了经过所有验证（包括字段级验证和全局验证）后的有效数据。
        这些数据可以直接用于创建或更新数据库中的对象。

        """
        # 移除不需要的password2字段
        validated_data.pop('password2')
        # print(validated_data)
        # 使用create_user方法创建用户（自动加密密码）
        user = User.objects.create_user(**validated_data)
        return user

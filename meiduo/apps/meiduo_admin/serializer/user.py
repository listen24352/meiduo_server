from rest_framework import serializers
from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)  # 设置不给前端返回  方法一

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'mobile', 'email', 'password']

        # 设置不给前端返回  方法一
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 15,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class LoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": _("该账号已被禁用,请与管理员联系!")
    }

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]
        user = User.objects.filter(username=username).first()
        if not user:
            result = {
                'code': 400,
                'errmsg': '账户密码不正确',
                'data': None
            }
            return result
        if user and not user.is_staff:
            result = {
                'code': 400,
                'errmsg': '您没有权限登录后台',
                'data': None
            }
            return result
        if user and not user.is_active:
            result = {
                'code': 400,
                'errmsg': '该账户已被禁用，请与管理员联系',
                'data': None
            }
            return result
        if user and user.check_password(password):
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['username'] = self.user.username
            data['userid'] = self.user.id
            requests = self.context.get('request')
            requests.user = self.user
            result = {
                'code': 200,
                'errmsg': '登录成功',
                'username': self.user.username,
                'user_id': str(self.user.id),
                'token': str(refresh.access_token),
                'data': data
            }
        else:
            result = {
                'code': 400,
                'errmsg': '账户或密码不正确',
                'data': None
            }
        return result

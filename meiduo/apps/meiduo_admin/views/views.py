from rest_framework_simplejwt.views import TokenObtainPairView

from apps.meiduo_admin.user import LoginSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

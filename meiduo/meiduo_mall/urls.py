"""
URL configuration for meiduo_mall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 注册路径转化器
from utils.converters import UsernameConverter
from django.urls import register_converter
register_converter(UsernameConverter, 'username')

# djangorestframework-simplejwt  项目配置
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),  # 用户
    path('api/', include('apps.areas.urls')),  # 省市区

    # 验证码
    path('', include('apps.verifications.urls')),
    path('', include('apps.goods.urls')),
    path('', include('apps.carts.urls')),
    path('', include('apps.orders.urls')),  # 订单
    path('', include('apps.pay.urls')),  # 支付
    # path('meiduo_admin/', include('apps.meiduo_admin.urls')),
    # djangorestframework-simplejwt
    # path('meiduo_admin/authorizations/', TokenObtainPairView.as_view()),
    path('api/token/refrensh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),


]

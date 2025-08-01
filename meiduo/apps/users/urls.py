from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views.register_views import UserRegisterViewSet
from apps.users.views.login_views import LoginView
from apps.users.views.logout_views import LogoutView
from apps.users.views.address_views import AddressView,AddressCreateView
from apps.users.views.views import CenterView, EmailView, EmailVerifyView, \
    UserHistoryView

router = DefaultRouter()  # DRF 提供的自动路由生成器，可根据视图集自动生成 URL。
router.register(r'users', UserRegisterViewSet, basename='user_register')  # 将视图集注册到路由中

# router.register('addresses', AddressViewSet, basename='address')

"""
GET /addresses/ → 列表
POST /addresses/ → 创建
GET /addresses/{id}/ → 详情
PUT /addresses/{id}/ → 更新
PATCH /addresses/{id}/ → 部分更新
DELETE /addresses/{id}/ → 删除（逻辑删除）

"""

"""
r'users'：URL 前缀，生成的 URL 会以 /users/ 开头。
UserRegisterViewSet：绑定的视图集，处理该 URL 下的请求。
basename='user'：为路由命名，用于反向解析 URL（如生成链接）。
"""

urlpatterns = [
    # 用户名检查: /api/users/check_username/<username>/
    # 用户注册: /api/users/
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # 用户中心
    path('info/', CenterView.as_view()),
    # 邮件保存
    path('emails/', EmailView.as_view()),
    # 邮件验证
    path('emails/verification/', EmailVerifyView.as_view()),

    # 创建地址
    path('addresses/create/', AddressCreateView.as_view()),

    # 获取地址列表
    path('addresses/', AddressView.as_view()),

    # 新增地址
    # path('addresses/create/', AddressCreateView.as_view()),
    # 查询地址
    # path('addresses/', AddressView.as_view()),
    # path('addresses/<int>', AddressView.as_view()),
    # 浏览记录
    path('browse_histories/', UserHistoryView.as_view()),
]

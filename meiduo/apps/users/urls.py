# from django.urls import path
# # from apps.users.views.register_views import UsernameCountView, RegisterView, LoginView, LogoutView, CenterView, UserHistoryView
# # from apps.users.views import EmailView, EmailVerifyView, AddressCreateView, AddressView
#
# urlpatterns = {
#     path('usernames/<str:username>/count/', UsernameCountView.as_view(), name='username_count'),
#     # 注册
#     path('register/', RegisterView.as_view()),
#     # 登录
#     path('login/', LoginView.as_view()),
#     # 退出
#     path('logout/', LogoutView.as_view()),
#     # 用户中心
#     path('info/', CenterView.as_view()),
#     # 邮件保存
#     path('emails/', EmailView.as_view()),
#     # 邮件验证
#     path('emails/verification/', EmailVerifyView.as_view()),
#     # 新增地址
#     path('addresses/create/', AddressCreateView.as_view()),
#     # 查询地址
#     path('addresses/', AddressView.as_view()),
#     # 浏览记录
#     path('browse_histories/', UserHistoryView.as_view()),
# }


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views.register_views import UserRegisterViewSet
from apps.users.views.login_views import LoginView

router = DefaultRouter()  # DRF 提供的自动路由生成器，可根据视图集自动生成 URL。
router.register(r'users', UserRegisterViewSet, basename='user_register')  # 将视图集注册到路由中
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
]

from django.urls import path, include

from apps.meiduo_admin.views.images import ImagesModelViewSet, ImageSKUAPIView
from apps.meiduo_admin.views.views import LoginView
from apps.meiduo_admin.views.home import DailyActiveAPIView, DailyOrderCountAPIView, MonthCountAPIView, \
    TotalCountAPIView, DayIncrementCountAPIView, GoodsCountAPIView
from apps.meiduo_admin.views.user import UserApiView

# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('authorizations', LoginSerializer)

urlpatterns = [
    path('authorizations/', LoginView.as_view()),

    # 日活统计
    path('statistical/day_active/', DailyActiveAPIView.as_view()),
    path('statistical/day_orders/', DailyOrderCountAPIView.as_view()),
    path('statistical/month_increment/', MonthCountAPIView.as_view()),
    # 总人数
    path('statistical/total_count/', TotalCountAPIView.as_view()),
    # 日新增用户
    path('statistical/day_increment/', DayIncrementCountAPIView.as_view()),
    path('statistical/goods_day_views/', GoodsCountAPIView.as_view()),

    # 用户
    path('users/', UserApiView.as_view()),
    path('skus/simple/', ImageSKUAPIView.as_view())
]

from rest_framework.routers import DefaultRouter

rouer = DefaultRouter()
rouer.register('skus/images', ImagesModelViewSet, basename='images')
urlpatterns += rouer.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.areas.views.areas_views import AreaView, SubAreaView

# router = DefaultRouter()
# router.register('addresses', AreaViewSet)
urlpatterns = [
    # path('', include(router.urls)),
    path('areas/', AreaView.as_view()),
    path('areas/<id>/', SubAreaView.as_view()),

]
"""
GET /api/addresses/：获取当前用户的所有收货地址。
POST /api/addresses/：创建一个新的收货地址。
GET /api/addresses/<id>/：获取指定 ID 的收货地址。
PUT /api/addresses/<id>/：更新指定 ID 的收货地址。
PATCH /api/addresses/<id>/：部分更新指定 ID 的收货地址。
DELETE /api/addresses/<id>/：删除指定 ID 的收货地址。
"""
# from django.urls import path
# from apps.areas.views import AreaView, SubAreaView
#
# urlpatterns = [
#     path('areas/', AreaView.as_view()),
#     path('areas/<id>/', SubAreaView.as_view()),
# ]

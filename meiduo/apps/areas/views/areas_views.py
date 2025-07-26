from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.users.models import Address
from apps.areas.serializers.areas_serializers import AreaSerializer
from apps.areas.models import Area
from django.core.cache import cache


class AreaView(APIView):
    def get(self, request):
        provinces = Area.objects.filter(parent=None)
        province_list = []
        for provinces in provinces:
            province_list.append({
                'id': provinces.id,
                'name': provinces.name
            })
        return Response({'code': 0, 'errmsg': 'ok', 'province_list': province_list}, status=status.HTTP_200_OK)


class SubAreaView(APIView):
    def get(self, request, id):
        up_level = Area.objects.get(id=id)
        down_level = up_level.subs.all()
        data_list = []
        for item in down_level:
            data_list.append({
                'id': item.id,
                'name': item.name
            })

        return Response({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}}, status=status.HTTP_200_OK)

# class AreaViewSet(viewsets.ModelViewSet):
#     queryset = Address.objects.all()
#     serializer_class = AreaSerializer
#     # permission_classes = []
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# from django.views.generic.base import View
# from django.http import JsonResponse


#
# class SubAreaView(View):
#     def get(self, request, id):
#         data_list = cache.get(f'city:{id}')
#         if data_list is None:
#             up_level = Area.objects.get(id=id)
#             down_level = up_level.subs.all()
#             data_list = []
#             for item in down_level:
#                 data_list.append({
#                     'id': item.id,
#                     'name': item.name
#                 })
#             cache.set(f'city:{id}', data_list, 24 * 3600)
#         return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}})

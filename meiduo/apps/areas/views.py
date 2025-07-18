from django.views.generic.base import View
from apps.areas.models import Area
from django.http import JsonResponse
from django.core.cache import cache


class AreaView(View):
    def get(self, request):
        province_list = cache.get('province')
        if province_list is None:
            provinces = Area.objects.filter(parent=None)
            province_list = []
            for provinces in provinces:
                province_list.append({
                    'id': provinces.id,
                    'name': provinces.name
                })
            cache.set('province', province_list, 24 * 3600)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})


class SubAreaView(View):
    def get(self, request, id):
        data_list = cache.get(f'city:{id}')
        if data_list is None:
            up_level = Area.objects.get(id=id)
            down_level = up_level.subs.all()
            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                })
            cache.set(f'city:{id}', data_list, 24 * 3600)
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}})

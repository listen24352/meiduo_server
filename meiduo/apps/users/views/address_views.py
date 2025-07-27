from apps.users.models import Address
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class AddressView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1.查询指定数据
        user = request.user
        addresses = Address.objects.filter(user=user, is_deleted=False)

        # 2.将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })

        # 3.返回响应
        return Response({'code': 0, 'errmsg': 'ok', 'addresses': address_list})

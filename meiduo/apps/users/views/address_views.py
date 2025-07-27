from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from apps.users.models import Address
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.serializers.address_serializers import AddressSerializer


class AddressView(APIView):
    # 启用会话认证（适配 Django 登录态）
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

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


class AddressCreateView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        print(data)

        serializer = AddressSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            address = serializer.save(user=request.user)

            # 准备返回数据
            address_dict = {
                'id': address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }

            return Response({'code': 0, 'errmsg': 'ok', 'address': address_dict}, status=status.HTTP_201_CREATED)

        return Response({'code': 400, 'errmsg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

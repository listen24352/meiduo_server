from rest_framework import serializers
from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['receiver', 'province_id', 'city_id', 'district_id', 'place', 'mobile']
        # extra_kwargs = {
        #     'mobile': {'required': True},
        #     'receiver': {'required': True},
        #     'place': {'required': True},
        #     'province_id': {'required': True},
        #     'city_id': {'required': True},
        # }

    def create(self, validated_data):
        print('validated_data', validated_data)
        # 设置默认标题为收货人
        validated_data['title'] = validated_data.get('receiver')
        return super().create(validated_data)

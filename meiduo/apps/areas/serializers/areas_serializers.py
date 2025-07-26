from rest_framework import serializers
from apps.areas.models import Area
from apps.users.models import Address


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'parent']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'title', 'receiver', 'province', 'city', 'district',
                  'place', 'mobile', 'tel', 'email', 'is_deleted']



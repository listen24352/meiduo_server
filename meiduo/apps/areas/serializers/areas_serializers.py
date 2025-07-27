from rest_framework import serializers
from apps.areas.models import Area
from apps.users.models import Address


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'parent']





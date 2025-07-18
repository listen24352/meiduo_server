from rest_framework import serializers
from apps.goods.models import SKUImage, SKU


class SKUImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKUImage
        fields = '__all__'


class ImageSKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'

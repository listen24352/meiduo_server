from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage, SKU
from apps.meiduo_admin.serializer.images import SKUImageModelSerializer, ImageSKUModelSerializer
from apps.meiduo_admin.utils import PageNum
from rest_framework.mixins import ListModelMixin


class ImagesModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum


class ImageSKUAPIView(ListModelMixin, GenericAPIView):
    queryset = SKU.objects.all()
    serializer_class = ImageSKUModelSerializer

    def get(self, request):
        return self.list(request)

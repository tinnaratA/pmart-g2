from rest_framework import serializers
from common.serializers import MdmBaseSerializer

from merchandise.serializers import UnitOfMeasurementSerializer
from merchandise.serializers import MerchandiseMasterItemSerializer
from customer_store.serializers import CustomerStoreTypeSerializer

from . import models


class ProductItemImageSerializer(MdmBaseSerializer):
    
    class Meta:
        model = models.ProductItemImage
        fields = (
            'resource_type',
            'url'
        )


class ProductItemSerializer(MdmBaseSerializer):
    sku = serializers.CharField(max_length=50)
    uom = UnitOfMeasurementSerializer(many=False)
    merchandise = MerchandiseMasterItemSerializer(many=False)
    store_type = CustomerStoreTypeSerializer(many=True, source='product_items')
    images = ProductItemImageSerializer(many=True)

    class Meta:
        model = models.ProductItem
        fields = (
            'resource_type',
            'sku',
            'uom',
            'merchandise',
            'store_type',
            'images'
        )



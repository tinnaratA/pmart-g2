from rest_framework import serializers
from . import models

from common.serializers import MdmBaseSerializer
from common.serializers import HumanNameSerializer
from common.serializers import AddressSerializer

from merchandise.serializers import MerchandiseMasterItemSerializer
from merchandise.serializers import UnitOfMeasurementSerializer


class VendorContactSerializer(MdmBaseSerializer):
    type = serializers.CharField(max_length=20)
    value = serializers.CharField(max_length=256)

    class Meta:
        model = models.VendorContact
        fields = (
            'resource_type',
            'type',
            'value'
        )


class VendorSerializer(MdmBaseSerializer):
    name = HumanNameSerializer(many=False)
    address = AddressSerializer(many=False)
    registered_date = serializers.DateField(required=True)

    contacts = VendorContactSerializer(many=True)

    class Meta:
        model = models.Vendor
        fields = (
            'resource_type'
            'name',
            'address',
            'registered_date',
            'contacts'
        )


class PurchaseItemImageSerializer(MdmBaseSerializer):

    class Meta:
        model = models.PurchaseItemImage
        fields = (
            'resource_type',
            'url'
        )


class PurchaseItemSerializer(MdmBaseSerializer):
    sku = serializers.CharField(max_length=50)
    uom = UnitOfMeasurementSerializer(many=False)
    merchandise = MerchandiseMasterItemSerializer(many=False)
    images = PurchaseItemImageSerializer(many=True)

    class Meta:
        model = models.PurchaseItem
        fields = (
            'resource_type',
            'sku',
            'uom',
            'merchandise',
            'images'
        )


class VendorPurchaseItemSerializer(MdmBaseSerializer):
    purchase = PurchaseItemSerializer(many=False)
    vendor = VendorSerializer(many=False)

    class Meta:
        model = models.VendorPurchaseItem
        fields = (
            'resource_type',
            'purchase',
            'vendor'
        )

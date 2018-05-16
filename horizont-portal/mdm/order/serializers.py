from rest_framework import serializers
from common.serializers import MdmBaseSerializer
from common.serializers import AddressSerializer

from customer_store.serializers import CustomerStoreSerializer

from product.serializers import ProductItemSerializer
from vendor.serializers import PurchaseItemSerializer

from . import models


class SaleDeliveryDetailSerializer(MdmBaseSerializer):
    address = AddressSerializer(many=False)
    store = CustomerStoreSerializer(many=False)

    class Meta:
        model = models.SaleDeliveryDetail
        fields = (
            'resource_type',
            'address',
            'store'
        )


class SaleOrderDetailSerializer(MdmBaseSerializer):
    item = ProductItemSerializer(many=False)
    quantity = serializers.IntegerField(default=1)
    description = serializers.CharField(max_length=2147483647, required=False, default=None, allow_null=True)

    class Meta:
        model = models.SaleOrderDetail
        fields = (
            'resource_type',
            'quantity',
            'description'
        )


class SaleOrderSerializer(MdmBaseSerializer):
    status = serializers.CharField(max_length=10)
    delivery_on = serializers.DateTimeField()
    order_details = SaleOrderDetailSerializer(many=True, source="order_details")
    delivery_details = SaleDeliveryDetailSerializer(many=True)

    class Meta:
        model = models.SaleOrder
        fields = (
            'resource_type',
            'status',
            'delivery_on',
            'order_details',
            'delivery_details'
        )

class PurchaseOrderDetailSerializer(MdmBaseSerializer):
    item = PurchaseItemSerializer(many=False)
    quantity = serializers.IntegerField(default=1)
    description = serializers.CharField(max_length=2147483647, required=False, default=None, allow_null=True)

    class Meta:
        model = models.PurchaseOrderDetail
        fields = (
            'resource_type',
            'item'
            'quantity',
            'description'
        )

class PurchaseOrder(MdmBaseSerializer):
    status = serializers.CharField(max_length=10)
    delivery_on = serializers.DateTimeField()
    order_details = PurchaseOrderDetailSerializer(many=True)

    class Meta:
        model = models.PurchaseOrder
        fields = (
            'resource_type',
            'status',
            'delivery_on',
            'order_details'
        )
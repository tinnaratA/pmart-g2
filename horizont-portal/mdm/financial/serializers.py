from rest_framework import serializers
from common.serializers import MdmBaseSerializer
from order.serializers import SaleOrderSerializer

from . import models

class ArInvoiceSerializer(MdmBaseSerializer):
    order = SaleOrderSerializer(many=False)
    status = serializers.CharField(max_length=20)

    class Meta:
        model = models.ArInvoice
        fields = (
            'resource_type',
            'order',
            'status'
        )

class ArReceiveSerializer(MdmBaseSerializer):
    invoice = ArInvoiceSerializer(many=False)

    class Meta:
        model = models.ArReceive
        fields = (
            'resource_type',
            'invoice'
        )

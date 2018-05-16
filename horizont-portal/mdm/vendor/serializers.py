from rest_framework import serializers
from . import models

from common.serializers import MdmBaseSerializer
from common.serializers import HumanNameSerializer
from common.serializers import AddressSerializer


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




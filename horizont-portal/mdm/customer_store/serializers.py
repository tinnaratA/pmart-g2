from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from common.serializers import MdmBaseSerializer
from common.serializers import HumanNameSerializer, AddressSerializer
from routing.serializers import RouteSerializer

from customer_store import models

excludes = ['id', 'customer_store', 'owner']

class CustomerStoreTypeSerializer(MdmBaseSerializer):
    code = serializers.SlugField(max_length=256)
    name = serializers.CharField(max_length=2147483647)
    parent = RecursiveField(allow_null=True, required=True)

    class Meta:
        model = models.CustomerStoreType
        fields = ['resource_type'] + [f.name for f in models.CustomerStoreType._meta.fields if f.name not in excludes]


class CustomerStoreContactSerializer(MdmBaseSerializer):
    type = serializers.CharField(max_length=20)
    value = serializers.CharField(max_length=256)
    owner = HumanNameSerializer(many=False)

    class Meta:
        model = models.CustomerStoreContact
        fields = ['resource_type'] + [f.name for f in models.CustomerStoreContact._meta.fields if f.name not in excludes]


class CustomerStoreImageSerializer(MdmBaseSerializer):
    image = serializers.ImageField(allow_empty_file=False, use_url=True)

    class Meta:
        model = models.CustomerStoreImage
        fields = ['resource_type'] + [f.name for f in models.CustomerStoreImage._meta.fields if f.name not in excludes]


class CustomerStoreSerializer(MdmBaseSerializer):
    id = serializers.ReadOnlyField()
    store_name = serializers.CharField(max_length=512, allow_null=False, required=True)
    description = serializers.CharField(max_length=2147483647, allow_null=True, required=False, default=None)
    owners = HumanNameSerializer(many=True, source="owner")
    type = CustomerStoreTypeSerializer(many=False)
    address = AddressSerializer(many=False)
    route = RouteSerializer(many=False, allow_null=True)
    contacts = CustomerStoreContactSerializer(many=True, source="customer_store_contacts")
    images = CustomerStoreImageSerializer(many=True, source="customer_store_images")

    class Meta:
        model = models.CustomerStore
        fields = ['resource_type', 'id'] + \
                 [f.name for f in models.CustomerStore._meta.fields] + \
                 [f.name for f in models.CustomerStore._meta.many_to_many if f.name not in excludes] + \
                 ['images', 'contacts', 'owners']

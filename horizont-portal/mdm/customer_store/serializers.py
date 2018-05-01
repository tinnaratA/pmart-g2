from django.conf import settings
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from common.serializers import MdmBaseSerializer, AddressSerializer, HumanNameSerializer

from . import models


class CustomerStoreAddressSerializer(AddressSerializer):
    latitude = serializers.CharField(max_length=50, required=True)
    longitude = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = models.CustomerStoreAddress
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreAddress._meta.fields]


class CustomerStoreTypeSerializer(MdmBaseSerializer):
    code = serializers.SlugField(max_length=256, allow_null=False, allow_blank=False, required=True)
    name = serializers.CharField(max_length=2147483647, allow_blank=False, allow_null=False, required=True)
    parent = RecursiveField()

    class Meta:
        model = models.CustomerStoreType
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreType._meta.fields]


class CustomerGradeSerializer(MdmBaseSerializer):
    higher_grade = RecursiveField()
    grade = serializers.CharField(max_length=10, required=True)
    lower_grade = serializers.ReadOnlyField()

    class Meta:
        model = models.CustomerStoreGrade
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreGrade._meta.fields]


class CustomerStoreContactSerializer(MdmBaseSerializer):
    owner = HumanNameSerializer(many=False, source="customer_store_contact")
    type = serializers.CharField(max_length=20, required=True)
    value = serializers.CharField(max_length=256, required=True)

    class Meta:
        model = models.CustomerStoreContact
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreContact._meta.fields]


class CustomerStoreImageSerializer(MdmBaseSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = models.CustomerStoreImage
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreImage._meta.fields]


class CustomerStoreSerializer(MdmBaseSerializer):
    store_name = serializers.CharField(max_length=512, allow_null=False, allow_blank=False, required=True)
    owners = HumanNameSerializer(many=True, source="customer_stores", required=True)
    description = serializers.CharField(max_length=2147483647, allow_blank=True, allow_null=True, required=False, default=None)
    type = CustomerStoreTypeSerializer(many=False, source="customer_stores", required=True)
    address = CustomerStoreAddressSerializer(many=False, source="customer_store", required=True)
    grade = CustomerGradeSerializer(many=False, required=False, default="D")
    contacts = CustomerStoreContactSerializer(many=True, source="customer_store_contacts")
    images = CustomerStoreImageSerializer(many=True, source="customer_store_images")

    class Meta:
        model = models.CustomerStore
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStore._meta.fields] + \
                 ['owners', 'contacts', 'images']

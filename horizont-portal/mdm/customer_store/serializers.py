from rest_framework import serializers

from common.serializers import MdmBaseSerializer

from customer_store import models


class CustomerStoreTypeSerializer(MdmBaseSerializer):

    class Meta:
        model = models.CustomerStoreType
        fields = ['resource_type'] + [f.name for f in models.CustomerStoreType._meta.fields]


class CustomerStoreSerializer(MdmBaseSerializer):

    class Meta:
        model = models.CustomerStore
        fields = ['resource_type'] + [f.name for f in models.CustomerStoreType._meta.fields]


class CustomerStoreContactSerializer(MdmBaseSerializer):

    class Meta:
        model = models.CustomerContact
        fields = ['resource_type'] + [f.name for f in models.CustomerContact._meta.fields]


class CustomerStoreImageSerializer(MdmBaseSerializer):

    class Meta:
        model = models.CustomerStoreImage
        fields = ['resource_type'] + [f.name for f in models.CustomerStoreImage._meta.fields]


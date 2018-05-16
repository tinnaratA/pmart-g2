from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from common.serializers import MdmBaseSerializer

from . import models


class MerchandiseCategorySerializer(MdmBaseSerializer):
    name = serializers.CharField(max_length=128)
    slug = serializers.SlugField(max_length=128)
    description = serializers.CharField(max_length=2147483647)
    parent = RecursiveField(allow_null=True, required=True)

    class Meta:
        model = models.MerchandiseCategory
        fields = (
            'resource_type',
            'name',
            'slug',
            'description',
            'parent'
        )


class MerchandiseMasterItemSerializer(MdmBaseSerializer):
    code = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=2147483647)
    category = MerchandiseCategorySerializer(many=False)
    price = serializers.FloatField(default=1.00)
    available_on = serializers.DateField()
    is_published = serializers.BooleanField(default=True)
    updated_at = serializers.DateTimeField()
    is_featured = serializers.BooleanField(default=False)

    class Meta:
        model = models.MerchandiseMasterItem
        fields = (
            'resource_type',
            'code',
            'name',
            'description',
            'category',
            'price',
            'available_on',
            'is_published',
            'is_featured'
        )


class UnitOfConversionSerializer(MdmBaseSerializer):
    name = serializers.CharField(max_length=50)
    factor = serializers.FloatField(default=None)

    class Meta:
        model = models.UnitOfConversion
        fields = (
            'resource_type',
            'name',
            'factor'
        )


class UnitOfMeasurementSerializer(MdmBaseSerializer):
    merchandise = MerchandiseMasterItemSerializer(many=False)
    name = serializers.CharField(max_length=50)
    unit_conversions = UnitOfConversionSerializer(many=True, source="uoms")

    class Meta:
        model = models.UnitOfMeasurement
        fields= (
            'resource_type',
            'merchandise',
            'name',
            'unit_conversions'
        )

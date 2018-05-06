from rest_framework import serializers
from .models.models import HumanName, Address

excludes = ['id']

class MdmBaseSerializer(serializers.ModelSerializer):
    resource_type = serializers.SerializerMethodField()
    id = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField(required=False)
    updated = serializers.ReadOnlyField(required=False)

    def get_resource_type(self, obj):
        return self.Meta.model.__name__


class HumanNameSerializer(MdmBaseSerializer):
    title = serializers.CharField(max_length=20, required=True)
    first = serializers.CharField(max_length=512, required=True)
    middle = serializers.CharField(max_length=512, required=True, allow_null=True, allow_blank=True)
    last = serializers.CharField(max_length=512, required=True)

    class Meta:
        model = HumanName
        fields = ['resource_type'] + [f.name for f in HumanName._meta.fields if f.name not in excludes]

    def create(self, validated_data):
        instance, created = HumanName.objects.update_or_create(**validated_data)
        return instance


class AddressSerializer(MdmBaseSerializer):
    line1 = serializers.CharField(max_length=2147483647)
    line2 = serializers.CharField(max_length=2147483647, allow_null=True, allow_blank=True)
    district = serializers.CharField(max_length=256)
    city = serializers.CharField(max_length=256)
    province = serializers.CharField(max_length=256)
    postcode = serializers.CharField(max_length=256)

    class Meta:
        model = Address
        fields = ['resource_type'] + [f.name for f in Address._meta.fields if f.name not in excludes]

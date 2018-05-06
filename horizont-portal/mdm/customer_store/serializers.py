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
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreAddress._meta.fields if '_ptr' not in f.name]

    def create(self, validated_data):
        instance, created = models.CustomerStoreAddress.objects.update_or_create(**validated_data)
        return instance


class CustomerStoreTypeSerializer(MdmBaseSerializer):
    code = serializers.SlugField(max_length=256, allow_null=False, allow_blank=False, required=True)
    name = serializers.CharField(max_length=2147483647, allow_blank=False, allow_null=False, required=True)
    parent = RecursiveField(allow_null=True)

    class Meta:
        model = models.CustomerStoreType
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreType._meta.fields]

    def create(self, validated_data):
        parent = validated_data.pop('parent')
        if parent:
            parent = self.create(parent)

        instance, created = models.CustomerStoreType.objects.update_or_create(parent=parent, **validated_data)
        return instance


class CustomerGradeSerializer(MdmBaseSerializer):
    grade = serializers.CharField(max_length=10, required=True)

    class Meta:
        model = models.CustomerStoreGrade
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + ['grade']

    def create(self, validated_data):
        fix_grade_list = [g[0] for g in models.CustomerStoreGrade.GRADES]
        length = len(fix_grade_list)
        grade = validated_data['grade']
        index = fix_grade_list.index(grade)
        if index == length - 1:
            validated_data['higher_grade'] = models.CustomerStoreGrade.objects.get(grade=fix_grade_list[index-1])
            validated_data['lower_grade'] = None
        elif index == 0:
            validated_data['higher_grade'] = None
            validated_data['lower_grade'] = models.CustomerStoreGrade.objects.get(grade=fix_grade_list[index+1])
        else:
            validated_data['higher_grade'] = models.CustomerStoreGrade.objects.get(grade=fix_grade_list[index-1])
            validated_data['lower_grade'] = models.CustomerStoreGrade.objects.get(grade=fix_grade_list[index + 1])

        instance, created = models.CustomerStoreGrade.objects.update_or_create(**validated_data)
        return instance


class CustomerStoreContactSerializer(MdmBaseSerializer):
    owner = HumanNameSerializer(many=False)
    type = serializers.CharField(max_length=20, required=True)
    value = serializers.CharField(max_length=256, required=True)

    class Meta:
        model = models.CustomerStoreContact
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreContact._meta.fields if f.name not in ['store']]


class CustomerStoreImageSerializer(MdmBaseSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = models.CustomerStoreImage
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStoreImage._meta.fields]


class CustomerStoreSerializer(MdmBaseSerializer):
    store_name = serializers.CharField(max_length=512, allow_null=False, allow_blank=False, required=True)
    owners = HumanNameSerializer(many=True, required=True)
    description = serializers.CharField(max_length=2147483647, allow_blank=True, allow_null=True, required=False, default=None)
    type = CustomerStoreTypeSerializer(many=False, required=True)
    address = CustomerStoreAddressSerializer(many=False, required=True)
    grade = CustomerGradeSerializer(many=False, required=True)
    contacts = CustomerStoreContactSerializer(many=True, source="customer_store_contacts")
    images = CustomerStoreImageSerializer(many=True, source="customer_store_images", read_only=True)

    class Meta:
        model = models.CustomerStore
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.CustomerStore._meta.fields] + \
                 ['owners', 'contacts', 'images']

    def create(self, validated_data):
        address = validated_data.pop('address')
        contacts = validated_data.pop('customer_store_contacts')
        grade = validated_data.pop('grade')
        owners = validated_data.pop('owners')
        cstype = validated_data.pop('type')

        address_serializer = CustomerStoreAddressSerializer(data=address, many=False)
        if address_serializer.is_valid():
            address = address_serializer.save()
        else:
            return address_serializer.errors

        grade_serializer = CustomerGradeSerializer(data=grade, many=False)
        if grade_serializer.is_valid():
            grade = grade_serializer.save()
        else:
            return grade_serializer.errors

        cstype_serializer = CustomerStoreTypeSerializer(data=cstype, many=False)
        if cstype_serializer.is_valid():
            cstype = cstype_serializer.save()
        else:
            return cstype_serializer.errors

        instance, created = models.CustomerStore.objects.update_or_create(
            address=address,
            grade=grade,
            type=cstype,
            **validated_data
        )

        name_serializer = HumanNameSerializer(data=owners, many=True)
        if name_serializer.is_valid():
            names = name_serializer.save()
            instance.owners.add(*names)
        else:
            return name_serializer.errors

        for contact in contacts:
            owner = contact.pop('owner')
            name_serializer = HumanNameSerializer(data=owner, many=False)
            if name_serializer.is_valid():
                name = name_serializer.save()
            else:
                return name_serializer.errors
            models.CustomerStoreContact.objects.update_or_create(owner=name, store=instance, **contact)

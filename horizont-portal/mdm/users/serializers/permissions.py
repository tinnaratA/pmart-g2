from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import Permission, PermissionManager, ContentType
from common.serializers import MdmBaseSerializer


class ContentTypeSerializer(MdmBaseSerializer):
    id = serializers.ReadOnlyField(required=False)
    app_label = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        required=True
    )
    model = serializers.CharField(
        max_length=50,
        allow_null=False,
        allow_blank=False,
        required=True,
    )

    class Meta:
        model = ContentType
        fields = ['resource_type'] + [f.name for f in ContentType._meta.fields]
        validators = []


class PermissionSerializer(MdmBaseSerializer):
    id = serializers.ReadOnlyField(required=False)
    name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False, required=True)
    content_type = ContentTypeSerializer(many=False)
    codename = serializers.CharField(max_length=100, allow_blank=False, allow_null=False, required=True)

    class Meta:
        model = Permission
        fields = ['resource_type'] + [f.name for f in Permission._meta.fields]

    def create(self, validated_data):
        content, created = ContentType.objects.get_or_create(**validated_data.pop('content_type'))
        instance, created = Permission.objects.update_or_create(content_type=content, **validated_data)
        return instance

    def update(self, instance, validated_data):
        if 'content_type' in validated_data.keys():
            content_validated_data = validated_data.pop('content_type')
            content = instance.content_type
            [setattr(content, key, content_validated_data[key]) for key in content_validated_data.keys()]
            content.save()
        else:
            content = instance.content_type
        validated_data['content_type'] = content
        [setattr(instance, key, validated_data[key]) for key in validated_data.keys()]
        instance.save()
        return instance

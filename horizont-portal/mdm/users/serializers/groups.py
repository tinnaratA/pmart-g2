from rest_framework import serializers
from django.contrib.auth.models import Group, GroupManager
from common.serializers import MdmBaseSerializer
from users.serializers.permissions import PermissionSerializer


class GroupSerializer(MdmBaseSerializer):
    id = serializers.ReadOnlyField(required=False)
    name = serializers.CharField(max_length=80, allow_null=False, allow_blank=False, required=True)
    permissions = PermissionSerializer(
        many=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Group
        fields = ['resource_type', 'permissions'] + [f.name for f in Group._meta.fields]

    def create(self, validated_data):
        instance, created = Group.objects.update_or_create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        [setattr(instance, key, validated_data[key]) for key in validated_data.keys()]
        instance.save()
        return instance

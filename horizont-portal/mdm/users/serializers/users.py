from django.contrib.auth.models import User, UserManager
from rest_framework import serializers
from common.serializers import MdmBaseSerializer


class UserSerializer(MdmBaseSerializer):
    id = serializers.ReadOnlyField(required=False)
    password = serializers.CharField(max_length=128, required=True, allow_null=False, allow_blank=False)
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)

    is_superuser = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['resource_type'] + [f.name for f in User._meta.fields]

    def create(self, validated_data):
        manager = UserManager()
        manager.model = User
        user = manager.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            **validated_data
        )
        return user

    def update(self, instance, validated_data):
        [setattr(instance, key, validated_data[key]) for key in validated_data.keys()]
        instance.save()
        return instance

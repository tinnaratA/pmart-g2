from rest_framework import serializers
from common.serializers import MdmBaseSerializer
from users.serializers.users import UserSerializer
from routing.models import Route


class RouteSerializer(MdmBaseSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=256)
    sale = UserSerializer(many=False)

    class Meta:
        model = Route
        fields = ['resource_type'] + [f.name for f in Route._meta.fields]

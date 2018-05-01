from django.conf import settings
from rest_framework import serializers
from common.serializers import MdmBaseSerializer
from customer_store.serializers import CustomerStoreSerializer
from users.serializers import UserSerializer

from . import models


class RouteSerializer(MdmBaseSerializer):
    name = serializers.CharField(max_length=256, allow_null=False, allow_blank=False)

    class Meta:
        model = models.Route
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.Route._meta.fields]


class RouteCustomerStoreSerializer(MdmBaseSerializer):
    route = RouteSerializer(many=False, required=True)
    store = CustomerStoreSerializer(many=False, required=True)

    class Meta:
        model = models.RouteCustomerStore
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.RouteCustomerStore._meta.fields]


class RouteTaskOrderSerializer(MdmBaseSerializer):
    pass



class RouteActivityTaskSerializer(MdmBaseSerializer):
    executed_by = UserSerializer(many=False)
    # task_orders =
    # task_questionaire

    class Meta:
        model = models.RouteActivityTask
        fields = ('executed_by', 'task_orders', 'task_questionaire')


class RouteActivitySerializer(MdmBaseSerializer):
    route_stores = CustomerStoreSerializer(many=False, required=True)
    schedule_datetime = serializers.DateTimeField(required=True)
    status = serializers.CharField(max_length=4, required=True, allow_null=False, allow_blank=False, default='SCHE')
    created_by = UserSerializer(many=False, required=True)
    updated_by = UserSerializer(many=False, required=True)
    # tasks =

    class Meta:
        model = models.RouteActivity
        fields = settings.SERIALIZER_MUST_HAVE_FIELDS + [f.name for f in models.RouteActivity._meta.fields] + \
                 ['tasks']



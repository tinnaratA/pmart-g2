from django.conf import settings
from rest_framework import serializers
from common.serializers import MdmBaseSerializer
from customer_store.serializers import CustomerStoreSerializer
from users.serializers import UserSerializer
from order.serializers import SaleOrderSerializer
from questionaire.serializers import QuestionaireAnswerSerializer

from . import models


class RouteSerializer(MdmBaseSerializer):
    name = serializers.CharField(max_length=256, allow_null=True, allow_blank=True, required=True)

    class Meta:
        model = models.Route
        fields = (
            'resource_type',
            'name'
        )


class RouteTaskQuestionaireSerializer(MdmBaseSerializer):
    question = QuestionaireAnswerSerializer(many=False)

    class Meta:
        model = models.RouteTaskQuestionaire
        fields = (
            'resource_type'
            'question'
        )


class RouteTaskOrderSerializer(MdmBaseSerializer):
    orders = SaleOrderSerializer(many=True)
    
    class Meta:
        model = models.RouteTaskOrder
        fields = (
            'resource_type',
            'orders'
        )

    
class RouteActivityTaskSerializer(MdmBaseSerializer):
    executed_by = UserSerializer(many=False)
    task_orders = RouteTaskOrderSerializer(many=True)
    task_questionaire = RouteTaskQuestionaireSerializer(many=True)

    class Meta:
        model = models.RouteActivityTask
        fields = (
            'resource_type',
            'executed_by',
            'task_orders',
            'task_questionaire'
        )


class RouteActivitySerializer(MdmBaseSerializer):
    schedule_datetime = serializers.DateTimeField(required=True)
    status = serializers.CharField(max_length=4)
    created_by = UserSerializer(many=False)
    updated_by = UserSerializer(many=False)
    tasks = RouteActivityTaskSerializer(many=True, source="route_tasks")

    class Meta:
        model = models.RouteActivity
        fields = (
            'resource_type',
            'schedule_datetime',
            'status',
            'created_by',
            'updated_by',
            'tasks'
        )


class RouteCustomerStoreSerializer(MdmBaseSerializer):
    route = RouteSerializer(many=False)
    store = CustomerStoreSerializer(many=False)
    status = serializers.CharField(max_length=10, allow_null=True, allow_blank=False, required=True)
    comment = serializers.CharField(max_length=10, allow_null=True, default=None, required=False)

    class Meta:
        model = models.RouteCustomerStore
        fields = (
            'resource_type',
            'route',
            'store',
            'status',
            'comment'
        )




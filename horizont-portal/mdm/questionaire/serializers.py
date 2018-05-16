from rest_framework import serializers
from common.serializers import MdmBaseSerializer

from customer_store.serializers import CustomerStoreTypeSerializer, CustomerStoreSerializer

from . import models

class QuestionaireTemplateSerializer(MdmBaseSerializer):
    store_type = CustomerStoreTypeSerializer(many=True, source="questionaires")
    question = serializers.CharField(max_length=2000000, required=True)

    class Meta:
        model = models.QuestionaireTemplate
        fields = (
            'resource_type',
            'store_type',
            'question'
        )


class QuestionaireAnswerSerializer(MdmBaseSerializer):
    question = QuestionaireTemplateSerializer(many=False)
    answer = serializers.IntegerField(required=True)
    store = CustomerStoreSerializer(many=False)

    class Meta:
        model = models.QuestionaireAnswer
        fields = (
            'resource_type',
            'question',
            'answer',
            'store'
        )

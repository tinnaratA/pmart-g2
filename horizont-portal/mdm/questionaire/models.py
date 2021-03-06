import uuid
from django.db import models
from common.models.abstracts import TimeStampMixin
from customer_store.models import CustomerStoreType, CustomerStore


class QuestionaireTemplate(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    store_type = models.ManyToManyField(
        CustomerStoreType,
        related_name="questionaires"
    )
    question = models.TextField()

    class Meta:
        app_label = 'questionaire'
        db_table = 'questionaire_template'


class QuestionaireAnswer(models.Model):
    question = models.ForeignKey(QuestionaireTemplate, related_name="answers", on_delete=models.CASCADE)
    answer = models.IntegerField()
    store = models.ForeignKey(CustomerStore, related_name="questions", on_delete=models.CASCADE)

    class Meta:
        app_label = 'questionaire'
        db_table = 'questionaire_answer'

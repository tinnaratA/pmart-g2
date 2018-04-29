import uuid
from django.db import models
from common.models.abstracts import TimeStampMixin
from order.models import SaleOrder


class ArInvoice(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    order = models.OneToOneField(SaleOrder, related_name="invoice", on_delete=models.CASCADE)

    class Meta:
        app_label = 'financial'
        db_table = 'ar_invoice'

    def __str__(self):
        return self.id


class ArReceive(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    invoice = models.OneToOneField(ArInvoice, related_name="ar_receive", on_delete=models.CASCADE)

    class Meta:
        app_label = 'financial'
        db_table = 'ar_receive'

    def __str__(self):
        return self. id

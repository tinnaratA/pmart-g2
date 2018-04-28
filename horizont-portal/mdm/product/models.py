import uuid

from django.db import models
from common.models.abstracts import TimeStampMixin
from merchandise.models import MerchandiseMasterItem, UnitOfMeasurement
# from customer_store.models import CustomerStoreType

# Customer store SKU
class ProductItem(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    sku = models.CharField(max_length=50)
    uom = models.ForeignKey(
        UnitOfMeasurement,
        related_name="product_items",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True
    )
    merchandise = models.ForeignKey(MerchandiseMasterItem, related_name="product_items", on_delete=models.CASCADE)
    store_type = models.ForeignKey(
        to="customer_store.CustomerStoreType",
        related_name="product_items",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True
    )

    class Meta:
        app_label = 'product'
        db_table = 'product_item'

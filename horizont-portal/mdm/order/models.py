import uuid
from django.db import models
from common.models.abstracts import TimeStampMixin
from common.models.models import Address
from routing.models import RouteTaskOrder
from product.models import ProductItem
from customer_store.models import CustomerStore
from vendor.models import PurchaseItem


class SaleOrder(TimeStampMixin):
    RAISED = 'Raised'
    COMFIRMED = 'Confirmed'
    DELIVERED = 'Delivered'
    PAID = 'Paid'
    CANCEL = 'Cancel'
    ORDER_STATUS = (
        (RAISED, RAISED),
        (COMFIRMED, COMFIRMED),
        (DELIVERED, DELIVERED),
        (PAID, PAID),
        (CANCEL, CANCEL)
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    task = models.ForeignKey(RouteTaskOrder, related_name="orders", null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default=RAISED, choices=ORDER_STATUS)
    delivery_on = models.DateTimeField()

    class Meta:
        app_label = 'order'
        db_table = 'sale_order'

    def __str__(self):
        return self.id

    def get_status_choice(self):
        return self.ORDER_STATUS


class SaleOrderDetail(models.Model):
    order = models.ForeignKey(SaleOrder, related_name='order_details', on_delete=models.CASCADE)
    item = models.ForeignKey(ProductItem, related_name="order_details", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    description = models.TextField(default=None, null=True, blank=True)

    class Meta:
        app_label = 'order'
        db_table = 'sale_order_detail'

    def __str__(self):
        return f"detail of {self.id} of order id {self.order.id}"


class SaleDeliveryDetail(models.Model):
    order = models.ForeignKey(SaleOrder, related_name='delivery_details', on_delete=models.CASCADE)
    company_address = models.ForeignKey(Address, on_delete=models.SET_DEFAULT, default=None, null=True)
    store = models.ForeignKey(CustomerStore, related_name="delivery_details", on_delete=models.CASCADE)

    class Meta:
        app_label = 'order'
        db_table = 'sale_delivery_detail'


class PurchaseOrder(TimeStampMixin):
    RAISED = 'Raised'
    COMFIRMED = 'Confirmed'
    DELIVERED = 'Delivered'
    PAID = 'Paid'
    CANCEL = 'Cancel'
    ORDER_STATUS = (
        (RAISED, RAISED),
        (COMFIRMED, COMFIRMED),
        (DELIVERED, DELIVERED),
        (PAID, PAID),
        (CANCEL, CANCEL)
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    status = models.CharField(max_length=10, default=RAISED, choices=ORDER_STATUS)
    delivery_on = models.DateTimeField()

    class Meta:
        app_label = 'order'
        db_table = 'purchase_order'

    def __str__(self):
        return str(self.id)

    def get_status_choice(self):
        return self.ORDER_STATUS


class PurchaseOrderDetail(models.Model):
    order = models.ForeignKey(PurchaseOrder, related_name='order_details', on_delete=models.CASCADE)
    item = models.ForeignKey(PurchaseItem, related_name="order_details", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    description = models.TextField(default=None, null=True, blank=True)

import uuid
from django.db import models
from common.models.abstracts import TimeStampMixin, AbstractContact
from common.models.models import Address, HumanName
from merchandise.models import MerchandiseMasterItem, UnitOfMeasurement



class Vendor(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.ForeignKey(HumanName, on_delete=models.SET_DEFAULT, default=None, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_DEFAULT, default=None, null=True)
    registered_date = models.DateField()


    class Meta:
        app_label = 'vendor'
        db_table = 'vendor'


class VendorContact(AbstractContact):
    vendor = models.ForeignKey(Vendor, related_name="contacts", on_delete=models.CASCADE)

    class Meta:
        app_label = 'vendor'
        db_table = 'vendor_contact'


# Vendor SKU
class PurchaseItem(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    vendor = models.ForeignKey(Vendor, related_name="perchase_items", on_delete=models.CASCADE)
    uom = models.ForeignKey(
        UnitOfMeasurement,
        related_name="purchase_items",
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True
    )
    merchandise = models.ForeignKey(MerchandiseMasterItem, related_name="purchase_items", on_delete=models.CASCADE)

    class Meta:
        app_label = 'vendor'
        db_table = 'purchase_item'

import uuid
from django.db import models
from django.utils.translation import pgettext_lazy
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

    def get_full_name(self):
        return str(self.name)


class VendorContact(AbstractContact):
    vendor = models.ForeignKey(Vendor, related_name="contacts", on_delete=models.CASCADE)

    class Meta:
        app_label = 'vendor'
        db_table = 'vendor_contact'


# Vendor SKU
class PurchaseItem(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    sku = models.CharField(max_length=50)
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


class PurchaseItemImage(TimeStampMixin):
    purchase = models.ForeignKey(PurchaseItem, related_name="images", on_delete=models.CASCADE)
    abspath = models.CharField(max_length=256)

    class Meta:
        app_label = 'vendor'
        db_table = 'purchase_item_image'
        permissions = (
            ('view_purchaseitemimage', pgettext_lazy('Permission description', 'Can view purchase item images')),
        )

    def __str__(self):
        return f"Image of {self.purchase.sku}"

    @property
    def url(self):
        return os.path.join(settings.MEDIA_URL, "/".join(self.abspath.split("/")[-2:]))

    @property
    def binary_image(self):
        fp = open(self.abspath, mode="rb")
        content = fp.read()
        fp.close()
        return content


class VendorPurchaseItem(models.Model):
    purchase = models.ForeignKey(PurchaseItem, related_name="vendors", on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="purchase_items", on_delete=models.CASCADE)

    class Meta:
        app_label = 'vendor'
        db_table = 'vendor_purchase_item'

    def __str__(self):
        return f"{self.purchase.sku} of {self.vendor.get_full_name()}"

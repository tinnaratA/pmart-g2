import uuid

from django.conf import settings
from django.utils.translation import pgettext_lazy
from django.db import models
from common.models.abstracts import TimeStampMixin
from merchandise.models import MerchandiseMasterItem, UnitOfMeasurement

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
    store_type = models.ManyToManyField(to="customer_store.CustomerStoreType", related_name="product_items")

    class Meta:
        app_label = 'product'
        db_table = 'product_item'


class ProductItemImage(TimeStampMixin):
    product = models.ForeignKey(ProductItem, related_name="images", on_delete=models.CASCADE)
    abspath = models.CharField(max_length=256)

    class Meta:
        app_label = 'product'
        db_table = 'product_item_image'
        permissions = (
            ('view_productitemimage', pgettext_lazy('Permission description', 'Can view product item images')),
        )

    def __str__(self):
        return f"Image of {self.product.sku}"

    @property
    def url(self):
        return os.path.join(settings.MEDIA_URL, "/".join(self.abspath.split("/")[-2:]))

    @property
    def binary_image(self):
        fp = open(self.abspath, mode="rb")
        content = fp.read()
        fp.close()
        return content

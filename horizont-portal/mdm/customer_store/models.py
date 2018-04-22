import uuid

from django.db import models
from django.utils.translation import pgettext_lazy

from mptt.managers import TreeManager
from mptt.models import MPTTModel

class CustomerStoreType(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    slug = models.SlugField(max_length=256, null=False, blank=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_type'
        permissions = (
            'view_customer_store_type', pgettext_lazy('Permission description', '')
        )



class CustomerStore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=512, blank=False, null=True)
    description = models.TextField(null=True, blank=False)


    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store'
        permissions = (
            ('can_view', pgettext_lazy('Permission description', 'Can view customer stores')),
        )

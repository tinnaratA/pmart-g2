import uuid
from text_unidecode import unidecode

from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.encoding import smart_text
from django.utils.text import slugify

from mptt.managers import TreeManager
from mptt.models import MPTTModel

from common.models.models import Address, HumanName
from common.models.abstracts import AbstractContact, TimeStampMixin
from routing.models import Route


class CustomerStoreAddress(Address, TimeStampMixin):
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_address'
        permissions = (
            ('view_customerstoreaddress', pgettext_lazy('Permission description', 'Can view customer store addresses')),
        )


class CustomerStoreType(MPTTModel, TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    code = models.SlugField(max_length=256, null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_type'
        permissions = (
            ('view_customerstoretype', pgettext_lazy('Permission description', 'Can view customer store types')),
        )


class CustomerStore(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    store_name = models.CharField(max_length=512, blank=False, null=True)
    owner = models.ManyToManyField(HumanName, related_name='customer_stores')
    description = models.TextField(null=True, blank=False)
    type = models.ForeignKey(CustomerStoreType, related_name='customer_stores', on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerStoreAddress, related_name='customer_store', on_delete=models.CASCADE)
    route = models.ForeignKey(Route, related_name='customer_store', null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store'
        permissions = (
            ('view_customerstore', pgettext_lazy('Permission description', 'Can view customer stores')),
        )


class CustomerStoreContact(AbstractContact, TimeStampMixin):
    owner = models.ForeignKey(HumanName, related_name='customer_store_contacts', on_delete=models.CASCADE)
    customer_store = models.ForeignKey(CustomerStore, related_name='customer_store_contacts', null=False, on_delete=models.CASCADE)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_contact'
        permissions = (
            ('view_customerstorecontact', pgettext_lazy('Permission description', 'Can view customer store contacts')),
        )


class CustomerStoreImage(TimeStampMixin):
    customer_store = models.ForeignKey(CustomerStore, related_name='images', null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='customer_store_images')

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_image'
        permissions = (
            ('view_customerstoreimage', pgettext_lazy('Permission description', 'Can view customer stores images')),
        )

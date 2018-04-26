import uuid

from django.db import models
from django.utils.translation import pgettext_lazy


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    line1 = models.TextField(null=False, blank=False)
    line2 = models.TextField(null=True, blank=False)
    district = models.CharField(max_length=256, null=False, blank=False)
    city = models.CharField(max_length=256, null=False, blank=False)
    province = models.CharField(max_length=256, null=False, blank=False)
    postcode = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        app_label = 'common'
        db_table = 'address'
        permissions = (
            ('view_address', pgettext_lazy('Permission description', 'Can view common addresses')),
        )


class HumanName(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    first = models.CharField(max_length=512, null=False, blank=False)
    middle = models.CharField(max_length=512, null=True, blank=True)
    last = models.CharField(max_length=512, null=False, blank=False)

    class Meta:
        app_label = 'common'
        db_table = 'human_name'
        permissions = (
            ('view_name', pgettext_lazy('Permission description', 'Can view human names')),
        )

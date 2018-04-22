from django.db import models


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractContact(models.Model):
    type = models.CharField(max_length=20)
    value = models.CharField(max_length=256)

    class Meta:
        abstract = True

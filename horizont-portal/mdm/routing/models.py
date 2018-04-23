import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy

from common.models.abstracts import TimeStampMixin


class Route(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    sale = models.ForeignKey(User, related_name='route', null=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'routing'
        db_table = 'route'
        permissions = (
            ('view_route', pgettext_lazy('Permission description', 'Can view routes')),
        )

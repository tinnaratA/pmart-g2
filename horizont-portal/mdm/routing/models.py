import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy

from common.models.abstracts import TimeStampMixin
from customer_store.models import CustomerStore


class Route(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=256, null=False, blank=False)
    stores = models.ManyToManyField(CustomerStore, through='RouteCustomerStore')

    class Meta:
        app_label = 'routing'
        db_table = 'route'
        permissions = (
            ('view_route', pgettext_lazy('Permission description', 'Can view routes')),
        )


class RouteCustomerStore(TimeStampMixin):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    store = models.ForeignKey(CustomerStore, on_delete=models.CASCADE)

    class Meta:
        app_label = 'routing'
        db_table = 'route_customer'


class RouteActivity(TimeStampMixin):
    SCHE = 'SCHE'
    FUTU = 'FUTU'
    EXEC = 'EXEC'
    ACTIVITY_STATUS = (
        (SCHE, 'Scheduled'),
        (FUTU, 'Future'),
        (EXEC, 'Executed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    route_stores = models.ForeignKey(RouteCustomerStore, on_delete=models.CASCADE)
    schedule_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=4,
        choices=ACTIVITY_STATUS,
        default=SCHE
    )
    created_by = models.ForeignKey(User, related_name='create_route_activities', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='update_route_activities', on_delete=models.CASCADE)

    class Meta:
        app_label = 'routing'
        db_table = 'route_activity'


class RouteActivityTask(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    activity = models.ForeignKey(RouteActivity, related_name="route_tasks", on_delete=models.CASCADE)
    executed_by = models.ForeignKey(User, related_name="route_tasks", on_delete=models.CASCADE)

    class Meta:
        app_label = "routing"
        db_table = "route_activity_task"

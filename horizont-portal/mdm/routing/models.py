import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy

from common.models.abstracts import TimeStampMixin
from customer_store.models import CustomerStore
from questionaire.models import QuestionaireTemplate


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

    def __str__(self):
        return self.name

    def get_store_ids(self):
        return [str(store.id) for store in self.stores.all()]

class RouteCustomerStore(TimeStampMixin):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    store = models.ForeignKey(CustomerStore, on_delete=models.CASCADE)

    class Meta:
        app_label = 'routing'
        db_table = 'route_customer'

    def __str__(self):
        return f"{self.route.name} - {self.store.store_name}"


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

    def __str__(self):
        return f"Acitivity of {self.route_stores.route.name} - {self.route_stores.store.store_name}"

    def get_all_status(self):
        return [s[1] for s in self.ACTIVITY_STATUS]


class RouteActivityTask(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    activity = models.ForeignKey(RouteActivity, related_name="route_tasks", on_delete=models.CASCADE)
    executed_by = models.ForeignKey(User, related_name="route_tasks", on_delete=models.CASCADE)

    class Meta:
        app_label = "routing"
        db_table = "route_activity_task"

    def __str__(self):
        return self.executed_by.username

class RouteTaskOrder(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    activity = models.ForeignKey(RouteActivityTask, related_name="task_orders", on_delete=models.CASCADE)

    class Meta:
        app_label = 'routing'
        db_table = 'route_task_order'


class RouteTaskQuestionaire(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    activity = models.OneToOneField(RouteActivityTask, related_name="task_questionaire", on_delete=models.CASCADE)
    questions = models.ManyToManyField(QuestionaireTemplate)

    class Meta:
        app_label = 'routing'
        db_table = 'route_task_questionaire'

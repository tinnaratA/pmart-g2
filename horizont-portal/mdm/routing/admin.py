from django.contrib import admin
from . import models

admin.site.register(models.Route)
admin.site.register(models.RouteCustomerStore)
admin.site.register(models.RouteActivity)
admin.site.register(models.RouteActivityTask)
admin.site.register(models.RouteTaskOrder)
admin.site.register(models.RouteTaskQuestionaire)

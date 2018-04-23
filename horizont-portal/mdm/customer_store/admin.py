from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.CustomerStoreType)
admin.site.register(models.CustomerStore)
admin.site.register(models.CustomerStoreAddress)
admin.site.register(models.CustomerStoreContact)
admin.site.register(models.CustomerStoreImage)

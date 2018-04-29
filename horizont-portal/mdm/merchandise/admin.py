from django.contrib import admin
from . import models

admin.site.register(models.MerchandiseMasterItem)
admin.site.register(models.MerchandiseCategory)
admin.site.register(models.MerchandiseImage)
admin.site.register(models.MerchandiseVariant)
admin.site.register(models.VariantImage)
admin.site.register(models.Collection)
admin.site.register(models.UnitOfMeasurement)
admin.site.register(models.UnitOfConversion)
from django.contrib import admin
from . import models

admin.site.register(models.Vendor)
admin.site.register(models.VendorContact)
admin.site.register(models.PurchaseItem)
admin.site.register(models.VendorPurchaseItem)

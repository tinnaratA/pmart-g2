from django.contrib import admin
from . import models


admin.site.register(models.SaleOrder)
admin.site.register(models.SaleOrderDetail)
admin.site.register(models.SaleDeliveryDetail)
admin.site.register(models.PurchaseOrder)
admin.site.register(models.PurchaseOrderDetail)

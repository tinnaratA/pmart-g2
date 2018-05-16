from django.contrib import admin

from . import models

class CustomerStoreTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'parent']
    search_fields = ['code', 'name', 'parent__code', 'parent__name']
    list_display_links = ['id', 'parent']

class CustomerStoreAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_address', 'latitude', 'longitude']
    search_fields = ['line1', 'line2', 'districe', 'city', 'province', 'postcode', 'latitude', 'longitude']
    list_display_links = ['id']

class CustomerStoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'store_name', 'description']

# Register your models here.
admin.site.register(models.CustomerStoreType, CustomerStoreTypeAdmin)
admin.site.register(models.CustomerStore, CustomerStoreAdmin)
admin.site.register(models.CustomerStoreAddress, CustomerStoreAddressAdmin)
admin.site.register(models.CustomerStoreContact)
admin.site.register(models.CustomerStoreImage)
admin.site.register(models.CustomerStoreGrade)

from django.contrib import admin

from .models.models import HumanName, Address

# Register your models here.
admin.site.register(HumanName)
admin.site.register(Address)
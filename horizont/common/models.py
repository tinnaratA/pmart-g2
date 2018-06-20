from django.db import models
from django.utils.translation import pgettext_lazy

class Address(models.Model):
    line = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True, default='Thailand')
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'common'
        db_table = 'common_address'
        permissions = (
            ('view_address', pgettext_lazy('Permission description', 'Can view addresses')),
        )
        ordering = ('country', 'zipcode',)

    def __str__(self):
        return self.zipcode if self.zipcode else self.get_full_address()

    def get_full_address(self):
        data = [self.line, self.city, self.district, self.province, self.country, self.zipcode]
        return " ".join([d for d in data if d])

    def get_geo_location(self, returntype=dict):
        if returntype == dict:
            return {"latitude": self.latitude, "longitude": self.longitude}
        elif returntype == tuple:
            return self.latitude, self.longitude
        else:
            return [self.latitude, self.longitude]


class Contact(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        app_label = 'common'
        db_table = 'common_contact'
        permissions = (
            ('view_contact', pgettext_lazy('Permission description', 'Can view contacts')),
        )
        
    def __str__(self):
        return f"<{self.__class__.__name__}: {self.type}-{self.value}>"

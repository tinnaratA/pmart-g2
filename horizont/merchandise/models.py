from django.db import models
from django.utils.translation import pgettext_lazy


class ItemCategory(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_item_category'
        permissions = (
            ('view_item_category', pgettext_lazy('Permission description', 'Can view item categories')),
        )
        ordering = ('code',)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.code}>"

    def get_children(self):
        return self._children.all()


class ItemSubCategory(models.Model):
    # Attribute
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    # Relations
    category = models.ForeignKey(ItemCategory, related_name="_children", on_delete=models.CASCADE)

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_item_sub_category'
        permissions = (
            ('view_item_sub_category', pgettext_lazy('Permission description', 'Can view item sub-categories')),
        )
        ordering = ('code',)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.code}>"

    def get_ancestor(self):
        return self.category

class ItemMaster(models.Model):
    # Attribute
    code = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=4096, null=True, blank=True)

    # Relations
    category = models.ForeignKey(
        ItemSubCategory, 
        related_name="_item_masters", 
        on_delete=models.SET_NULL, 
        null=True
    )

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_item_master'
        permissions = (
            ('view_item_master', pgettext_lazy('Permission description', 'Can view master items')),
        )
        ordering = ('code',)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.code}>"
    

class ItemUnitOfConversion(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    factor = models.FloatField(default=None, null=True)

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_unit_of_conversion'
        permissions = (
            ('view_unit_of_conversion', pgettext_lazy('Permission description', 'Can view unit of conversions')),
        )
        ordering = ('code',)

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.factor} {self.name}>"

class ItemUnitOfMeasurement(models.Model):
    item_master = models.ForeignKey(ItemMaster, related_name="uoms", on_delete=models.CASCADE)
    package_code = models.CharField(max_length=50)
    package_name = models.CharField(max_length=50)
    unit_conversions = models.ManyToManyField(ItemUnitOfConversion, related_name="uoms")

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_unit_of_measurement'
        permissions = (
            ('view_unit_of_measurement', pgettext_lazy('Permission description', 'Can view unit of measurements')),
        )
        ordering = ('package_code',)


    def __str__(self):
        return f"<{self.__class__.__name__}: {self.package_name} of item code: {self.item_master.code}>"



    
    
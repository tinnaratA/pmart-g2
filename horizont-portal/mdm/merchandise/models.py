import datetime, uuid
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Max, Q
from django.utils.translation import pgettext_lazy
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from versatileimagefield.fields import PPOIField, VersatileImageField


class MerchandiseCategory(MPTTModel):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_category'
        permissions = (
            ('view_merchandise_category', pgettext_lazy('Permission description', 'Can view merchandise categories')),
        )
        ordering = ('slug',)

    def __str__(self, result=''):
        return "-".join([cate.slug for cate in self.get_ancestors()] + [self.slug])


class MerchandiseQuerySet(models.QuerySet):
    def available_merchandises(self):
        today = datetime.date.today()
        return self.filter(
            Q(available_on__lte=today) | Q(available_on__isnull=True),
            Q(is_published=True))


class MerchandiseMasterItem(models.Model):
    code = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.TextField()
    category = models.ForeignKey(MerchandiseCategory, related_name='merchandises_of_category', on_delete=models.CASCADE)
    price = models.FloatField(default=1.00)
    available_on = models.DateField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_featured = models.BooleanField(default=False)

    objects = MerchandiseQuerySet.as_manager()

    class Meta:
        app_label = 'merchandise'
        db_table = 'merchandise_master_item'
        permissions = (
            ('view_merchandise',
             pgettext_lazy('Permission description', 'Can view merchandises')),
            ('edit_merchandise',
             pgettext_lazy('Permission description', 'Can edit merchandises')),
            ('view_properties',
             pgettext_lazy(
                 'Permission description', 'Can view merchandise properties')),
            ('edit_properties',
             pgettext_lazy(
                 'Permission description', 'Can edit merchandise properties')))

    def __iter__(self):
        if not hasattr(self, '__variants'):
            setattr(self, '__variants', self.variants.all())
        return iter(getattr(self, '__variants'))

    def __repr__(self):
        class_ = type(self)
        return '<%s.%s(pk=%r, name=%r)>' % (
            class_.__module__, class_.__name__, self.pk, self.name)

    def __str__(self):
        return self.name


# class MerchandiseVariant(models.Model):
#     sku = models.CharField(max_length=40, unique=True, default=uuid.uuid1)
#     name = models.CharField(max_length=100, blank=True)
#     price_override = models.FloatField(default=None, null=True)
#     merchandise = models.ForeignKey(
#         MerchandiseMasterItem, related_name='variants', on_delete=models.CASCADE)
#     images = models.ManyToManyField('MerchandiseImage', through='VariantImage')

#     class Meta:
#         app_label = 'merchandise'
#         db_table = 'merchandise_variant'

#     def __str__(self):
#         return self.name


# class StockLocation(models.Model):
#     name = models.CharField(max_length=100)

#     class Meta:
#         permissions = (
#             ('view_stock_location',
#              pgettext_lazy('Permission description',
#                            'Can view stock location')),
#             ('edit_stock_location',
#              pgettext_lazy('Permission description',
#                            'Can edit stock location')))

#     def __str__(self):
#         return self.name


# class Stock(models.Model):
#     variant = models.ForeignKey(
#         MerchandiseVariant, related_name='stock', on_delete=models.CASCADE)
#     location = models.ForeignKey(
#         StockLocation, null=True, on_delete=models.CASCADE)
#     quantity = models.IntegerField(
#         validators=[MinValueValidator(0)], default=Decimal(1))
#     quantity_allocated = models.IntegerField(
#         validators=[MinValueValidator(0)], default=Decimal(0))
#     cost_price = models.FloatField(default=None, null=True)

#     class Meta:
#         app_label = 'merchandise'
#         db_table = 'merchandise_stock'
#         unique_together = ('variant', 'location')

#     def __str__(self):
#         return '%s - %s' % (self.variant.name, self.location)

#     @property
#     def quantity_available(self):
#         return max(self.quantity - self.quantity_allocated, 0)


# class MerchandiseImage(models.Model):
#     merchandise = models.ForeignKey(
#         MerchandiseMasterItem, related_name='images', on_delete=models.CASCADE)
#     image = VersatileImageField(
#         upload_to='merchandises', ppoi_field='ppoi', blank=False)
#     ppoi = PPOIField()
#     alt = models.CharField(max_length=128, blank=True)
#     order = models.PositiveIntegerField(editable=False)

#     class Meta:
#         ordering = ('order', )
#         app_label = 'merchandise'
#         db_table = 'merchandise_image'

#     def get_ordering_queryset(self):
#         return self.merchandise.images.all()

#     def save(self, *args, **kwargs):
#         if self.order is None:
#             qs = self.get_ordering_queryset()
#             existing_max = qs.aggregate(Max('order'))
#             existing_max = existing_max.get('order__max')
#             self.order = 0 if existing_max is None else existing_max + 1
#         super().save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         qs = self.get_ordering_queryset()
#         qs.filter(order__gt=self.order).update(order=F('order') - 1)
#         super().delete(*args, **kwargs)


# class VariantImage(models.Model):
#     variant = models.ForeignKey(
#         'MerchandiseVariant', related_name='variant_images',
#         on_delete=models.CASCADE)
#     image = models.ForeignKey(
#         MerchandiseImage, related_name='variant_images', on_delete=models.CASCADE)


class Collection(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=128)
    merchandises = models.ManyToManyField(
        MerchandiseMasterItem, blank=True, related_name='collections')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


class UnitOfConversion(models.Model):
    name = models.CharField(max_length=50)
    factor = models.FloatField(default=None, null=True)

    class Meta:
        app_label = 'merchandise'
        db_table = 'unit_of_conversion'

    def __str__(self):
        return f"{self.factor} {self.name}"


class UnitOfMeasurement(models.Model):
    merchandise = models.ForeignKey(MerchandiseMasterItem, related_name="uoms", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    unit_conversions = models.ManyToManyField(UnitOfConversion, related_name="uoms")

    class Meta:
        app_label = 'merchandise'
        db_table = 'unit_of_measurement'

    def __str__(self):
        return f"{self.name} - {self.merchandise.name}"

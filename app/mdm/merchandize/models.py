from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel
from mptt.managers import TreeManager

from django.utils.text import slugify
from django.utils.translation import pgettext_lazy


class Category(MPTTModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=50)
    slug = models.SlugField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children',
        on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        app_label = 'merchandize'
        db_table = 'mdm_merchandize_category'
        default_permissions = ('add_mdm_merchandize', 'change_mdm_merchandize', 'delete_mdm_merchandize')
        permissions = (
            ('view_mdm_merchandize_category',
             pgettext_lazy('Permission description', 'Can view mdm merchandize categories')),
            ('edit_mdm_merchandize_category',
             pgettext_lazy('Permission description', 'Can edit mdm merchandize categories')))

    def __str__(self):
        return self.name

    def get_absolute_url(self, ancestors=None):
        return reverse('product:category',
                       kwargs={'path': self.get_full_path(ancestors),
                               'category_id': self.id})

    def get_full_path(self, ancestors=None):
        if not self.parent_id:
            return self.slug
        if not ancestors:
            ancestors = self.get_ancestors()
        nodes = [node for node in ancestors] + [self]
        return '/'.join([node.slug for node in nodes])


class Merchandize(models.Model):
    # Common Fields
    name = models.CharField(max_length=512)
    barcode = models.CharField(max_length=128)
    itemcode = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    # Related Fields
    category = models.ForeignKey(Category, related_name='mdm_merchandizes', on_delete=models.CASCADE)
    # Timestamp Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'merchandize'
        db_table = 'mdm_merchandize'
        unique_together = ('barcode', 'itemcode')
        default_permissions = ('add_mdm_merchandize', 'change_mdm_merchandize', 'delete_mdm_merchandize')
        permissions = (
            ('view_mdm_merchandize',
             pgettext_lazy('Permission description', 'Can view mdm merchandizes')),
            ('edit_mdm_merchandize',
             pgettext_lazy('Permission description', 'Can edit mdm merchandizes')),
            ('view_properties_mdm_merchandize',
             pgettext_lazy(
                 'Permission description', 'Can view mdm merchandizes properties')),
            ('edit_properties_mdm merchandizes',
             pgettext_lazy(
                 'Permission description', 'Can edit mdm merchandizes properties')))


class Attribute(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    merchandize = models.ForeignKey(Merchandize, related_name='attributes', on_delete=models.CASCADE)

    class Meta:
        app_label = 'merchandize'
        db_table = 'mdm_merchandize_attribute'
        ordering = ('slug',)

    def __str__(self):
        return self.name

    def get_formfield_name(self):
        return slugify('attribute-%s' % self.slug, allow_unicode=True)

    def has_values(self):
        return self.choices.exists()


class AttributeChoiceValue(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    value = models.CharField(max_length=512)
    attribute = models.ForeignKey(Attribute, related_name='choices', on_delete=models.CASCADE)

    class Meta:
        app_label = 'merchandize'
        db_table = 'mdm_merchandize_attribute_choice_value'
        unique_together = ('name', 'attribute')

    def __str__(self):
        return self.name

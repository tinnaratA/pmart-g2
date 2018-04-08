from django.db import models
from saleor.account import models as account_models
from saleor.product import models as product_models

class ProductFavorite(models.Model):
    favorite_name = models.CharField(max_length=512)
    variants = models.ManyToManyField(product_models.ProductVariant, related_name='products')
    customer = models.ForeignKey(account_models.User, related_name='favorites', on_delete=models.CASCADE)

    class Meta:
        app_label = 'product_extension'
        db_table = 'product_favorite'

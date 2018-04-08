from rest_framework import serializers
from saleor.product import models as product_models

class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        models = product_models.Category
        fields = (
            'customer',
            'favorite_name',
            'variants'
        )
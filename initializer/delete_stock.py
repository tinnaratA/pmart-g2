import os
import sys
import django
base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if base not in sys.path:
    sys.path.append(base)
    sys.path.append(os.path.join(base, ""))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")
django.setup()

from saleor.product import models as product_models

product_models.Product.objects.all().delete()
product_models.Category.objects.all().delete()
product_models.ProductAttribute.objects.all().delete()
product_models.AttributeChoiceValue.objects.all().delete()
product_models.ProductType.objects.all().delete()
product_models.ProductImage.objects.all().delete()
product_models.ProductVariant.objects.all().delete()

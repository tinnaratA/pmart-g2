import os
import sys
import django


base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if base not in sys.path:
    sys.path.append(base)
    sys.path.append(os.path.join(base, ""))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")
django.setup()

from saleor.product.initializer.initial_category_master import main as master_category_initialize
from saleor.product.initializer.initial_product_attribute_master import main as master_attribute_initialize
from saleor.product.initializer.initial_product_type_master import main as master_product_type_initialize
from saleor.product.initializer.initial_product_master import main as master_product_initialize

def main(filepath):
    master_category_initialize(filepath)
    master_attribute_initialize(filepath)
    master_product_type_initialize(filepath)
    master_product_initialize(filepath)

if __name__ == "__main__":
    main(sys.argv[1])

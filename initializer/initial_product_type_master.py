import os
import sys
import django

base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if base not in sys.path:
    sys.path.append(base)
    sys.path.append(os.path.join(base, ""))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")
django.setup()

from django.utils.encoding import smart_text
from django.utils.text import slugify
from text_unidecode import unidecode

from saleor.product.initializer import utils
from saleor.product.models import ProductType, ProductAttribute

PATH_TO_SOURCE = os.path.join(base, 'saleor', 'product', 'initializer', 'source')


def create_master_product_type_objects(data):
    sys.stdout.write("\rCreating product type....0%       ")
    total = len(data)
    i = 0
    product_types = list()
    for item in data:
        temp = dict()
        temp['name'] = item['subcatery_name']
        temp['has_variants'] = True
        temp['is_shipping_required'] = True
        if temp not in product_types:
            instance, created = ProductType.objects.get_or_create(**temp)
            attribute = ProductAttribute.objects.get(slug=slugify(smart_text(unidecode("ขนาดบรรจุ"))))
            instance.variant_attributes.add(attribute)
            product_types.append(temp)
        percent = (i / total) * 100
        sys.stdout.write(f"\rCreating product type....{percent:.2f}%       ")
        i += 1
    sys.stdout.write(f"\rCreating product type....Done       \n")
    return product_types


def main(filepath):
    rawdata = utils.read_excel(filepath)
    rawdata = rawdata['_003ud']
    master_product_types = create_master_product_type_objects(rawdata)
    utils.write_jsonfile(os.path.join(PATH_TO_SOURCE, 'type_master.json'), master_product_types)


if __name__ == "__main__":
    main(sys.argv[1])

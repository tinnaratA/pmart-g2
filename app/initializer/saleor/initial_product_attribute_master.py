import os
import sys
import django

from datetime import date

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

from saleor.product.models import ProductAttribute, AttributeChoiceValue, ProductType

PATH_TO_SOURCE = os.path.join(base, 'saleor', 'product', 'initializer', 'source')


# def create_master_product_attribute_object(rawdata):
#     sys.stdout.write("\n\rCreating attribute....0%       ")
#     total = len(rawdata)
#     i = 0
#
#     checkdup = list()
#     unit_of_items = list()
#     for item in rawdata:
#         item['unit_of_items'] = item['unit_of_items'].replace("x", "*").replace('(', '').replace(")", "").split("*")[0]
#         if item['unit_of_items'] not in checkdup:
#             unit_of_items.append({"name": item['unit_of_items'], "slug": slugify(smart_text(unidecode(item['unit_of_items'])))})
#             checkdup.append(item['unit_of_items'])
#             temp = {"name": item['unit_of_items'], "slug": slugify(smart_text(unidecode(item['unit_of_items'])))}
#             attribute = ProductAttribute.objects.get_or_create(**temp)
#             percent = (i / total) * 100
#             sys.stdout.write(f"\rCreating attribute....{percent:.2f}%       ")
#             i += 1
#     sys.stdout.write(f"\rCreating attribute....Done       \n")
#     return unit_of_items


def create_attribute_choice(rawdata):
    sys.stdout.write("\rCreating attribute choice....0%       ")
    total = len(rawdata)
    i = 0
    for item in rawdata:
        attr_name = item['unit_of_items'].replace("x", "*").replace('(', '').replace(")", "").split("*")[0]
        name = f"{attr_name}*{int(item['unit_fact'])}"
        attr = ProductAttribute.objects.get_or_create(name="ขนาดบรรจุ", slug=slugify(smart_text((unidecode("ขนาดบรรจุ")))))[0]
        temp = dict()
        temp['attribute'] = attr
        temp['name'] = name
        temp['slug'] = slugify(smart_text(unidecode(name)))
        AttributeChoiceValue.objects.get_or_create(**temp)
        percent = (i / total) * 100
        sys.stdout.write(f"\rCreating attribute choice....{percent:.2f}%       ")
        i += 1
    sys.stdout.write(f"\rCreating attribute choice....Done       \n")


def main(filepath):
    rawdata = utils.read_excel(filepath)
    rawdata = rawdata['_003ud']
    create_attribute_choice(rawdata)

if __name__ == "__main__":
    main(sys.argv[1])

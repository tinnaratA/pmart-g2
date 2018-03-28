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

from saleor.product.models import Product, ProductType, Category, ProductVariant, AttributeChoiceValue
from saleor.product.models import StockLocation, Stock

PATH_TO_SOURCE = os.path.join(base, 'saleor', 'product', 'initializer', 'source')


def create_master_product_object(data):
    sys.stdout.write("\rCreating product object....0%       ")
    total = len(data)
    i = 0
    for d in data:
        temp = dict()
        temp['product_type'] = ProductType.objects.filter(name=d['subcatery_name'])[0]
        temp['name'] = d['desc_th']
        temp['description'] = d['item_code']
        temp['category'] = Category.objects.filter(name=d['subcatery_name'])[0]
        temp['price'] = float(1.00)
        temp['available_on'] = date.today()
        temp['is_published'] = False
        temp['is_featured'] = True
        Product.objects.get_or_create(**temp)
        percent = (i / total) * 100
        sys.stdout.write(f"\rCreating product object....{percent:.2f}%       ")
        i += 1
    sys.stdout.write(f"\rCreating product object....Done       \n")


def create_product_variant_object(data):
    sys.stdout.write("\rCreating product variant....0%       ")
    total = len(data)
    i = 0
    for d in data:
        try:
            temp = dict()
            temp['sku'] = f"{d['item_code']}-{d['barcode']}"
            temp['name'] = f"{d['unit_of_items'].split('*')[0]}*{int(d['unit_fact'])}"
            temp['price_override'] = d['normal_sp']
            temp['product'] = Product.objects.get(description=d['item_code'])
            choice = AttributeChoiceValue.objects.get(slug=slugify(smart_text(unidecode(temp['name']))))
            attribute_id = choice.attribute_id
            temp['attributes'] = {f"{attribute_id}": f"{choice.id}"}
            variant = ProductVariant.objects.get_or_create(**temp)[0]
            create_product_stock(variant)
        except:
            continue
        finally:
            percent = (i / total) * 100
            sys.stdout.write(f"\rCreating product variant....{percent:.2f}%       ")
            i += 1
    sys.stdout.write(f"\rCreating product variant....Done       \n")


def create_product_stock(variant):
    temp = dict()
    temp['variant'] = variant
    temp['location'] = StockLocation.objects.get_or_create(name="กรุงเทพ")[0]
    temp['quantity'] = 2000
    temp['quantity_allocated'] = 0
    temp['cost_price'] = variant.product.price - ((variant.product.price * 25) / 100)
    Stock.objects.get_or_create(**temp)


def enable_product():
    all_product = Product.objects.all()
    sys.stdout.write("\rEnabling product....0%       ")
    total = all_product.count()
    i = 0
    for product in all_product:
        product.is_published = True
        product.save()
        percent = (i / total) * 100
        sys.stdout.write(f"\rEnabling product....{percent:.2f}%       ")
        i += 1
    sys.stdout.write(f"\rEnabling product....Done       \n")


def main(filepath):
    rawdata = utils.read_excel(filepath)
    rawdata = rawdata['_003ud']
    create_master_product_object(rawdata)
    create_product_variant_object(rawdata)
    enable_product()

if __name__ == "__main__":
    main(sys.argv[1])

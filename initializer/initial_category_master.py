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

from saleor.product.models import Category

PATH_TO_SOURCE = os.path.join(base, 'saleor', 'product', 'initializer', 'source')


def get_or_create_parent_category_object(parent_id, data):
    for d in data:
        if d['id'] == parent_id:
            d['slug'] = slugify(smart_text(unidecode(d['name'])))
            d.pop('level')
            d['description'] = d.pop('sequence')
            instance, created = Category.objects.get_or_create(**d)
            return instance


def get_parent_category_object(parent_id, data):
    try:
        return Category.objects.get(id=parent_id)
    except Category.DoesNotExist:
        return get_or_create_parent_category_object(parent_id, data)


def create_master_category_object(data):
    sys.stdout.write("\rCreating master category object.....0%   ")
    total = len(data)
    i = 0
    for d in data:
        d['slug'] = slugify(smart_text(unidecode(d['name'])))
        d.pop('level')
        parent_id = d.pop('parent_id')
        if parent_id:
            d['parent'] = get_parent_category_object(parent_id, data)
        else:
            d['parent'] = None
        d['description'] = d.pop('sequence')
        Category.objects.get_or_create(**d)
        percent = (i / total) * 100
        sys.stdout.write(f"\rCreating master category object.....{percent:.2f}%")
        i += 1
    sys.stdout.write(f"\rCreating master category object.....Done     \n")


def classify_data(raw_data):
    category_code_list = set(
        [
            (
                item['category_code'] + '-' + item['subcategero_code'].split('-')[-1], item['division'],
                item['department'], item['category_name'], item['subcatery_name']
            ) for item in raw_data
        ]
    )
    key_list = ['category_code', 'division', 'department', 'category_name', 'subcatery_name']
    result = [{k: v for k, v in zip(key_list, cate)} for cate in category_code_list]
    result = sorted(result, key=lambda x: x['category_code'])
    cate_name_map_level = ['division', 'department', 'category_name', 'subcatery_name']
    seq_id = 1
    master_categories = list()
    sys.stdout.write("\rClassifying the category data.....0%   ")
    total = len(result)
    i = 0
    for cate in result:
        codes = [str(c) for c in cate['category_code'].split('-')]
        for level in range(0, 4):
            temp = dict()
            temp['id'] = seq_id
            temp['description'] = ""
            temp['name'] = cate[cate_name_map_level[level]]
            temp['slug'] = cate[cate_name_map_level[level]].lower().replace(' ', '_')
            temp['level'] = level + 1
            temp['sequence'] = "-".join(codes[0:level + 1]) if level != 0 else codes[0]
            seq_id += 1
            master_categories.append(temp)
        percent = (i / total) * 100
        sys.stdout.write(f"\rClassifying the category data.....{percent:.2f}%")
        i += 1
    sys.stdout.write(f"\rClassifying the category data.....Done     \n")
    return master_categories


def get_parent_category(cates, parent_name):
    for cate in cates:
        if parent_name == cate['sequence']:
            return cate


def create_master_category(classified_data):
    sys.stdout.write("\rCreating master category dict.....0%   ")
    total = len(classified_data)
    i = 0

    dup = list()
    result = list()
    for cate in classified_data:
        catecode = cate['sequence'].split('-')
        catecode_length = len(catecode)
        parent = dict()
        if catecode_length <= 1:
            parent['parent_id'] = ''
        else:
            parent['parent_id'] = get_parent_category(classified_data, "-".join(catecode[0:catecode_length - 1])).get('id')
        cate.update(parent)
        cate_dup = dict(cate)
        cate_dup.pop('id')
        if cate_dup not in dup:
            result.append(cate)
            dup.append(cate_dup)
        percent = (i / total) * 100
        sys.stdout.write(f"\rCreating master category dict.....{percent:.2f}%")
        i += 1
    sys.stdout.write(f"\rCreating master category dict.....Done     \n")
    return result


def main(filepath):
    rawdata = utils.read_excel(filepath)
    rawdata = rawdata['_003ud']
    classified_data = classify_data(rawdata)
    master_categories = create_master_category(classified_data)
    utils.write_jsonfile(os.path.join(PATH_TO_SOURCE, 'category_master.json'), master_categories)
    create_master_category_object(master_categories)

if __name__ == "__main__":
    main(sys.argv[1])

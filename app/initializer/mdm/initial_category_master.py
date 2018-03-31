import os
import sys
import django

base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base not in sys.path:
    sys.path.append(base)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")
django.setup()

from django.utils.encoding import smart_text
from django.utils.text import slugify
from text_unidecode import unidecode

from initializer import utils
from mdm.merchandize import models as mdm_mcdse_models

PATH_TO_SOURCE = os.path.join(base, 'mdm', 'source')

def str_to_slug(string):
    return slugify(smart_text(unidecode(string)))

def update_or_create_division(data):
    instance, created = mdm_mcdse_models.Category.objects.update_or_create(
        name=data['division_name'],
        slug=str_to_slug(data['division_name']),
        code=data['division']
    )
    return instance

def main(filepath, sheet_name):
    rawdata = utils.read_excel(filepath)
    rawdata = rawdata[sheet_name]
    # master_categories = create_master_category(rawdata)
    # utils.write_jsonfile(os.path.join(PATH_TO_SOURCE, 'category_master.json'), master_categories)
    # create_master_category_object(master_categories)


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except IndexError as e:
        raise e

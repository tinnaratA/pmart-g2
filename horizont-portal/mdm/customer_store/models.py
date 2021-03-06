import uuid, os
from text_unidecode import unidecode

from django.conf import settings
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.encoding import smart_text
from django.utils.text import slugify

from mptt.managers import TreeManager
from mptt.models import MPTTModel

from common.models.models import Address, HumanName
from common.models.abstracts import AbstractContact, TimeStampMixin
from product.models import ProductItem

class CustomerStoreAddress(Address, TimeStampMixin):
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_address'
        permissions = (
            ('view_customerstoreaddress', pgettext_lazy('Permission description', 'Can view customer store addresses')),
        )

    def to_dict(self):
        return {
            "line1": self.line1,
            "line2": self.line2,
            "district": self.district,
            "city": self.city,
            "province": self.province,
            "postcode": self.postcode,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @property
    def full_address(self):
        return self.get_full_address()

    def get_full_address(self):
        return " ".join([s for s in [v for k,v in self.to_dict().items()][0:-2] if s and s != "-"])

class CustomerStoreType(MPTTModel, TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    code = models.SlugField(max_length=256, null=False, blank=False)
    name = models.TextField(null=False, blank=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_type'
        permissions = (
            ('view_customerstoretype', pgettext_lazy('Permission description', 'Can view customer store types')),
        )

    def __str__(self):
        return f"{self.code} - {self.name}"

    def to_dict(self):
        if self.parent is not None:
            return {"code": self.code, "name": self.name, "parent": self.parent.to_dict()}
        else:
            return {"code": self.code, "name": self.name, "parent": self.parent}

    def get_detail(self, parent=False):
        if not parent:
            return {"code": self.code, "name": self.name}
        else:
            return {"code": self.code, "name": self.name, "parent": self.parent.to_dict()}


class CustomerStoreGrade(models.Model):
    GRADE_A = 'A'
    GRADE_B = 'B'
    GRADE_C = 'C'
    GRADE_D = 'D'
    GRADES = (
        (GRADE_A, 'Grade A'),
        (GRADE_B, 'Grade B'),
        (GRADE_C, 'Grade C'),
        (GRADE_D, 'Grade D'),
    )

    higher_grade = models.ForeignKey(
        to='self', related_name="higher", blank=True,
        on_delete=models.SET_DEFAULT, default=None, null=True
    )
    grade = models.CharField(max_length=10, choices=GRADES, default=GRADE_D)
    lower_grade = models.ForeignKey(
        to='self', related_name="lower", blank=True,
        on_delete=models.SET_DEFAULT, default=None, null=True
    )

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_grade'

    def __str__(self):
        return self.grade


class CustomerStore(TimeStampMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    store_name = models.CharField(max_length=512, blank=False, null=True)
    owners = models.ManyToManyField(HumanName, related_name='customer_stores')
    description = models.TextField(null=True, blank=True)
    type = models.ForeignKey(CustomerStoreType, related_name='customer_stores', on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerStoreAddress, related_name='customer_store', on_delete=models.CASCADE)
    grade = models.ForeignKey(CustomerStoreGrade, default=None, on_delete=models.SET_DEFAULT, null=True)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store'
        permissions = (
            ('view_customerstore', pgettext_lazy('Permission description', 'Can view customer stores')),
        )

    def __str__(self):
        return self.store_name

    def get_owners(self):
        return [
            {"title": name.title, "first": name.first, "middle": name.middle, "last": name.last}
            for name in self.owners.all()
        ]

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.store_name,
            "owners": self.get_owners(),
            "description": self.description,
            "type": self.type.to_dict(),
            "address": self.address.to_dict(),
            "grade": self.grade.grade,
            "contacts": [contact.to_dict() for contact in self.customer_store_contacts.all()]
        }


class CustomerStoreContact(AbstractContact, TimeStampMixin):
    store = models.ForeignKey(CustomerStore, related_name="customer_store_contacts", on_delete=models.CASCADE)
    owner = models.ForeignKey(HumanName, related_name='customer_store_contacts', on_delete=models.CASCADE)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_contact'
        permissions = (
            ('view_customerstorecontact', pgettext_lazy('Permission description', 'Can view customer store contacts')),
        )

    def __str__(self):
        return self.value

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "contact_owner": self.owner.to_dict()
        }


class CustomerStoreImage(TimeStampMixin):
    customer_store = models.ForeignKey(CustomerStore, related_name='customer_store_images', null=False, on_delete=models.CASCADE)
    abspath = models.CharField(max_length=256)

    class Meta:
        app_label = 'customer_store'
        db_table = 'customer_store_image'
        permissions = (
            ('view_customerstoreimage', pgettext_lazy('Permission description', 'Can view customer stores images')),
        )

    def __str__(self):
        return f"Image of {self.customer_store.store_name} store"

    @property
    def url(self):
        return os.path.join(settings.MEDIA_URL, "/".join(self.abspath.split("/")[-2:]))

    @property
    def binary_image(self):
        fp = open(self.abspath, mode="rb")
        content = fp.read()
        fp.close()
        return content

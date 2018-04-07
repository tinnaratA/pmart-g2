import os
import sys
import django

base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base not in sys.path:
    sys.path.append(base)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saleor.settings")
django.setup()

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, Group

from utils import file_utils


def get_permissions(keyword, app_label, models=[]):
    django_keys = {
        "read": "view",
        "write": "add",
        "edit": "change",
        "delete": "delete"
    }

    if models:
        return Permission.objects.filter(
            content_type__app_label__iexact=app_label,
            content_type__model__in=models,
            codename__icontains=django_keys[keyword]
        )
    return Permission.objects.filter(
        content_type__app_label__iexact=app_label,
        codename__icontains=django_keys[keyword]
    )


def setup_group(roles):
    groups = list()
    for r in roles:
        try:
            group = Group.objects.get(name=r)
        except Group.DoesNotExist as e:
            group, created = Group.objects.update_or_create(name=r)
        finally:
            groups.append(group)
    return Group.objects.all()


def setup_group_permission_domain(role, permissions, group):
    for permdict in permissions:
        app_label = permdict['app_label']
        models = permdict.get('models')
        for act in permdict['actions']:
            permissions = get_permissions(act, app_label, models)
            [group.permissions.add(perm) for perm in permissions]


def setup_group_permission(dictsettings, groups):
    for role, perms in dictsettings.items():
        domain_permissions = perms['domains']
        partial_permissions = perms['partial']
        group = groups.get(name=role)

        if domain_permissions:
            setup_group_permission_domain(role, domain_permissions, group)

        if partial_permissions:
            pass


def main(dictsettings):
    groups = setup_group(dictsettings.keys())
    setup_group_permission(dictsettings, groups)


if __name__ == "__main__":
    try:
        filepath = sys.argv[1]
    except IndexError as e:
        filepath = settings.DEFAULT_USER_PERMISSION_SETTING_FILE

    dictsettings = file_utils.read_json(filepath)
    main(dictsettings)

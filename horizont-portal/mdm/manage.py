#!/usr/bin/env python
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
MODULE = 'mdm'
from settings import settings


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mdm.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    argc = len(sys.argv)
    if sys.argv[1] == 'runserver' and argc == 2:
        sys.argv.append(f"0.0.0.0:{settings['module'][MODULE]['port']}")
    execute_from_command_line(sys.argv)

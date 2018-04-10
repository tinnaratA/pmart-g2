#!/usr/bin/env python
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)
MODULE = 'content_management'
from settings import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_management.settings.dev")

    from django.core.management import execute_from_command_line

    argc = len(sys.argv)
    if sys.argv[1] == 'runserver' and argc == 2:
        sys.argv.append(f"0.0.0.0:{settings['module'][MODULE]['port']}")

    execute_from_command_line(sys.argv)

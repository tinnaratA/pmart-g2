from .base import *

DEBUG = False
SECRET_KEY = 'lwympefmj+-r_io)%0%g3v#3g3_*^-okia9@#9pk5x(1-g$9uj'

INTERNAL_IPS = [
    '127.0.0.1'
]

ALLOWED_HOSTS = [
    '127.0.0.1'
]

try:
    from .local import *
except ImportError:
    pass

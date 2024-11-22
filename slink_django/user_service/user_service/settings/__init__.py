import os

from . import base

DEBUG = os.environ.get('DEBUG', True)

if DEBUG:
    from .dev import *
else:
    from .prod import *
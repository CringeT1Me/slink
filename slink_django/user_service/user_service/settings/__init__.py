import os

ENV = os.environ.get('ENV', '')
print(f'Mode: {ENV.upper()}')
if ENV == '.test':
    from .test import *
elif ENV == '.prod':
    from .prod import *
else:
    from .dev import *
from .base import *

SECRET_KEY = ')h5te@q0c2d9y-z29&1f7#k&bf(-bl)3(a*s8)4gs)=q-o@pvl'

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reptiles',
        'USER': 'user',
        'PASSWORD': 'BT6,NKsJ+eqm',
        'HOST': 'db',
        'PORT': '3306',
    }
}
# Celeryの設定
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/1')
CELERY_RESULT_BACKEND = 'django-db'
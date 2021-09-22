from .base import *
import os

SECRET_KEY = ')h5te@q0c2d9y-z29&1f7#k&bf(-bl)3(a*s8)4gs)=q-o@pvl'

DEBUG = False

ALLOWED_HOSTS = ["reptiles.azurewebsites.net", ".reptiles.azurewebsites.net"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reptiles',
        'USER': 'user@reptiles',
        'PASSWORD': 'BT6,NKsJ+eqm',
        'HOST': 'reptiles.mysql.database.azure.com',
        'PORT': '3306',
    }
}
# Celeryの設定
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://:NeEdMJkmvKg1LF3+5XXDONdIerlWP6iW6A0d+01anqU=@reptiles.redis.cache.windows.net:6380/0')
CELERY_RESULT_BACKEND = 'django-db'
import os

from .base import *

ALLOWED_HOSTS = []
DEBUG = True

#  협업
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("D"),
#         "USER": os.environ.get("DB_USER"),
#         "PASSWORD": os.environ.get("DB_PASSWORD"),
#         "HOST": os.environ.get("DB_HOST"),
#         "PORT": os.environ.get("DB_PORT"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_gagyebu",
        "USER": "mac",
        "PASSWORD": "1234",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

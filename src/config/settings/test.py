import os
os.environ.setdefault("DJANGO_SECRET_KEY", "test-only-secret")
from .base import *  # noqa: F403
DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

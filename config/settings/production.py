import os

from .general import *  # noqa

DEBUG = False

# set string like "localhost,example.com"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

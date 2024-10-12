from datetime import UTC, datetime, timedelta
from typing import Any

from django.conf import settings
from django.contrib.auth.hashers import make_password
from jose import jwt
from passlib.handlers.django import django_pbkdf2_sha256

"""
JWT
"""


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(tz=UTC) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_access_token(token: str) -> Any:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


"""
password hashing
"""


def hash_password(plain_password: str) -> str:
    return make_password(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return django_pbkdf2_sha256.verify(plain_password, hashed_password)

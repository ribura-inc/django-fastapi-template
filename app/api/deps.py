"""Dependencies for the API routes."""

from typing import Annotated

from django.conf import settings
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError

from app.models import User
from config.exceptions import ForbiddenException, NotFoundException
from config.security import verify_access_token

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/login/access-token/",
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(token: TokenDep) -> User:
    try:
        payload = verify_access_token(token)
    except (JWTError, ValidationError):
        raise ForbiddenException(
            detail="Could not validate credentials",
        ) from None
    user = User.objects.filter(uid=payload.get("sub")).first()
    if not user:
        raise NotFoundException(detail="User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

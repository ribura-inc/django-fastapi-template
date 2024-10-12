from datetime import timedelta
from typing import Annotated

from django.conf import settings
from django.db.models import Q
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models import User
from app.schemas.token import Token
from config.exceptions import UnauthorizedException
from config.security import create_access_token, verify_password

router = APIRouter()


@router.post(
    "/access-token/",
    description="ユーザー名またはメールアドレスでログインしてアクセストークンを取得する",
    status_code=status.HTTP_200_OK,
)
def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = User.objects.filter(Q(username=form_data.username) | Q(email=form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise UnauthorizedException(detail="Incorrect username, email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=create_access_token(user.uid, expires_delta=access_token_expires))

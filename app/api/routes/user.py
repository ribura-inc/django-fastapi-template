from fastapi import APIRouter, status

from app.api.deps import CurrentUser
from app.models import User
from app.schemas.user import UserRead

router = APIRouter()


#########################################
# GET
#########################################


@router.get("/", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_current_user(current_user: CurrentUser) -> User:
    return current_user

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, NoneStr
from services.user_service import UserParcerService, get_user_parser_service


class UserInfo(BaseModel):
    twitter_id: int
    name: str
    username: str
    following_count: int | None = None
    followers_count: int | None = None
    description: NoneStr


router = APIRouter()


@router.get("/user/{username}", response_model=UserInfo)
async def user_info(
    username: str, user_service: UserParcerService = Depends(get_user_parser_service)
) -> UserInfo:
    user = await user_service.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"user with {username} does not exit in Twitter \
                or please check username.",
        )

    return user

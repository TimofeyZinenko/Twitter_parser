from fastapi import APIRouter
from pydantic import BaseModel


class UserInfo(BaseModel):
    twitter_id: int
    name: str
    username: str
    following_count: int
    followers_count: int
    description: str


router = APIRouter()


@router.get("/user/{username}", response_model=UserInfo)
async def user_info(username: str) -> UserInfo:

    result = UserInfo(
        twitter_id=24785647,
        name="Elon Musk",
        username="elonmusk",
        following_count=166,
        followers_count=124_400_000,
        description="Elon Musk & SpaceX & Tesla",
    )
    return result

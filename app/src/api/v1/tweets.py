from fastapi import APIRouter
from pydantic import BaseModel, Json


class TweetsInfo(BaseModel):
    tweet: Json = {}


router = APIRouter()


@router.get("/tweets/{twitter_id}", response_model=list[TweetsInfo])
async def tweets(twitter_id: int, limit: int = 10) -> list[TweetsInfo]:
    return TweetsInfo()

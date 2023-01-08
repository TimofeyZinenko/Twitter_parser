from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.tweets_service import TweetsService, get_tweets_service


class TweetsInfo(BaseModel):
    tweet: dict = {}


router = APIRouter()


@router.get("/tweets/{twitter_id}", response_model=list[TweetsInfo])
async def tweets(
    twitter_id: int,
    limit: int = 10,
    twts_service: TweetsService = Depends(get_tweets_service),
) -> List[TweetsInfo]:
    tweets = await twts_service.get_by(twitter_id=twitter_id, limit=limit)
    if not tweets:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"user whose id is {twitter_id} does not post any tweets yet!",
        )
    return tweets

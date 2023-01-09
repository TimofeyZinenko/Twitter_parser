import json
from functools import lru_cache
from typing import List

from fastapi import Depends
from src.db.abstract_cashe import AsyncCacheStorage
from src.db.redis_cache import get_redis_cacher
from src.db.twitter_api import get_twitter_api
from src.models.tweets import Tweets
from tweepy import API


class TweetsService:
    def __init__(self, cacher: AsyncCacheStorage, twttr_api: API) -> None:
        self.cacher = cacher
        self.twttr_api = twttr_api

    async def get_by(self, twitter_id: int, limit: int = 10) -> List[Tweets]:
        tweets = await self.cacher.get(twitter_id)

        if not tweets:
            tweets = self.twttr_api.user_timeline(user_id=twitter_id, count=limit)
            if not tweets:
                return []
            tweets = [
                Tweets(tweet=tweet).dict() for tweet in map(self.__transorm, tweets)
            ]
            await self.cacher.set(twitter_id, json.dumps(tweets))
            return tweets

    @staticmethod
    def __transorm(tweet):
        tweet = tweet._json
        del tweet["user"]
        return tweet


cacher_obj = Depends(get_redis_cacher)
api_obj = Depends(get_twitter_api)


@lru_cache()
def get_tweets_service(
    cacher: AsyncCacheStorage = cacher_obj,
    twttr_api: API = api_obj,
) -> TweetsService:
    return TweetsService(cacher, twttr_api)

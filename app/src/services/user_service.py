import json
from functools import lru_cache
from typing import Optional

from db.abstract_cashe import AsyncCacheStorage
from db.redis_cache import get_redis_cacher
from db.twitter_api import get_twitter_api
from fastapi import Depends
from models.users import UserParser
from tweepy import API


class UserParcerService:
    def __init__(self, cacher: AsyncCacheStorage, twttr_api: API) -> None:
        self.cacher = cacher
        self.twttr_api = twttr_api

    async def get_by_username(self, username: str) -> Optional[UserParser]:
        user = await self.cacher.get(username)
        if not user:  # user has not been searched yet
            twttr_user = self.twttr_api.get_user(screen_name=username)
            if not twttr_user:
                return None
            user = UserParser.parse_obj(twttr_user._json)
            await self.cacher.set(username, json.dumps(user.json()))
        else:
            user = UserParser.parse_raw(user)

        return user


cacher_obj = Depends(get_redis_cacher)
api_obj = Depends(get_twitter_api)


@lru_cache()
def get_user_parser_service(
    cacher: AsyncCacheStorage = cacher_obj,
    twttr_api: API = api_obj,
) -> UserParcerService:
    return UserParcerService(cacher, twttr_api)

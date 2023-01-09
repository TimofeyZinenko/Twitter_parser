import json
from functools import lru_cache
from typing import List

from fastapi import Depends
from pydantic import parse_obj_as
from src.db.abstract_cashe import AsyncCacheStorage
from src.db.redis_cache import get_redis_cacher
from src.models.sesson_details_model import SessonDetails
from tweepy import API


class SessonDetailsServise:
    def __init__(self, cacher: AsyncCacheStorage) -> None:
        self.cacher = cacher

    async def get_by(self, sesson_id: str) -> List[SessonDetails]:
        details = await self.cacher.get(sesson_id)
        details = json.loads(details)
        if not details:
            return None

        return parse_obj_as(List[SessonDetails], details)


cacher_obj = Depends(get_redis_cacher)


@lru_cache()
def get_sesson_details_service(
    cacher: AsyncCacheStorage = cacher_obj,
) -> SessonDetailsServise:
    return SessonDetailsServise(cacher)

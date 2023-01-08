import json
from functools import lru_cache
from itertools import chain
from operator import getitem
from typing import List

import requests
from core.config import config_settings, status
from db.abstract_cashe import AsyncCacheStorage
from db.redis_cache import get_redis_cacher
from fastapi import Depends
from models.sesson_models import SessonModel
from models.users import UserParser
from pydantic import BaseSettings


class AccountsParserService:
    cur_sesson_id = 0

    def __init__(self, cacher: AsyncCacheStorage, settings: BaseSettings) -> None:
        self.cacher = cacher
        self.url = "https://api.twitter.com/1.1/users/lookup.json"
        self.headers = {"Authorization": f"Bearer {settings.api_bearer_token}"}

    async def get_usernames(self, links: List[str]) -> tuple[map, int]:
        return map(lambda x: getitem(x.strip().split("/"), -1), links), len(links)

    async def get_user_objs(self, screen_names: List, limit: int = 100) -> List:
        to_lookup = [
            name for name in screen_names if not await self.cacher.isKeyExist(name)
        ]

        if not to_lookup:
            return to_lookup

        if len(to_lookup) > 100:
            params_gen = (
                {"screen_name": to_lookup[i : i + limit]}
                for i in range(0, len(to_lookup), limit)
            )
            data = [
                record
                for record in chain(
                    [
                        requests.post(self.url, params=param, headers=self.headers)
                        for param in params_gen
                    ]
                )
            ]
            user_objs = [
                UserParser.parse_obj(user)
                for responce in data
                for user in responce.json()
            ]
        else:
            params = {"screen_name": to_lookup}
            data = requests.get(self.url, params=params, headers=self.headers)
            # await asyncio.gather(say(data, 0.01))
            user_objs = [UserParser.parse_obj(user) for user in data.json()]

        return user_objs

    async def save_to_redis(self, user_objs: List[UserParser]):
        for user in user_objs:
            json_str = user.json()
            await self.cacher.set(user.screen_name, json_str)

    async def data_process(self, links: List[str]):
        screen_names, names_count = await self.get_usernames(links)
        screen_names = list(screen_names)

        usr_objs = await self.get_user_objs(screen_names)

        await self.save_to_redis(usr_objs)

        existed = [name for name in screen_names if await self.cacher.isKeyExist(name)]

        report_data = [
            {"username": name, "status": status.one}
            for name in chain([user.screen_name for user in usr_objs], existed)
        ]

        if len(report_data) != names_count:
            base = set(
                [
                    name
                    for name in chain([user.screen_name for user in usr_objs], existed)
                ]
            )

            diff = [name for name in screen_names if name not in base]
            report_data.extend(
                [{"username": name, "status": status.zero} for name in diff]
            )

        ans = SessonModel(session_id=self.cur_sesson_id)
        json_str = json.dumps(report_data)

        await self.cacher.set(str(self.cur_sesson_id), json_str)
        self.cur_sesson_id += 1
        await self.cacher.set("last session id", str(self.cur_sesson_id))
        return ans


cacher_obj = Depends(get_redis_cacher)


@lru_cache()
def get_sesson_service(
    cacher: AsyncCacheStorage = cacher_obj,
) -> AccountsParserService:
    return AccountsParserService(cacher, config_settings)
